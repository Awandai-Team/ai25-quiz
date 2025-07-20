"""Command-line interface for LLM interactions."""
import argparse
import click
import logging
import sys
from core import LLMEngine

logger = logging.getLogger(__name__)

# Shared LLM engine instance
engine = LLMEngine()

@click.group()
def cli_group():
    """LLM CLI: Interact with LLM via commands."""
    pass

@cli_group.command()
@click.argument('prompt', required=False)
def query(prompt: str):
    """Query the LLM with a prompt."""
    if not prompt:
        prompt = click.prompt("Enter your LLM prompt")
    try:
        response = engine.query_llm(prompt)
    except Exception as e:
        logger.error(f"Error in CLI query: {e}")
        click.echo("An error occurred. Check logs for details.", err=True)

@cli_group.command()
def interactive():
    """Start an interactive CLI session."""
    click.echo("Interactive mode: Type prompts or 'exit' to quit.")
    messages = []  # Track conversation history
    while True:
        prompt = click.prompt("Prompt", prompt_suffix=": ", default="", show_default=False)
        if prompt.lower() == 'exit':
            click.echo("Goodbye!")
            break
        response, is_question = engine.query_llm(prompt, messages=messages)
        if is_question:
            click.echo("(Model needs more details—answer the question above to continue.)")
        else:
            messages = []  # Reset for new conversation

def parse_and_run():
    """Parse arguments and run the selected mode (CLI or server)."""
    parser = argparse.ArgumentParser(description="Run the LLM app in server or CLI mode.")
    parser.add_argument('--mode', choices=['server', 'cli'], required=True, 
                        help="Choose 'server' for Flask web interface, or 'cli' for command-line interface.")
    args, extra_args = parser.parse_known_args()

    if args.mode == 'server':
        from web import start_flask_server
        start_flask_server()
    elif args.mode == 'cli':
        sys.argv = [sys.argv[0]] + extra_args
        cli_group()
