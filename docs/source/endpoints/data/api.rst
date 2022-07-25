Data API
========

A **Data API Endpoint** handles a **Data API Request** and relays the **Data API Response**.

.. note::
   Historical resource counterparts (e.g. ``hist/<resource>``) do **not**
   have corresponding low-level constructs. Instead, the base constructs accept
   an optional ``trade_date`` argument that, if specified, will automatically
   direct to the proper historical resource endpoint. While this implementation
   goes against a core :ref:`design goal <design goals>`, it simplifies the
   architecture to a significant enough degree that it is ultimately justifiable.

A user is expected to create a **request** object from one of the subclasses of
:class:`~orats.endpoints.data.request.DataApiRequest`. These requests can be
passed to the corresponding **endpoint** object, which is a subclass of type
:class:`~orats.endpoints.data.endpoints.DataApiEndpoint`.

.. automodule:: orats.endpoints.data.api
   :special-members: __init__, __call__
   :members:
