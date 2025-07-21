# LLM Module

A movie recommendation system using local language models with streaming support.

## What it does

- Provides movie recommendations based on user queries
- Uses structured prompts with thinking, question, and recommendation tags
- Supports both CLI and web API interfaces
- Streams responses in real-time (Only supported for CLI)
- Filters movie data based on query keywords
- Asks for clarification when user requests are vague

## Components

- **core.py**: Main LLM engine with movie data processing and streaming
- **web.py**: Flask API server with `/query` and `/health` endpoints
- **cli.py**: Command-line interface with interactive mode
- **app.py**: Entry point for running in server or CLI mode (server mode as default)

## Usage

**API Endpoints:**
- `POST /query`: Submit movie recommendation requests
  ```json
  {
    "prompt": "I want a sci-fi movie"
  }
  ```
- `GET /health`: Health check

### Test Cli Mode

Test 1
```bash
docker-compose run -it --rm llm-app python app.py --mode cli interactive 
```
Test 2
```bash
docker-compose run -it --rm llm-app python app.py --mode server 
```

### Test Server Mode

Test 1
```bash
curl -X POST http://localhost:5050/query \                                                                         ✔ │ ≡ │ 3.11.0 Py │ 05:42:38 
  -H "Content-Type: application/json" \
  -d '{"prompt": "Recommend me an action movie"}'
```
Test 2
```bash
curl http://localhost:5050/health  
```


### Expected Behavior
- Vague queries (e.g., "recommend movies") should return clarification questions
- Specific queries should return movie recommendations with reasoning
- Responses are streamed in real-time
- Movie data is filtered based on query keywords

## Data Format

The system expects a JSON file with movie data containing:
- Title
- Director
- Release Date
- Age Restriction

Set the path via `JSON_DATA_PATH` environment variable.

## Troubleshooting

- **Model loading fails**: Check HuggingFace cache and model name
- **No movie data**: Verify `JSON_DATA_PATH` points to valid JSON file
- **GPU issues**: Set `DEVICE_MAP=cpu` to force CPU mode
