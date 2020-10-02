"""
    pyexcel_htmlr.htmlr
    ~~~~~~~~~~~~~~~~~~~
    html table reader using messytables

    :copyright: (c) 2015-2020 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
import html5lib
import xml.etree.ElementTree as etree

import codecs
from pyexcel_io.sheet import NamedContent
from pyexcel_io._compact import OrderedDict
import pyexcel_io.service as service

from pyexcel_io.plugin_api.abstract_sheet import ISheet
from pyexcel_io.plugin_api.abstract_reader import IReader

ALL_TABLE_COLUMNS = './/*[name()="td" or name()="th"]'


class HtmlTable(ISheet):
    def __init__(self, sheet, auto_detect_int=True,
                 auto_detect_float=True,
                 auto_detect_datetime=True,
                 **keywords):
        self._native_sheet = sheet
        self.__auto_detect_int = auto_detect_int
        self.__auto_detect_float = auto_detect_float
        self.__auto_detect_datetime = auto_detect_datetime
        self.__xml_table = self._native_sheet.payload
        self.__column_span = {}

    @property
    def name(self):
        return self._native_sheet.name

    def row_iterator(self):
        for element in self._native_sheet.payload.xpath('.//tr'):
            if self.__xml_table in element.xpath("./ancestor::table[1]"):
                yield element

    def column_iterator(self, row):
        index = 0
        for element in row.xpath(ALL_TABLE_COLUMNS):
            # generate '' due to previous rowspan
            while index in self.__column_span:
                # and keep generating '' if next index is in the list
                self.__column_span[index] -= 1
                if self.__column_span[index] == 0:
                    del self.__column_span[index]
                yield ''
                index += 1

            cell_text = text_from_element(element)
            yield self.__convert_cell(cell_text)
            row_span = get_attribute('colspan', element)
            col_span = get_attribute('rowspan', element)
            if row_span > 1:
                # generate '' due to colspan
                if col_span > 1:
                    for offset in range(row_span):
                        if offset > 0:
                            # for next cell, give full col span
                            self.__column_span[index+offset] = col_span
                        else:
                            # for current cell, give -1 because it has been
                            # yielded
                            self.__column_span[index+offset] = col_span - 1
                else:
                    # no col span found, so just repeat in the same row
                    for _ in range(row_span-1):
                        yield ''
                        index += 1
            else:
                if col_span > 1:
                    self.__column_span[index] = col_span - 1
            # next index
            index += 1

    def __convert_cell(self, cell_text):
        ret = None
        if self.__auto_detect_int:
            ret = service.detect_int_value(cell_text)
        if ret is None and self.__auto_detect_float:
            ret = service.detect_float_value(cell_text)
            shall_we_ignore_the_conversion = (
                (ret in [float('inf'), float('-inf')]) and
                self.__ignore_infinity
            )
            if shall_we_ignore_the_conversion:
                ret = None
        if ret is None and self.__auto_detect_datetime:
            ret = service.detect_date_value(cell_text)
        if ret is None:
            ret = cell_text
        return ret


class HtmlPageInContent(IReader):
    def __init__(self, file_content, file_type, **keywords):
        self._keywords = keywords
        self.content_array = list(HtmlPageInContent.parse_html(file_content))

    def read_sheet(self, native_sheet_index):
        native_sheet = self.content_array[native_sheet_index]
        sheet = HtmlTable(native_sheet, **self._keywords)
        return sheet

    @staticmethod
    def parse_html(content):
        root = fromstring(content)
        for index, table in enumerate(root.xpath('//table'), 1):
            name = 'Table %s' % index
            yield NamedContent(name, table)

    def close(self):
        pass


class HtmlPageInStream(HtmlPageInContent):
    def __init__(self, file_stream, file_type, **keywords):
        file_stream.seek(0)
        file_content = file_stream.read()
        super().__init__(file_content, file_type, **keywords)


class HtmlPageInFile(HtmlPageInContent):
    def __init__(self, file_name, file_type, **keywords):
        self.file_handle = codecs.open(file_name, 'r')
        file_content = self.file_handle.read()
        super().__init__(file_content, file_type, **keywords)

    def close(self):
        if self.file_handle:
            self.file_handle.close()


def fromstring(s):
    tb = html5lib.getTreeBuilder("lxml", implementation=etree)
    p = html5lib.HTMLParser(tb, namespaceHTMLElements=False)
    return p.parse(s)


def text_from_element(elem):
    builder = []
    for x in elem.iter():
        if is_invisible_text(x):
            cell_str = x.tail or ''  # handle None values.
        else:
            cell_str = (x.text or '') + (x.tail or '')
        cell_str = cell_str.replace('\n', ' ').strip()
        if x.tag == 'br' or x.tag == 'p':
            cell_str = '\n' + cell_str
        builder.append(cell_str)
    return ''.join(builder).strip()


def is_invisible_text(elem):
    flag = False
    if elem.tag == "span":
        if 'style' in elem.attrib:
            if 'display:none' in elem.attrib['style']:
                flag = True

    return flag


def get_attribute(tag, element):
    try:
        return int(element.attrib.get(tag, 1))
    except ValueError:
        return 1
