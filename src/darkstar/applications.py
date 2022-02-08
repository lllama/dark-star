import ast
from hashlib import md5
from pathlib import Path
from tokenize import tokenize, COMMENT
from io import BytesIO
import shlex
import typing

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.routing import Mount
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

from .templating import Jinja2Templates


dark_star_templates = None


class FunctionAdder(ast.NodeTransformer):
    """Makes our bare files into functions"""

    def __init__(self, template_path, function_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function_name = function_name
        self.template_path = template_path
        self.new_return = ast.parse(
            f"""return dark_star_templates.TemplateResponse("{self.template_path}", locals())"""
        )

    def visit_Module(self, node):
        super().generic_visit(node)

        wrapper = ast.AsyncFunctionDef(
            name=self.function_name,
            decorator_list=[],
            args=ast.arguments(
                posonlyargs=[],
                kwonlyargs=[],
                defaults=[],
                kw_defaults=[],
                args=[ast.arg(arg="request")],
            ),
        )
        wrapper.body = node.body
        wrapper.body.extend(self.new_return.body)
        node.body = [wrapper]
        return node


def get_options(code):
    tokens = tokenize(BytesIO(code.strip().encode("utf-8")).readline)
    for toknum, tokval, (srow, scol), *_ in tokens:
        if srow > 1:
            return {}
        if toknum == COMMENT:
            _, *options = shlex.split(tokval)
            break
    route_options = {}
    if options:
        for option in options:
            key, _, value = option.partition("=")
            if key == "methods":
                route_options[key] = [x.strip() for x in value.split(",")]
            elif key == "name":
                route_options[key] = value
    return route_options


class DarkStar(Starlette):
    def __init__(
        self,
        routes_path: typing.Union[str, Path] = "routes",
        debug: bool = False,
        routes: typing.Sequence[BaseRoute] = [],
        static_directory: str = "static",
        middleware: typing.Sequence[Middleware] = None,
        exception_handlers: typing.Mapping[
            typing.Any,
            typing.Callable[
                [Request, Exception], typing.Union[Response, typing.Awaitable[Response]]
            ],
        ] = None,
        on_startup: typing.Sequence[typing.Callable] = None,
        on_shutdown: typing.Sequence[typing.Callable] = None,
        lifespan: typing.Callable[["Starlette"], typing.AsyncContextManager] = None,
    ) -> None:

        global dark_star_templates
        dark_star_templates = Jinja2Templates(routes_path)

        path_routes = self._collect_routes(routes_path)

        if not any(
            type(route) == Mount and type(route.app) == StaticFiles for route in routes
        ):
            routes.append(Mount("/static/", StaticFiles(directory=static_directory)))

        super().__init__(
            debug,
            path_routes + routes,
            middleware,
            exception_handlers,
            on_startup,
            on_shutdown,
        )

    def _collect_routes(self, routes_path) -> typing.Sequence[BaseRoute]:
        routes = []

        for path in Path(routes_path).rglob("*.py"):
            if path.is_file():
                python = path.read_text()
                function_name = f"ds_{md5(str(path).encode()).hexdigest()}"

                modded_function = ast.fix_missing_locations(
                    FunctionAdder(path.relative_to(routes_path), function_name).visit(
                        ast.parse(python)
                    )
                )

                exec(compile(modded_function, f"{path}", "exec"), globals())

                route_options = get_options(python)

                routes.append(
                    Route(
                        f"/{path.relative_to(routes_path).with_suffix('')}/",
                        globals()[function_name],
                        **route_options,
                    )
                )

        async def index_route(request):
            return dark_star_templates.TemplateResponse(
                "index.html", {"request": request}
            )

        routes.append(Route("/", index_route))
        return routes
