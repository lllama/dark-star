# Routes

The key feature that Dark Star offers is using the filesystem for routing. I.e. your file paths will become your application routes.


## Route file format


Route files are simple python files. Any python code they contain will be wrapped into a view function and passed to Starlette.

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
    {% extends 'index.html' %}
    Hello {{user}} - welcome to Dark Star
    """

The `user` variable is passed into the template and can be used as shown.
