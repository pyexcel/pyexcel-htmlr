================================================================================
pyexcel-htmlr - Let you focus on data, instead of file formats
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-htmlr.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-htmlr

.. image:: https://codecov.io/gh/pyexcel/pyexcel-htmlr/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel-htmlr

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby

.. image:: https://readthedocs.org/projects/pyexcel-htmlr/badge/?version=latest
   :target: http://pyexcel-htmlr.readthedocs.org/en/latest/

Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please `support me on patreon <https://www.patreon.com/bePatron?u=5537627>`_ to
maintain the project and develop it further.

If you are an individual, you are welcome to support me too on patreon and for however long
you feel like to. As a patreon, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.



Introduction
================================================================================
**pyexcel-htmlr** does read tables in html file as excel data. It is inspared by `messytables'`_ html capability
and brings pyexcel developers the html reading capability. In pyexcel family,
pyexcel developers can cherry pick the plugins for your needs.

.. _messytables': https://github.com/okfn/messytables




Installation
================================================================================
You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel-htmlr


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel-htmlr.git
    $ cd pyexcel-htmlr
    $ python setup.py install



Development guide
================================================================================

Development steps for code changes

#. git clone https://github.com/pyexcel/pyexcel-htmlr.git
#. cd pyexcel-htmlr

Upgrade your setup tools and pip. They are needed for development and testing only:

#. pip install --upgrade setuptools pip

Then install relevant development requirements:

#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt

Once you have finished your changes, please provide test case(s), relevant documentation
and update CHANGELOG.rst.

.. note::

    As to rnd_requirements.txt, usually, it is created when a dependent
	library is not released. Once the dependecy is installed
	(will be released), the future
	version of the dependency in the requirements.txt will be valid.


How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make

On Windows systems, please issue this command::

    > test.bat

How to update test environment and update documentation
---------------------------------------------------------

Additional steps are required:

#. pip install moban
#. git clone https://github.com/pyexcel/pyexcel-commons.git commons
#. make your changes in `.moban.d` directory, then issue command `moban`

What is pyexcel-commons
---------------------------------

Many information that are shared across pyexcel projects, such as: this developer guide, license info, etc. are stored in `pyexcel-commons` project.

What is .moban.d
---------------------------------

`.moban.d` stores the specific meta data for the library.

Acceptance criteria
-------------------

#. Has Test cases written
#. Has all code lines tested
#. Passes all Travis CI builds
#. Has fair amount of documentation if your change is complex
#. Agree on NEW BSD License for your contribution




License
================================================================================

New BSD License
