# Dark Star

Dark Star is a web framework that combines [Starlette](https://starlette.io) and [htmx](https://htmx.org).

## Motivation

[htmx prefers HATEOAS](https://htmx.org/essays/hateoas/) as its application
architecture, and uses [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/)
to improve developer productivity. It also makes using web features such as
[Server-sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
and [Websockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) easy to use.

Starlette is an ASGI framework for Python that supports SSE and Websockets out
of the box and has been used to create a number of alternative frameworks.

Dark Star aims to provide an easy way to create web applications using the htmx
philosophy. It also aims to reduce the boilerplate code normally needed when
creating web apps. In particular, it looks to reduce the need of having a
separate files for view functions and templates. It tries to embrace Locality
of Behaviour by putting the view function code and template in the same file,
and having the file's path be the route used by Starlette to access the code.
