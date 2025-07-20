from flask import Flask, request
import argparse
import logging
import os

app = Flask(__name__)

# Ensure log directory exists
log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(log_path, exist_ok=True)

# Configure logging
log_file = os.path.join(log_path, "api1.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Middleware to log each request
@app.before_request
def log_request():
    logging.info(f"{request.method} {request.path} from {request.remote_addr}")

# Example routes
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    return {"status": "success"}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Movie LLM')
    
    parser.add_argument('--debug', action='store_true',
                       help='Run in debug mode')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    app.run(debug=args.debug)
