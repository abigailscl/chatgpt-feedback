### Project README

#### 1. Description

Develop an API that allows employees to receive, display feedback, and generate action items for improvement, using the OpenAI GPT-3.5 model to summarize these action items. 

#### 2. Local Environment Setup

Before getting started with the project, ensure you have the following prerequisites installed on your local machine:

- Docker: [https://docs.docker.com/engine/install/]
- Python: For macOS, Linux, and Windows, you can install Python using the official installer from [python.org](https://www.python.org/).

#### 3. Makefile Commands

The following commands are available for managing the project using the Makefile:

- `make docker-up`: Start the API.
- `make run-test`: Run tests.
- `make run-cov`: Run tests and display coverage report.
- `make run-lint`: Run linters.
- `make run-mypy`: Run the mypy tool.

To use these commands, simply open a terminal in the project directory and run `make` followed by the desired command.

### Architecture

[app/

    ├── application/
    │   ├── dtos/
    │   └── use_cases/
    ├── domain/
    │   ├── repositories/
    │   └── models/
    ├── infrastructure/
    │   └── api/
    │   └── database/
    │   └── chatgpt/
    └── tests/
]

That's it! You're all set to get started with the project. If you encounter any issues or have any questions, feel free to reach out to us.

Happy coding!