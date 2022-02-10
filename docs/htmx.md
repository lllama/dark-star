# Working with htmx

Dark Star includes functionality to make working with
[htmx](https://htmx.org) easier. In particular, it includes a piece of
middleware to allow access to the `request.state.htmx` variable, which can be
used in functions and templates to test whether a request came from htmx.

## Example Template File

In the following example, the template will only extend `index.py` if the
request is not from htmx.

    profile = request.path_params.get("profile")

    """
    {% if request.state.htmx %}{% extends 'index.py' %}{% endif %}
    Hello {{profile}} - here are your account details

    ...
    """
