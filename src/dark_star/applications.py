import ast
from hashlib import md5
from pathlib import Path
import typing

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.routing import Route

from .templating import Jinja2Templates


dark_star_templates = None

function_template = """
def {name}(request):
{python_source}
    return dark_star_templates.TemplateResponse("{template_path}", locals())
"""


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


class DarkStar(Starlette):
    def __init__(
        self,
        routes_path: typing.Union[str, Path] = "routes",
        debug: bool = False,
        routes: typing.Sequence[BaseRoute] = None,
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
        super().__init__(
            debug,
            path_routes + routes if routes else path_routes,
            middleware,
            exception_handlers,
            on_startup,
            on_shutdown,
        )

    def _collect_routes(self, routes_path) -> typing.Sequence[BaseRoute]:
        routes = []

        async def index_route(request):
            return dark_star_templates.TemplateResponse(
                "routes/index.html", {"request": request}
            )

        for path in Path(routes_path).rglob("*"):
            if path == Path(routes_path) / "index.html":
                routes.append(Route("/", index_route))
                continue
            if path.is_file():
                python = path.read_text()
                function_name = f"ds_{md5(str(path).encode()).hexdigest()}"

                modded_function = ast.fix_missing_locations(
                    FunctionAdder(path, function_name).visit(ast.parse(python))
                )

                exec(compile(modded_function, f"{path}", "exec"), globals())

                routes.append(
                    Route(
                        f"/{path.relative_to(routes_path).with_suffix('')}",
                        globals()[function_name],
                    )
                )
        return routes


app = DarkStar()
