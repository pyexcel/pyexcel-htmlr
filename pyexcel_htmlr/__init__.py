"""
    pyexcel_htmlr
    ~~~~~~~~~~~~~~~~~~~
    Read html table using messytables
    :copyright: (c) 2015-2017 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
from ._version import __version__, __author__  # flake8: noqa
from pyexcel_io.plugins import IOPluginInfoChain
from pyexcel_io.io import get_data as read_data, isstream

__FILE_TYPE__ = 'html'
IOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path='htmlr.HtmlPage',
    file_types=[__FILE_TYPE__],
    stream_type='text'
)


def get_data(afile, file_type=None, **keywords):
    """standalone module function for reading module supported file type"""
    if isstream(afile) and file_type is None:
        file_type = __FILE_TYPE__
    return read_data(afile, file_type=file_type, **keywords)
