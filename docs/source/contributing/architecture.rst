Architecture
============

Design Goals
------------

* Layered constructs
* Low-level constructs correspond as closely as possible to the actual API
* High-level constructs compose low-level abstractions to satisfy common use cases

API Constructs
--------------

These are the lowest level (**Level 0**) constructs.
At this level, each construct corresponds to a specific API resource.

.. note::
   Historical resource counterparts (e.g. ``hist/<resource>``) do **not**
   have corresponding low-level constructs. Instead, the base constructs accept
   an optional ``trade_date`` argument that, if specified, will automatically
   direct to the proper historical resource endpoint. While this implementation
   goes against a core design goal, it simplifies the architecture to a significant
   enough degree that it is ultimately justifiable.

Industry Constructs
-------------------

This is the first level (**Level 1**) of abstract constructs.
Level 0 constructs are composed to create Level 1 constructs.

At this level, constructs are meant to correspond with industry standard concepts.

Application Constructs
----------------------

This is the second level (**Level 2**) of abstract constructs.
Both Level 0 and Level 1 constructs are composed to create Level 2 constructs.

These constructs are meant to specialize to user-specific use case.
This library may provide some essential application constructs, but users are
encouraged to follow this design philosophy in their own implementations.
You can :ref:`create your own construct <custom constructs>` to take advantage
of the features of this library.

Custom Constructs
-----------------
TODO
