### Makefile

.PHONY: init setup run clean

# Initialize project (create data/ and .env)
init:
	mkdir -p data
	test -f .env || cp .env.sample .env

# Install dependencies and initialize
setup: init
	uv pip install -r requirements.txt

# Example: run main.py (modify as needed)
run:
	python main.py

# Clean up
clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf data/*.tmp  # Example cleanup (modify as needed)
