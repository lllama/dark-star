import ast
from io import BytesIO
from shlex import split
from tokenize import COMMENT
from tokenize import tokenize

from astpretty import pprint

code1 = """
print(2)
print(2)
"""
code2 = """
async def f(request):
    print(2)
"""


class NumberChanger(ast.NodeTransformer):
    """Changes all number literals to 42."""

    def visit_Module(self, node):
        super().generic_visit(node)

        if isinstance(node, ast.Module):
            wrapper = ast.AsyncFunctionDef(
                name="do_request",
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
            node.body = [wrapper]
            return node
        if not isinstance(node, ast.Constant) or not isinstance(node.value, int):
            return node

        return ast.Constant(value=42)


# pprint(ast.parse(code1))
# pprint(ast.parse(code2))
# pprint(a)
modded1 = ast.fix_missing_locations(NumberChanger().visit(ast.parse(code1)))
# pprint(modded1)
modded2 = ast.parse(code2)
# pprint(modded2)
# print(modded1 == modded2)
# print("--------------")
# print(ast.unparse(modded1))
# print(ast.unparse(modded2))

# pprint(
#     ast.parse(
#         """
# return dark_star_templates.TemplateResponse("{template_path}", locals())
# """
#     )
# )
# code = '''
# print('')
# """adfa
# fadf
# a
# fadf
# ad
# """
# '''
# pprint(ast.parse(code))

code = """


# methods="GET, POST" name="this is my name"


r = request
"""
g = tokenize(BytesIO(code.strip().encode("utf-8")).readline)


for toknum, tokval, (srow, scol), *_ in g:
    if toknum == COMMENT:
        print(tokval, srow)
        for s in split(tokval):
            print(s)

pprint(ast.parse(code))
