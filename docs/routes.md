# Routes

The key feature that Dark Star offers is using the filesystem for routing. I.e. your file paths will become your application routes.


## Route file format


Route files are python files. Any python code they contain will be wrapped into a view function and passed to Starlette.

For example, the following code:

    user = request.path_params["user"]


Will get converted into the following function:

    def some_random_function_name(request):
        user = request.path_params["user"]
        return templates.TemplateResponse("<path_to_the_python_file>", {...})


The function's name is based off a hash of the file path, and so should be considered random to all intents and purposes.

The return value is added to the end of all functions, so it is important that a template also be defined in the file. Templates are defined by adding a triple-quoted string to the end of the file.

For example:


    user = request.path_params["user"]
    """
    {% extends 'index.py' %}
    Hello {{user}} - welcome to Dark Star
    """

The `user` variable is passed into the template and can be used as shown.

## Route methods and name

If you want to specify methods for a route rather than the default `GET`, then
you can use a special comment at the top of the file.

The following example shows a route that accepts both `GET` and `POST` requests:

```python
# methods="GET, POST"
if request.method == "POST":
    .... # process POST request
elif request.method == "GET":
    .... # process GET request
```

The methods need to be specified as a comma-separated list in a double-quoted string.

Similarly, the route's name can be specified in the same comment using the
`name=<name>` syntax. The following example shows a method named
`registration-form` that accepts `GET` and `POST` requests:

```python
# methods="GET, POST" name="registration-form"
if request.method == "POST":
    .... # process POST request
elif request.method == "GET":
    .... # process GET request
```

The `name` parameter is used when you want to obtain the url for a route using
the `url_for` helper. See the [Starlette docs](https://www.starlette.io/routing/#reverse-url-lookups)
for more information.
