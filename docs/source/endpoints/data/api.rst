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
:class:`~orats.constructs.api.data.request.DataApiRequest`. These requests can be
passed to the corresponding **endpoint** object, which is a subclass of type
:class:`~orats.endpoints.data.DataApiEndpoint`.

.. automodule:: orats.endpoints.data.api
   :special-members: __init__, __call__
   :members:

.. _Data API: https://docs.orats.io/datav2-api-guide/data.html#data-api
.. _Tickers: https://docs.orats.io/datav2-api-guide/data.html#tickers
.. _Strikes: https://docs.orats.io/datav2-api-guide/data.html#strikes
.. _Strikes History: https://docs.orats.io/datav2-api-guide/data.html#strikes-history
.. _Strikes by Options: https://docs.orats.io/datav2-api-guide/data.html#strikes-by-options
.. _Strikes History by Options: https://docs.orats.io/datav2-api-guide/data.html#strikes-history-by-options
.. _Monies: https://docs.orats.io/datav2-api-guide/data.html#monies
.. _Monies History: https://docs.orats.io/datav2-api-guide/data.html#monies-history
.. _Summaries: https://docs.orats.io/datav2-api-guide/data.html#smv-summaries
.. _Summaries History: https://docs.orats.io/datav2-api-guide/data.html#summaries-history
.. _Core Data: https://docs.orats.io/datav2-api-guide/data.html#core-data
.. _Core Data History: https://docs.orats.io/datav2-api-guide/data.html#core-data-history
.. _Daily Price: https://docs.orats.io/datav2-api-guide/data.html#daily-price
.. _Historical Volatility: https://docs.orats.io/datav2-api-guide/data.html#historical-volatility
.. _Dividend History: https://docs.orats.io/datav2-api-guide/data.html#dividend-history
.. _Earnings History: https://docs.orats.io/datav2-api-guide/data.html#earnings-history
.. _Stock Split History: https://docs.orats.io/datav2-api-guide/data.html#stock-split-history
.. _IV Rank: https://docs.orats.io/datav2-api-guide/data.html#iv-rank
.. _IV Rank History: https://docs.orats.io/datav2-api-guide/data.html#iv-rank-history
