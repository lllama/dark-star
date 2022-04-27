# Dark Star

Dark Star is a simple web framework built on top of Starlette that prioritises
server-side rendering with templates.

The vast majority of functionality is delegated to Starlette - Dark Star helps
you organise your code and keeps your code next to your templates.

## Installation

Install with `pip`:

```
pip install darkstar
```

Create a new app:

```
python -m darkstar create-app
# or
darkstar create-app
```


## Starter Application

Dark Star uses default values for its directories, so getting started is very
easy. If you didn't use the CLI's `create-app` command then create an `app.py`
file with the following content:

```python
from darkstar.applications import DarkStar

app = DarkStar()
```

The above code will assume your routes are in the `routes` directory and static
files are in the `static` directory.

You can then run your application using an ASGI server, such as uvircorn:

```python
pip install uvicorn[standard] # if not already installed
uvicorn app:app
```


## Example Project layout

```python
my_app.py            # The main application file
static/              # Static files under /static/
routes/
    index.py         # The root template - inherited by other templates
    users.py         # A template file that maps to the /users/ url
    users/
        {profile}.py # A template that maps to the /user/{profile}/ url
                     # and lets the code access the value of `profile`
```
## Example Template File

Template files are regular python files which contain the template at the end as a triple-quoted string.

```python
profile = request.path_params.get("profile")

"""
{% extends 'index.py' %}
Hello {{profile}} - here are your account details

... other content

"""
```

All templates get passed the `request` parameter as per Starlette's normal
routes. The template is then included as a triple-quoted string at the end of
the file. All variables defined in the code will be available in the template
for use when rendering.

Another example:

    users = Users.objects.all()

    """
    {% extends 'index.py' %}
    <ul>
    {% for user in users %}
        <li>{{user}}</li>
    {% endfor %}
    </ul>
    """


Here the view function uses a `Users` object from an ORM to fetch a list of
users from the database. These are then listed in the template. The `Users`
object can be imported locally in the function, or in the `my_app.py` file at
the root of the project. Anything imported in the `my_app` file is made
available to all view functions.
