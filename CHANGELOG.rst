Change log
===========

0.5.1 - 20.10.2017
--------------------------------------------------------------------------------

added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include LICENSE file
   in MANIFEST.in, meaning LICENSE file will appear in the released tar ball.

0.5.0 - 30.08.2017
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. put dependency on pyexcel-io 0.5.0, which uses cStringIO instead of StringIO.
   Hence, there will be performance boost in handling files in memory.
#. version jumped because it will be easy to see pyexcel-htmlr depends on
   pyexcel-io v0.5.0

Relocated
********************************************************************************

#. type detection code is being relocated into pyexcel-io

0.0.1 - 26-07-2017
---------------------------

Initial release
