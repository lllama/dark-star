# Dark Star

Dark Star is a simple web framework built on top of Starlette that prioritises
server-side rendering with templates.

The vast majority of functionality is delegated to Starlette - Dark Star helps
you organise your code and keeps your code next to your templates.

## Installation

Install with `pip`:

    pip install dark-star


## Example Project layout

    my_app.py            # The main application file
    routes/
        index.html       # The root template - inherited by other templates
        users.py         # A template file that maps to the /users/ url
        users/
            {profile}.py # A template that maps to the /user/{profile}/ url 
                         # and lets the code access the value of `profile`
## Example Template File

The following example shows how code and templates live together:

```python
profile = request.path_params.get("profile")

"""
{% extends 'index.html' %}
Hello {profile} - here are your account details

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
    {% extends 'index.html' %}
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
