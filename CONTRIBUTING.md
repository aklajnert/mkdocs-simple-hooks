# Contributing

Editable install (run in root of repository):

```shell
pip install -e .
```

Setup pre-commit:

```shell
pip install pre-commit
pre-commit install
```

Setup unit testing:

```shell
pip install --upgrade nox pytest pytest-cov
nox
```