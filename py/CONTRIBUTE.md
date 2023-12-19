## Local Development

### Prerequisites

Switch to your python virtual environment which contains all of the installed required libraries for this project. If you haven't setup your environment yet, I recommend installing miniconda and creating a new virtual env.

```sh
brew install --cask miniconda
```

Utilize [pip-tools](https://github.com/jazzband/pip-tools) to generate development and production dependencies.

```sh
pip install pip-tools
```

Generate the full list of dependencies in requirements.txt needed to develop the package.

```sh
make compile-all
```

Install the dependencies complied by the previous command.

```sh
make install-dev
```
