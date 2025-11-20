.PHONY: help run install install-dev clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make run          - Run the Streamlit app"
	@echo "  make install      - Install dependencies using Poetry"
	@echo "  make install-dev  - Install dependencies including dev dependencies"
	@echo "  make clean        - Clean Poetry cache and virtual environment"
	@echo "  make help         - Show this help message"

# Run the Streamlit app
run:
	@echo "Starting Streamlit app..."
	poetry run streamlit run main.py

# Install dependencies
install:
	@echo "Installing dependencies..."
	poetry install --no-dev

# Install dependencies including dev dependencies
install-dev:
	@echo "Installing dependencies (including dev)..."
	poetry install

# Clean Poetry cache and virtual environment
clean:
	@echo "Cleaning Poetry cache..."
	poetry cache clear pypi --all -n
	@echo "To remove virtual environment, run: poetry env remove python"

