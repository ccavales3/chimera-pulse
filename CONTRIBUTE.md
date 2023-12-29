## Local Development

When contributing to this repo. Please follow [pep 8](https://peps.python.org/pep-0008/) naming convention standard. 

Implement following [click](https://click.palletsprojects.com/en/8.1.x/) framework standards

### Prerequisites

Switch to your python virtual environment which contains all of the installed required libraries for this project. If you haven't setup your environment yet, I recommend installing miniconda and creating a new virtual env.

```sh
brew install --cask miniconda
```

Utilize [pip-tools](https://github.com/jazzband/pip-tools) to generate development and production dependencies.

```sh
pip install pip-tools
```

Intall [setuptools](https://github.com/pypa/setuptools) to hanlde facilitation of python packages
```sh
pip install setuptools
```

Compiles and install the dependencies complied by the previous command.

```sh
make install-dev
```
