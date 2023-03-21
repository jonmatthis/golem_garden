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

To install Golem Garden, follow these steps:

0. Create a `.env` file in the outer package folder and put your API key in it:

   ```bash
   OPENAI_API_KEY= <your API key> #get it from your profile on `https://platform.openai.com` 
   ```

1. Install Python 3.8+ from the [official website](https://www.python.org/downloads/).

2. Clone the Golem Garden repository:

   ```bash
   git clone https://github.com/username/golem_garden.git

3. Install the package:

```bash
    pip install -e . 
```
### Run the program:
```bash
    python -m golem_garden
```

6. Enjoy!