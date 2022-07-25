Getting Started
===============

Installation
------------

.. code-block:: shell

   $ pip install orats

Basic Usage
-----------

Direct API requests are particularly simple. For example, to access an endpoint from the
Data API, all you need is the following snippet.

.. code-block:: python

   from orats.endpoints.data import api, request as req

   data_api = api.DataApi(token="demo")
   request = req.TickersRequest(ticker="IBM")
   tickers = data_api.tickers(request)
   for ticker in tickers:
       assert isinstance(ticker, res.Ticker)

Have a look at the full list of available :ref:`API constructs <API Constructs>`.

.. note::

   You can also :ref:`set a default token <Setting a Default Token>` to avoid
   specifying your API token manually.

Setting a Default Token
-----------------------

If a token is not passed to the :class:`~orats.endpoints.data.api.DataApi` constructor,
the execution environment will be searched for a variable called ``ORATS_API_TOKEN``.
If not token is found in the environment, the ``demo`` token will be used.

.. warning::

   API tokens are sensitive! Avoid putting your token directly into source code.
   Use of the ``ORATS_API_TOKEN`` variable is a recommended best practice.

When the environment is set properly, you can instantiate objects without a token.

.. code-block:: python

   from orats.endpoints.data import api, request as req

   data_api = api.DataApi()
   request = req.DailyPriceRequest(tickers=("IBM", "RIVN"))
   prices = data_api.daily_price(request)

.. note::

   The ``demo`` token is very restrictive. If you are running to an :class:`~orats.errors.InsufficientPermissionsError`,
   make sure your token is available in the execution environment.
