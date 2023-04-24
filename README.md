# mkdocs-simple-hooks

Define your own hooks for mkdocs, without having to create a new package.

# Deprecated!

This plugin is no longer supported, as Mkdocs has its functionality implemented in version 1.4. See the [documentation](https://www.mkdocs.org/user-guide/configuration/#hooks).

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-simple-hooks
```

Next, add a python module to either the `docs/` directory or the root mkdocs directory. Then, add the plugin and hooks definition to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - mkdocs-simple-hooks:
      hooks:
        hook-name: "your.module:hook_function"
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Usage

You can use this plugin to create simple hooks for `mkdocs` without having to create 
a separate plugin package.

Just define a function and register it as a hook in the `mkdocs.yml`. The function shall
have the same API as the desired hook. To see available hooks and their API, see the
events chapter in the [mkdocs documentation][mkdocs-hooks].

## Example

Let's say you want to copy the `README.md` file to `docs/index.md`. To do that, create 
a new file, e.g.: `docs/hooks.py`, and put the following function there:  

```python
import shutil

def copy_readme(*args, **kwargs):
    shutil.copy("README.md", "docs/index.md")
```

Now, register the hook in your `mkdocs.yml`:  

```yaml
plugins:
  - mkdocs-simple-hooks:
      hooks:
        on_pre_build: "docs.hooks:copy_readme"
```

That's all - the `copy_readme()` function will run every time, before building the documentation.  


## Disabling the plugin

You can use the `enabled` option to optionally disable this plugin. A possible use case is local development where you might want faster build times. It's recommended to use this option with an environment variable together with a default fallback (introduced in `mkdocs` v1.2.1, see [docs](https://www.mkdocs.org/user-guide/configuration/#environment-variables)). Example:

```yaml
plugins:
  - mkdocs-simple-hooks:
      enabled: !ENV [ENABLE_MKDOCS_SIMPLE_HOOKS, True]
      hooks:
        on_pre_build: "docs.hooks:copy_readme"
```

Which enables you to disable the plugin locally using:

```bash
export ENABLE_MKDOCS_SIMPLE_HOOKS=false
mkdocs serve
```

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-hooks]: https://www.mkdocs.org/user-guide/plugins/#events
