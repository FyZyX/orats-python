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
