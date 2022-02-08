import ast
import os
from os import PathLike
from pathlib import Path
import typing

import jinja2
from jinja2.environment import Environment
from jinja2.exceptions import TemplateNotFound
from jinja2.loaders import FileSystemLoader as JinjaFileSystemLoader
from jinja2.loaders import split_template_path
from jinja2.utils import open_if_exists
from starlette.templating import Jinja2Templates as StarletteJinja2Templates

# @contextfunction renamed to @pass_context in Jinja 3.0, to be removed in 3.1
if hasattr(jinja2, "pass_context"):
    pass_context = jinja2.pass_context
else:  # pragma: nocover
    pass_context = jinja2.contextfunction


class TemplateExtractor(ast.NodeVisitor):
    """Makes our bare files into functions"""

    def visit_Constant(self, node):
        super().generic_visit(node)

        self.value = node.value


class FileSystemLoader(JinjaFileSystemLoader):
    def get_source(
        self, environment: Environment, template: str
    ) -> typing.Tuple[str, str, typing.Callable[[], bool]]:

        pieces = split_template_path(template)

        for searchpath in self.searchpath:
            filename = os.path.join(searchpath, *pieces)

            f = open_if_exists(filename)

            if f is None:
                continue
            try:
                contents = f.read().decode(self.encoding)
            finally:
                f.close()

            if Path(filename).suffix == ".py":
                extractor = TemplateExtractor()
                extractor.visit(ast.parse(contents))
                contents = extractor.value

            mtime = os.path.getmtime(filename)

            def uptodate() -> bool:
                try:
                    return os.path.getmtime(filename) == mtime
                except OSError:
                    return False

            return contents, filename, uptodate
        raise TemplateNotFound(template)


class Jinja2Templates(StarletteJinja2Templates):
    def _create_env(
        self, directory: typing.Union[str, PathLike], **env_options: typing.Any
    ) -> "jinja2.Environment":
        @pass_context
        def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
            request = context["request"]
            return request.url_for(name, **path_params)

        loader = FileSystemLoader(directory)
        env_options.setdefault("loader", loader)
        env_options.setdefault("autoescape", True)

        env = jinja2.Environment(**env_options)
        env.globals["url_for"] = url_for
        return env
