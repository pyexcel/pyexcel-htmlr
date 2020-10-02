"""
    pyexcel_htmlr
    ~~~~~~~~~~~~~~~~~~~
    Read html table using messytables
    :copyright: (c) 2015-2017 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
from ._version import __version__, __author__  # noqa
from pyexcel_io.plugins import IOPluginInfoChainV2
from pyexcel_io.io import get_data as read_data, isstream

__FILE_TYPE__ = 'html'
IOPluginInfoChainV2(__name__).add_a_reader(
    relative_plugin_class_path='htmlr.HtmlPageInContent',
    locations=["content"],
    file_types=[__FILE_TYPE__, 'htm'],
    stream_type='text'
).add_a_reader(
    relative_plugin_class_path='htmlr.HtmlPageInStream',
    locations=["memory"],
    file_types=[__FILE_TYPE__, 'htm'],
    stream_type='text'
).add_a_reader(
    relative_plugin_class_path='htmlr.HtmlPageInFile',
    locations=["file"],
    file_types=[__FILE_TYPE__, 'htm'],
    stream_type='text'
)


def get_data(afile, file_type=None, **keywords):
    """standalone module function for reading module supported file type"""
    if isstream(afile) and file_type is None:
        file_type = __FILE_TYPE__
    return read_data(afile, file_type=file_type, **keywords)
