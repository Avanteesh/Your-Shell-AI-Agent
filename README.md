# Shell AI Agent 🤖

A powerful AI agent designed to assist you with shell-related tasks, automations, and command executions. This project leverages AI to make your command-line experience smarter, faster, and more efficient.


## Features

- **Smart Command Execution**: Execute shell commands with AI-powered suggestions and validations.
- **Task Automation**: Automate repetitive tasks with AI-driven scripts.
- **Cross-Platform Support**: Works seamlessly on Linux, macOS, and Windows.
- **Natural Language Processing**: Interact with your shell using natural language commands.
- **Error Handling**: AI-assisted error detection and troubleshooting.
- **Get Weather**: Get to know whats the weather around the world right now!


## Installation

### Prerequisites

- Python 3.11 or higher
- A stable internet connection (for AI model interactions)
- Basic familiarity with the command line


### Steps for building

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/shell-ai-agent.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd shell-ai-agent
   ```

3. **initialize Virtual environment**
   ```bash
   uv venv # initialize venv!
   ```
4. **Add your API keys in the .env file**
   API key for Mistral: <a href="https://mistral.ai/">MistralAI</a>
   API key for weather api: <a href="https://www.weatherapi.com/">Free Weather API</a>
   
5. **Run the AI Agent**
   ```bash
   python3 app.py # or
   uv run app.py
   ```


## Usage

### Basic Commands

- **Execute a Shell Command**
  ```bash
  python3 app.py --prompt "run ls -la in the current directory"
  ```

- **Get Help**
  ```bash
  python3 app.py --prompt "how do I list all files modified in the last 24 hours?"
  ```

- **Get weather in countries around the world!**
  ```bash
  python3 app.py --prompt "Whats the current weather in Santiago?"
  ```


### Advanced Features

- **Multi-Step Workflows**: Chain multiple commands together for complex tasks.
- **Learning Mode**: Teach the AI agent new commands and workflows.

## Examples

1. **List Files in a Directory**
   ```bash
   python3 app.py --prompt "What folder am I at currently?"
   ```

2. **Search for a File**
   ```bash
   python3 app.py --prompt "find all .txt files in the current directory and its subdirectories"
   ```

3. **Automate Git Workflow**
   ```bash
   python3 app.py --prompt "commit all changes with the message Updated README and push to the main branch"
   ```

## Contributing

Contributions are welcome! Here’s how you can help:

1. **Fork the Repository**
2. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
4. **Commit Your Changes**
   ```bash
   git commit -m "Add your message here"
   ```
5. **Push to the Branch**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contact

for Queries or feedback? Reach out to us at:

- Email: eshan.avanti@example.com
- GitHub: [Avanteesh](https://github.com/Avanteesh)


---

Happy coding! 🚀
