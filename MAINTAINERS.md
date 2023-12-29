# Maintainers

Contains steps on how to publish to PyPI

## Local Development and Testing
Install package locally
```sh
python setup.py develop
```

## Prerequisite

```sh
pip install --upgrade twine
```

## Build and test package

```sh
python setup.py sdist bdist_wheel
```

Validate locally built package

```sh
twine check dist/*
```

## Publish to TestPyPI for testing

```sh
twine upload --repository testpypi dist/*
```

Install published package to TestPyPI

```sh
pip install -i https://test.pypi.org/simple/ maggport
```

## Publish to PyPI

```sh
twine upload dist/*
```
