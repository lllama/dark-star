import typing

from textwrap import indent
from starlette.applications import Starlette
from starlette.datastructures import State, URLPath
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Router, Route
from starlette.types import ASGIApp, Receive, Scope, Send
from pathlib import Path
import jinja2


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

        self.template_env = jinja2.Environment()

        path_routes = self._collect_routes(routes_path)
        super().__init__(
            debug,
            path_routes + routes if routes else path_routes,
            middleware,
            exception_handlers,
            on_startup,
            on_shutdown,
        )

    def _collect_routes(self, routes_path):
        routes = []
        for path in Path(routes_path).rglob("*"):
            if path.is_file():
                python, _, template = path.read_text().partition("----[DarkStar]----")
                function_source = f"""def wot(request):
{indent(python, '    ')}
    return Response('wowowowo')
"""
                exec(compile(function_source, f"{path}", "exec"), globals())
                routes.append(Route(f"/{path.with_suffix('')}", wot))
        return routes


app = DarkStar()
