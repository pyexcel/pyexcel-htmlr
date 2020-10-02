================================================================================
pyexcel-htmlr - Let you focus on data, instead of html format
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-htmlr.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-htmlr

.. image:: https://codecov.io/gh/pyexcel/pyexcel-htmlr/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel-htmlr

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby


Known constraints
==================

Fonts, colors and charts are not supported.

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


Usage
================================================================================

As a standalone library
--------------------------------------------------------------------------------

.. testcode::
   :hide:

    >>> import os
    >>> import sys
	>>> import pyexcel as pe
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import BytesIO as StringIO
    >>> PY2 = sys.version_info[0] == 2
    >>> if PY2 and sys.version_info[1] < 7:
    ...      from ordereddict import OrderedDict
    ... else:
    ...     from collections import OrderedDict
    >>> 
    >>> data = OrderedDict() # from collections import OrderedDict
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
    >>> book = pe.get_book(bookdict=data)
	>>> book.save_as("your_file.html")

Read from an html file
********************************************************************************

Here's the sample code:

.. code-block:: python

    >>> from pyexcel_htmlr import get_data
    >>> data = get_data("your_file.html")
    >>> import json
    >>> print(json.dumps(data))
    {"Table 1": [[1, 2, 3], [4, 5, 6]], "Table 2": [["row 1", "row 2", "row 3"]]}




Read from an html from memory
********************************************************************************

Continue from previous example:

.. code-block:: python

    >>> # This is just an illustration
    >>> # In reality, you might deal with html file upload
    >>> # where you will read from requests.FILES['YOUR_HTML_FILE']
    >>> with open('your_file.html', 'r') as html_file:
    ...    io = StringIO(html_file.read().encode())
    ...    data = get_data(io)
    >>> print(json.dumps(data))
    {"Table 1": [[1, 2, 3], [4, 5, 6]], "Table 2": [["row 1", "row 2", "row 3"]]}


Pagination feature
********************************************************************************



Let's assume the following file is a huge html file:

.. code-block:: python

   >>> huge_data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33],
   ...     [4, 24, 34],
   ...     [5, 25, 35],
   ...     [6, 26, 36]
   ... ]
   >>> sheetx = {
   ...     "huge": huge_data
   ... }
   >>> pe.save_book_as(dest_file_name="huge_file.html", bookdict=sheetx)

And let's pretend to read partial data:

.. code-block:: python

   >>> partial_data = get_data("huge_file.html", start_row=2, row_limit=3)
   >>> print(json.dumps(partial_data))
   {"Table 1": [[3, 23, 33], [4, 24, 34], [5, 25, 35]]}

And you could as well do the same for columns:

.. code-block:: python

   >>> partial_data = get_data("huge_file.html", start_column=1, column_limit=2)
   >>> print(json.dumps(partial_data))
   {"Table 1": [[21, 31], [22, 32], [23, 33], [24, 34], [25, 35], [26, 36]]}

Obvious, you could do both at the same time:

.. code-block:: python

   >>> partial_data = get_data("huge_file.html",
   ...     start_row=2, row_limit=3,
   ...     start_column=1, column_limit=2)
   >>> print(json.dumps(partial_data))
   {"Table 1": [[23, 33], [24, 34], [25, 35]]}

.. testcode::
   :hide:

   >>> os.unlink("huge_file.html")


As a pyexcel plugin
--------------------------------------------------------------------------------

No longer, explicit import is needed since pyexcel version 0.2.2. Instead,
this library is auto-loaded. So if you want to read data in html format,
installing it is enough.


Reading from an html file
********************************************************************************

Here is the sample code:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_book(file_name="your_file.html")
    >>> sheet
    Table 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Table 2:
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+




Reading from a IO instance
********************************************************************************

You got to wrap the binary content with stream to get html working:

.. code-block:: python

    >>> # This is just an illustration
    >>> # In reality, you might deal with html file upload
    >>> # where you will read from requests.FILES['YOUR_HTML_FILE']
    >>> htmlfile = "your_file.html"
    >>> with open(htmlfile, "rb") as f:
    ...     content = f.read()
    ...     r = pe.get_book(file_type="html", file_content=content)
    ...     print(r)
    ...
    Table 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Table 2:
    +-------+-------+-------+
    | row 1 | row 2 | row 3 |
    +-------+-------+-------+




License
================================================================================

New BSD License

Developer guide
==================

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



.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.html")
