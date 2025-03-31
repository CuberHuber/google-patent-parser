# Adeptus Patents

[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)
[![We recommend IntelliJ IDEA](https://www.elegantobjects.org/intellij-idea.svg)](https://www.jetbrains.com/idea/)

A Python project using UV for dependency management.

## Purpose
The main goal is to try to implement pure-oop on [Elegant Objects](https://www.elegantobjects.org/) into [a learning project](https://github.com/N0kr0s/adeptus_patents).

## Features:
   - EO principles
   - A Parameterized decorator as a Class
   - Environment as an Object
   - Multi-constructor (Only one primary constructor) through `multipledispatch.dispatch`
   - A Decorator pattern
   - Nor `None` references

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
