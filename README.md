# mkdocs-simple-hooks

Define your own hooks for mkdocs, without having to create a new package.

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-simple-hooks
```

Next, add the plugin and hooks definition to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - mkdocs-simple-hooks:
      hooks:
        - hook-name: "your.module:hook_function"
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Usage

You can use this plugin to create simple hooks for `mkdocs` without having to create 
a separate plugin package.

Just define a function and register it as a hook in the `mkdocs.yml`. The function shall
have the same API as the desired hook. To see available hooks and their API, see the
events chapter in the [documentation][mkdocs-hooks].

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
        - on_pre_build: "docs.hooks:copy_readme"
```

That's all - the `copy_readme()` function will run every time, before building the documentation.  


[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-hooks]: https://www.mkdocs.org/user-guide/plugins/#events
