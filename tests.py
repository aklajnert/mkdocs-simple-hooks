import yaml
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_mkdocs(plugin_config, monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    monkeypatch.syspath_prepend(tmpdir)
    (tmpdir / "docs").mkdir()
    (tmpdir / "site").mkdir()
    runner = CliRunner()
    with open((tmpdir / "mkdocs.yml"), "w") as f:
        yaml.dump(
            {
                "site_name": "test",
                "docs_dir": "docs",
                "site_dir": "site",
                "plugins": [{"mkdocs-simple-hooks": {"hooks": plugin_config}}],
            },
            f,
        )
    return runner


def test_no_hooks_defined(tmpdir, monkeypatch):
    runner = setup_mkdocs({}, monkeypatch, tmpdir)

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert (
        "Warning: No hooks defined. The mkdocs-simple-hooks plugin will not run anything."
        in result.output
    )


def test_wrong_hook(tmpdir, monkeypatch):
    runner = setup_mkdocs({"no_hook": "test"}, monkeypatch, tmpdir)

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert "'no_hook' is not valid hook name, will be ignored."


def test_no_such_module(tmpdir, monkeypatch):
    runner = setup_mkdocs(
        {"on_pre_build": "test_docs.hooks:on_pre_build"}, monkeypatch, tmpdir
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert "Cannot import module 'test_docs.hooks'" in result.output


def test_no_attribute(tmpdir, monkeypatch):
    test_docs = tmpdir / "no_attribute"
    test_docs.mkdir()

    with open(test_docs / "hooks.py", "w") as f:
        f.write("TEST = True")

    runner = setup_mkdocs(
        {"on_pre_build": "no_attribute.hooks:on_pre_build"}, monkeypatch, tmpdir
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert (
        "Config value: 'plugins'. Warning: Module 'no_attribute.hooks' doesn't have attribute 'on_pre_build'"
        in result.output
    )


def test_no_function(tmpdir, monkeypatch):
    test_docs = tmpdir / "no_function"
    test_docs.mkdir()

    with open(test_docs / "hooks.py", "w") as f:
        f.write("on_pre_build = True")

    runner = setup_mkdocs(
        {"on_pre_build": "no_function.hooks:on_pre_build"}, monkeypatch, tmpdir
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert "'no_function.hooks:on_pre_build' is not callable." in result.output


def test_valid_hook(tmpdir, monkeypatch):
    test_docs = tmpdir / "valid_hook"
    test_docs.mkdir()

    with open(test_docs / "hooks.py", "w") as f:
        f.write(
            "def on_pre_build(*args, **kwargs):\n"
            '    print("from on_pre_build")\n'
            "def on_post_build(*args, **kwargs):\n"
            '    print("from on_post_build")\n'
        )

    runner = setup_mkdocs(
        {
            "on_pre_build": "valid_hook.hooks:on_pre_build",
            "on_post_build": "valid_hook.hooks:on_post_build",
        },
        monkeypatch,
        tmpdir,
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert result.output == "from on_pre_build\nfrom on_post_build\n"
