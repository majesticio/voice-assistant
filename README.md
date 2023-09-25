
# Jarvis 🦾 🤖
----------
## Python Voice Assistant 🎙️

Welcome to the Python Voice Assistant project! This README provides a brief guide on how to set up and manage this project using the `poetry` dependency management tool.

### Table of Contents

### Project Overview

This project aims to build a sophisticated voice assistant using Python. By employing cutting-edge techniques and libraries, we intend to offer a robust solution for various voice-based tasks and automations.

## Quick start

If everything is already installed:

1. **Activate the Project Environment**

    ```bash
    poetry shell
    ```

2. **Serve the web app**

    ```bash
    hypercorn main.py
    ```

*first timers...*
### Getting Started with Poetry

**Poetry** is a tool for dependency management and packaging in Python. It ensures that you have the right stack everywhere.

1. **Activate the Project Environment**

    To activate the virtual environment associated with this project:

    ```bash
    poetry shell
    ```

2. **Installing Dependencies**

    Once inside the project directory, you can install the required dependencies using:

    ```bash
    poetry install
    ```

### Common Poetry Commands

Here are some common commands you might need during development:

- **Adding a Dependency**

    ```bash
    poetry add [package-name]
    ```

- **Removing a Dependency**

    ```bash
    poetry remove [package-name]
    ```

- **Updating Dependencies**

    ```bash
    poetry update
    ```

- **Building the Project**

    ```bash
    poetry build # package project for PyPi, etc
    ```

### Contributing

If you're looking to contribute to this project, please ensure that any added dependencies are managed through `poetry`. Also, consider opening an issue first to discuss your proposed changes.

### License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

-----

>notes:

`tts_models/en/vctk/vits` multispeaker indexes also sound pretty good and have a nice British accent. I’ve been using `p273`, `p330`, and `p234` quite a lot.