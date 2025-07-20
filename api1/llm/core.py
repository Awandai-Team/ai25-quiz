"""Core LLM engine for movie recommendations with streaming support."""
import os
import json
import logging
import re
import threading
from dotenv import load_dotenv
from transformers import pipeline, TextIteratorStreamer

load_dotenv()
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Set HuggingFace cache directory
os.environ['HF_HOME'] = os.getenv('HF_HOME', '~/.cache/huggingface')

class LLMEngine:
    def __init__(self):
        model_name = os.getenv('MODEL_NAME', 'Qwen/Qwen3-0.6B')
        try:
            # Get device configuration from environment
            device_map = os.getenv('DEVICE_MAP', 'auto')
            torch_dtype = os.getenv('TORCH_DTYPE', 'auto')
            
            # Force CPU if explicitly requested
            if device_map.lower() == 'cpu':
                device_map = 'cpu'
                torch_dtype = 'auto'
                logger.info("Forcing CPU mode as requested")
            elif device_map.lower() == 'gpu':
                device_map = 'auto'
                logger.info("GPU mode enabled - auto-detecting available GPUs")
            else:
                logger.info(f"Using device_map: {device_map}")
            
            # Initialize text generation pipeline
            self.pipe = pipeline(
                "text-generation",
                model=model_name,
                torch_dtype=torch_dtype,
                device_map=device_map
            )
            self.pipe.tokenizer.padding_side = "left"
            logger.info(f"LLMEngine initialized with model: {model_name}")

            # Load movie data once
            self.json_data = load_json_data()
        except Exception as e:
            logger.error(f"Failed to initialize LLMEngine: {e}")
            raise RuntimeError("Could not load model or data. Check HF cache and env vars.")

    def build_full_prompt(self, prompt: str, messages: list, context: str, reasonEnabled: bool) -> list:
        """Build structured prompt with system instructions."""
        system_prompt = """You are a movie recommender. If the user's request is vague (e.g., no genre or type specified), ask for more details using <question> tag. If you have enough info, recommend directly using <recommendation> tag.
Think step-by-step in <think>: 1. Check if enough details (e.g., genre). 2. If not, ask in <question>. 3. If yes, search data and suggest 1-2 with reasons. Keep it short. Don't ask for more info unless necessary.
Use this data: {context}"""

        if not messages:
            messages = [{"role": "system", "content": system_prompt.format(context=context)}]

        messages.append({"role": "user", "content": prompt})

        # Add thinking mode if enabled
        if reasonEnabled:
            messages[-1]["content"] += "/think"
        else:
            messages.append({"role": "assistant", "content": "<think>\n\n</think>\n\n"})

        return messages

    def query_llm(self, prompt: str, reasonEnabled: bool = True, messages: list = None) -> tuple[str, bool]:
        """Query LLM with streaming response and return if it's a clarification question."""
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Filter movies based on keywords in prompt
        keywords = re.findall(r'\w+', prompt.lower())
        relevant_movies = [movie for movie in self.json_data if any(k in str(movie).lower() for k in keywords)]

        # Format relevant data for context
        if relevant_movies:
            data_string = "\n".join([f"- {movie.get('Title', 'Unknown')} by {movie.get('Director', 'unknown')} (Release: {movie.get('Release Date', 'unknown')}, Age: {movie.get('Age Restriction', 'unknown')})" for movie in relevant_movies])
            context = f"Relevant movies: \n{data_string}\nUse this to make recommendations."
        else:
            context = "No matching movies. Suggest generally or ask for more details."

        # Build full prompt with engineering
        messages = self.build_full_prompt(prompt, messages or [], context, reasonEnabled)

        # Setup streaming
        streamer = TextIteratorStreamer(self.pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)

        # Generation parameters
        generation_kwargs = {
            "do_sample": True,
            "top_k": 20,
            "temperature": 0.6 if reasonEnabled else 0.7,
            "top_p": 0.95,
            "eos_token_id": self.pipe.tokenizer.eos_token_id,
            "max_new_tokens": 16384,
            "streamer": streamer
        }

        # Run generation in separate thread for non-blocking streaming
        generated_text = ""
        def run_generation():
            nonlocal generated_text
            try:
                outputs = self.pipe(messages, **generation_kwargs)
                parsed_outputs = parse_structured_content(outputs)
                full_text = parsed_outputs[0]["generated_text"] if parsed_outputs else ""
                generated_text = full_text
            except Exception as e:
                pass

        thread = threading.Thread(target=run_generation)
        thread.start()

        # Stream and print output
        streamed_output = ""
        for new_text in streamer:
            streamed_output += new_text
            print(new_text, end='', flush=True)

        thread.join()

        # Check if response is a clarification question
        is_question = bool(re.search(r"<question>.*?</question>", streamed_output, flags=re.DOTALL))

        return streamed_output, is_question

def parse_structured_content(outputs):
    """Parse thinking, question, and recommendation tags from LLM output."""
    parsed = []
    for output in outputs:
        content = output["generated_text"]
        msg = {"role": "assistant", "content": content}
        
        # Parse thinking content
        m = re.match(r"<think>\n(.+)</think>\n\n", msg["content"], flags=re.DOTALL)
        if m:
            msg["content"] = msg["content"][len(m.group(0)):]
            thinking_content = m.group(1).strip()
            if thinking_content:
                msg["reasoning_content"] = thinking_content
                
        # Parse question content
        q = re.match(r"<question>\n(.+)</question>\n\n", msg["content"], flags=re.DOTALL)
        if q:
            msg["content"] = msg["content"][len(q.group(0)):]
            question_content = q.group(1).strip()
            if question_content:
                msg["question_content"] = question_content
                
        # Parse recommendation content
        r = re.match(r"<recommendation>\n(.+)</recommendation>\n\n", msg["content"], flags=re.DOTALL)
        if r:
            msg["content"] = msg["content"][len(r.group(0)):]
            rec_content = r.group(1).strip()
            if rec_content:
                msg["recommendation_content"] = rec_content
        parsed.append(msg)
    return parsed

def load_json_data() -> list:
    """Load movie data from JSON file."""
    json_path = os.getenv('JSON_DATA_PATH')
    if not json_path or not os.path.exists(json_path):
        logger.warning("JSON path not set or file missing. Returning empty list.")
        return []
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} movies from {json_path}")
        return data
    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        return []