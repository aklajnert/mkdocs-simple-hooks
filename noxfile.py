import nox


@nox.session(python=["3.5", "3.6", "3.7", "3.8", "pypy3"])
def tests(session):
    session.install(".[test]")
    session.run(
        "pytest", "--cov=mkdocs_simple_hooks", "tests.py", "--cov-fail-under=100"
    )


@nox.session
def flake8(session):
    session.install("flake8")
    session.run("flake8", "mkdocs_simple_hooks", "tests.py")


@nox.session
def create_dist(session):
    session.install("twine")
    session.run("python", "setup.py", "sdist", "bdist_wheel")
    session.run("twine", "check", "dist/*")


@nox.session
def publish(session):
    """Publish to pypi. Run `nox publish -- prod` to publish to the official repo."""
    create_dist(session)
    twine_command = ["twine", "upload", "dist/*"]
    if "prod" not in session.posargs:
        twine_command.extend(["--repository-url", "https://test.pypi.org/legacy/"])
    session.run(*twine_command)
