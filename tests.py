import yaml
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_mkdocs(plugin_config, monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    monkeypatch.syspath_prepend(tmpdir)
    (tmpdir / "docs").mkdir()
    (tmpdir / "site").mkdir()
    runner = CliRunner()
    with open(str(tmpdir / "mkdocs.yml"), "w") as f:
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
        "Warning: No hooks defined. "
        "The mkdocs-simple-hooks plugin will not run anything." in result.output
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

    with open(str(test_docs / "hooks.py"), "w") as f:
        f.write("TEST = True")

    runner = setup_mkdocs(
        {"on_pre_build": "no_attribute.hooks:on_pre_build"}, monkeypatch, tmpdir
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert (
        "Config value: 'plugins'. "
        "Warning: Module 'no_attribute.hooks' doesn't have attribute 'on_pre_build'"
        in result.output
    )


def test_no_function(tmpdir, monkeypatch):
    test_docs = tmpdir / "no_function"
    test_docs.mkdir()

    with open(str(test_docs / "hooks.py"), "w") as f:
        f.write("on_pre_build = True")

    runner = setup_mkdocs(
        {"on_pre_build": "no_function.hooks:on_pre_build"}, monkeypatch, tmpdir
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert "'no_function.hooks:on_pre_build' is not callable." in result.output


def test_valid_hook_package(tmpdir, monkeypatch):
    test_docs = tmpdir / "hooks_pkg"
    test_docs.mkdir()
    open(str(test_docs / "__init__.py"), "w").close()

    with open(str(test_docs / "hooks.py"), "w") as f:
        f.write(
            "def on_pre_build(*args, **kwargs):\n"
            '    print("from on_pre_build")\n'
            "def on_post_build(*args, **kwargs):\n"
            '    print("from on_post_build")\n'
        )

    runner = setup_mkdocs(
        {
            "on_pre_build": "hooks_pkg.hooks:on_pre_build",
            "on_post_build": "hooks_pkg.hooks:on_post_build",
        },
        monkeypatch,
        tmpdir,
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert result.output == "from on_pre_build\nfrom on_post_build\n"


def test_valid_hook_namespace_package(tmpdir, monkeypatch):
    test_docs = tmpdir / "hooks_ns_pkg"
    test_docs.mkdir()

    with open(str(test_docs / "hooks.py"), "w") as f:
        f.write(
            "def on_pre_build(*args, **kwargs):\n"
            '    print("from on_pre_build")\n'
            "def on_post_build(*args, **kwargs):\n"
            '    print("from on_post_build")\n'
        )

    runner = setup_mkdocs(
        {
            "on_pre_build": "hooks_ns_pkg.hooks:on_pre_build",
            "on_post_build": "hooks_ns_pkg.hooks:on_post_build",
        },
        monkeypatch,
        tmpdir,
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert result.output == "from on_pre_build\nfrom on_post_build\n"


def test_valid_hook_subpackage(tmpdir, monkeypatch):
    test_package = tmpdir / "hooks_top_pkg"
    test_package.mkdir()
    open(str(test_package / "__init__.py"), "w").close()
    test_docs = test_package / "hooks_sub_pkg"
    test_docs.mkdir()
    open(str(test_docs / "__init__.py"), "w").close()

    with open(str(test_docs / "hooks.py"), "w") as f:
        f.write(
            "def on_pre_build(*args, **kwargs):\n"
            '    print("from on_pre_build")\n'
            "def on_post_build(*args, **kwargs):\n"
            '    print("from on_post_build")\n'
        )

    runner = setup_mkdocs(
        {
            "on_pre_build": "hooks_top_pkg.hooks_sub_pkg.hooks:on_pre_build",
            "on_post_build": "hooks_top_pkg.hooks_sub_pkg.hooks:on_post_build",
        },
        monkeypatch,
        tmpdir,
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert result.output == "from on_pre_build\nfrom on_post_build\n"


def test_valid_hook_module(tmpdir, monkeypatch):
    with open(str(tmpdir / "hooks.py"), "w") as f:
        f.write(
            "def on_pre_build(*args, **kwargs):\n"
            '    print("from on_pre_build")\n'
            "def on_post_build(*args, **kwargs):\n"
            '    print("from on_post_build")\n'
        )

    runner = setup_mkdocs(
        {"on_pre_build": "hooks:on_pre_build", "on_post_build": "hooks:on_post_build",},
        monkeypatch,
        tmpdir,
    )

    result = runner.invoke(build_command)
    assert result.exit_code == 0
    assert result.output == "from on_pre_build\nfrom on_post_build\n"
