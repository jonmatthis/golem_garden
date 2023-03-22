# Golem Garden 🌱

Golem Garden is a Python project that manages a collection of GPT-enabled chatbots called "Golems" and a swarm of simple Python scripts enacting "Beetles". The primary purpose of this project is to facilitate user interaction with various golems, providing a seamless experience in obtaining responses from different specialized chatbots.

## Features

- Manage multiple GPT-enabled chatbots called Golems
- Process user inputs and obtain responses from the appropriate Golem
- Store conversation history and user-specific data
- Configuration management using TOML files
- Comprehensive API documentation generated from source code

## Components

- GolemGarden class: Manages golems and processes user inputs
- Golem class: Base class for Golem instances
- GolemFactory class: Factory class for creating Golem instances
- ConfigDatabase class: Handles loading and storing Golem configurations from TOML files
- ContextDatabase class: Manages conversation history and user-specific data
- User Interface: Enables users to interact with the golems

# Installation

To install the golem_garden package using Poetry, follow these steps:

1. [Install Poetry](https://python-poetry.org/docs/#installation) if you haven't already.

2. Clone the `golem_garden` repository:

```bash
   git clone https://github.com/jonmatthis/golem_garden.git
   cd golem_garden
```
3. Install the project dependencies and create a virtual environment:
```bash
  poetry install
```
4. Activate the virtual environment:
```bash 
poetry shell
```

