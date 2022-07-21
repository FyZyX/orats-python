Notes
=====

The ``__call__`` method of ``Endpoint`` objects knows the response type, but
it is not accessible at runtime. Better solutions exist for Python 3.8+, but
the current implementation simply stores a reference to the response type in
each ``Endpoint`` subclass.
* https://stackoverflow.com/questions/72149212/how-to-get-generic-types-of-subclass-in-python
* https://stackoverflow.com/questions/69994838/get-generic-substituted-type
