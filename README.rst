fesenjoon
===========

Documentation_ -- GitHub_ 


A simple package

.. code-block:: python

    import fesenjoon

    drive = fesenjoon.Drive()
    # NOTE: URI params must be strings not integers

    gist_uri = 'https://api.github.com/gists{/gist_id}'
    t = URITemplate(gist_uri)
    print(t.expand(gist_id='123456'))
    # => https://api.github.com/users/sigmavirus24/gists/123456

    # or
    print(expand(gist_uri, gist_id='123456'))

    # also
    t.expand({'gist_id': '123456'})
    print(expand(gist_uri, {'gist_id': '123456'}))

Where it might be useful to have a class

.. code-block:: python

    from fesenjoon import Drive
    drive = Drive()


When the module containing this class is loaded, ``GitHubUser.url`` is
evaluated and so the template is created once. It's often hard to notice in
Python, but object creation can consume a great deal of time and so can the
``re`` module which uritemplate relies on. Constructing the object once should
reduce the amount of time your code takes to run.

Installing
----------

::

    pip install fesenjoon

License
-------

GPL license_


.. _Documentation: https://fesenjoon.readthedocs.io/
.. _GitHub: https://github.com/mohsenhariri/fesenjoon
.. _license: https://github.com/mohsenhariri/fesenjoon/blob/main/LICENSE