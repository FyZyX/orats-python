API Constructs
==============

These are the lowest level (**Level 0**) constructs.
At this level, each construct corresponds to a specific API resource.

.. note::
   Historical resource counterparts (e.g. ``hist/<resource>``) do **not**
   have corresponding low-level constructs. Instead, the base constructs accept
   an optional ``trade_date`` argument that, if specified, will automatically
   direct to the proper historical resource endpoint. While this implementation
   goes against a core :ref:`design goal <design goals>`, it simplifies the
   architecture to a significant enough degree that it is ultimately justifiable.

.. toctree::
   :maxdepth: 2

   data/request
   data/response

.. note:: While not considered constructs in their own right, this section also
   contains information about the :mod:`~orats.constructs.api.data.request` models,
   which are used with :mod:`~orats.endpoints.data` endpoints to generate the
   Level 0 constructs.

A user is expected to create a **request** object from one of the subclasses of
:class:`~orats.constructs.api.data.request.DataApiRequest`. These requests can be
passed to the corresponding **endpoint** object, which is a subclass of type
:class:`~orats.endpoints.data.DataApiEndpoint`.

