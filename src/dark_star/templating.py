from starlette.templating import Jinja2Templates as StarletteJinja2Templates
import typing
from os import PathLike
from pathlib import Path
import os


from starlette.background import BackgroundTask
from starlette.responses import Response
from starlette.types import Receive, Scope, Send

import jinja2
from jinja2.environment import Environment
from jinja2.loaders import (
    split_template_path,
    FileSystemLoader as JinjaFileSystemLoader,
)
from jinja2.exceptions import TemplateNotFound

from jinja2.utils import open_if_exists

# @contextfunction renamed to @pass_context in Jinja 3.0, to be removed in 3.1
if hasattr(jinja2, "pass_context"):
    pass_context = jinja2.pass_context
else:  # pragma: nocover
    pass_context = jinja2.contextfunction


DARK_STAR_SEPARATOR = "----[DarkStar]----"

TEMPLATE_TEMPLATE = """
{{% if not request.state.htmx %}}{{% extends '{template_parent}' %}}{{% endif %}}

{{% block children %}}
{template}
{{% endblock children %}}

"""


def get_parent_template(path, root):
    path = Path(path)

    if path.relative_to(root).parent == Path("."):
        template_parent = "index.html"
    else:
        template_parent = str(path.relative_to(root).parent.with_suffix(".py"))

    return template_parent


class FileSystemLoader(JinjaFileSystemLoader):
    def get_source(
        self, environment: Environment, template: str
    ) -> typing.Tuple[str, str, typing.Callable[[], bool]]:
        pieces = split_template_path(template)
        for searchpath in self.searchpath:
            filename = os.path.join(searchpath, *pieces)
            print(f"Searching for {filename}")
            f = open_if_exists(filename)
            if f is None:
                continue
            try:
                contents = f.read().decode(self.encoding)
            finally:
                f.close()

            print("Found it!!")

            if not Path(filename) == Path(searchpath) / "index.html":
                template_parent = get_parent_template(filename, searchpath)

                *_, contents = contents.partition(DARK_STAR_SEPARATOR)
                # contents = TEMPLATE_TEMPLATE.format(
                #     template=contents, template_parent=template_parent
                # )
                # print(contents)

            mtime = os.path.getmtime(filename)

            def uptodate() -> bool:
                try:
                    return os.path.getmtime(filename) == mtime
                except OSError:
                    return False

            return contents, filename, uptodate

        template_parent = get_parent_template(template, "")
        print(f"Parent: {template_parent}")

        # contents = TEMPLATE_TEMPLATE.format(
        #     template="", template_parent=template_parent
        # )
        # print(contents)
        # return contents, template, lambda: True


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
