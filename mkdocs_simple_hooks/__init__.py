import importlib
import os
import sys
from functools import partial
from pathlib import Path

import mkdocs

try:
    ModuleNotFoundError
except NameError:  # pragma: no cover
    ModuleNotFoundError = ImportError


class SimpleHooksPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("hooks", mkdocs.config.config_options.Type(dict, default={})),
        ("enabled", mkdocs.config.config_options.Type(bool, default=True)),
    )

    def load_config(self, options, config_file_path=None):
        errs, warns = super(SimpleHooksPlugin, self).load_config(
            options, config_file_path
        )

        if not self.config.get("enabled"):
            return errs, warns

        hooks = self.config.get("hooks", {})
        if not hooks:
            warns.append(
                "No hooks defined. The mkdocs-simple-hooks plugin will not run anything."
            )
        for name, hook_path in hooks.items():
            if not name.startswith("on_"):
                warns.append(
                    "'{}' is not valid hook name, will be ignored.".format(name)
                )
                continue

            hook_function = self._get_function(hook_path, warns)
            if hook_function:
                setattr(self, name, partial(self.handle_hook, hook=hook_function))

        return errs, warns

    def handle_hook(self, *args, hook, **kwargs):
        return hook(*args, **kwargs)

    def _get_function(self, hook_path, warns):
        cwd = Path(os.getcwd())
        root_dir = cwd.parent
        if str(cwd) not in sys.path:  # pragma: no cover
            sys.path.append(str(cwd))
        # allow hooks to be stored in the project's root directory
        if str(root_dir) not in sys.path:
            sys.path.append(str(root_dir))

        package_path, function = hook_path.split(":")
        try:
            hook_module = importlib.import_module(package_path)
        except ModuleNotFoundError:
            warns.append("Cannot import module '{}'.".format(package_path))
            return
        hook_function = getattr(hook_module, function, None)
        if not hook_function:
            warns.append(
                "Module '{}' doesn't have attribute '{}'.".format(
                    package_path, function
                )
            )
            return
        if not callable(hook_function):
            warns.append("'{}' is not callable.".format(hook_path))
            return
        return hook_function
