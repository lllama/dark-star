# Dark Star CLI

Dark Star comes with a CLI that helps you perform basic tasks.

Run it using the command `darkstar`.

```sh
$ darkstar
Usage: cli [OPTIONS] COMMAND [ARGS]...

  Dark Star - a web framework based on Starlette

Options:
  --help  Show this message and exit.

Commands:
  create-app
  new-route
```

## `create-app`

`create-app` takes a directory where a new app and directory structure will be
created.

```sh
$ darkstar create-app --help
Usage: cli create-app [OPTIONS] DIRECTORY

Options:
  --htmx / --no-htmx  Include htmx script in index.py
  --help              Show this message and exit.
```

The `--htmx` option will include `script` tags for htmx and hyperscript in the
default `index.py` file.

## `new-route`

`new-route` takes a route path and creates the python file in the correct
location. It will also parse any path parameters and add code to extract them
from the request.
