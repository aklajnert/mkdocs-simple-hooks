import mkdocs
import os
import sys
from functools import partial

try:
    ModuleNotFoundError
except NameError:  # pragma: no cover
    ModuleNotFoundError = ImportError


class SimpleHooksPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (("hooks", mkdocs.config.config_options.Type(dict, default={})),)

    def load_config(self, options, config_file_path=None):
        errs, warns = super(SimpleHooksPlugin, self).load_config(
            options, config_file_path
        )
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
        cwd = os.getcwd()
        if cwd not in sys.path:  # pragma: no cover
            sys.path.append(cwd)

        package_path, function = hook_path.split(":")
        try:
            hook_module = __import__(package_path)
        except ModuleNotFoundError:
            warns.append("Cannot import module '{}'.".format(package_path))
            return
        module_name = package_path.split(".")[-1]
        if hasattr(hook_module, module_name) and hook_module.__name__ != module_name:
            hook_module = getattr(hook_module, module_name)
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
