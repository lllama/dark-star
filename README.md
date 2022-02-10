# Dark Star

Dark Star is a web framework that provides filesystem routing for
[Starlette](https://starlette.io) and first-class support for server-side rendering.

Dark Star routes are defined by their filesystem path and both the route's
backend code and template are contained in the first page.

## Motivation

Dark Star aims to provide an easy way to create web applications using the
[HATEOAS](https://htmx.org/essays/hateoas/) and
[HDA](https://htmx.org/essays/hypermedia-driven-applications/) philosophies
favoured by [htmx](https://htmx.org). It also aims to reduce the boilerplate
code normally needed when creating web apps. In particular, it looks to reduce
the need of having a separate files for view functions and templates. It tries
to embrace [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/)
by putting the view function code and template in the same file, and having the
file's path be the route used by Starlette to access the code.
