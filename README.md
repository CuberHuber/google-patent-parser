# Adeptus Patents

A Python project using UV for dependency management.

## Purpose
The main goal is to try to implement pure-oop on [Elegant Objects](https://www.elegantobjects.org/) into [a learning project](https://github.com/N0kr0s/adeptus_patents).


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/CuberHuber/google-patent-parser
    cd google-patent-parser
    ```

2. Create and activate a virtual environment (recommended):
    ```bash
    uv venv  # Creates a virtual environment in .venv
    source .venv/bin/activate  # On Unix/macOS
    ```

3. Install dependencies and initialize the project:
    ```bash
    make setup
    ```

## Configuration
1. A `data/` directory will be created automatically.
2. The `.env` file is generated from `.env.sample` during setup. Update it with your configuration:
    ```bash
    nano .env
    ```

## Start Up
1. Run the Application

    ```bash
    make run
    ```
