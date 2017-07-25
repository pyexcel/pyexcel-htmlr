"""
    pyexcel_odsr.htmlr
    ~~~~~~~~~~~~~~~~~~~
    html table reader using messytables

    :copyright: (c) 2015-2017 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
import re

import html5lib
import xml.etree.ElementTree as etree

import datetime
from pyexcel_io.book import BookReader
from pyexcel_io.sheet import SheetReader, NamedContent
from pyexcel_io._compact import OrderedDict


ALL_TABLE_COLUMNS = './/*[name()="td" or name()="th"]'


class HtmlTable(SheetReader):
    def __init__(self, sheet, auto_detect_int=True,
                 auto_detect_float=True,
                 auto_detect_datetime=True,
                 **keywords):
        SheetReader.__init__(self, sheet, **keywords)
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
            ret = _detect_int_value(cell_text)
        if ret is None and self.__auto_detect_float:
            ret = _detect_float_value(cell_text)
            shall_we_ignore_the_conversion = (
                (ret in [float('inf'), float('-inf')]) and
                self.__ignore_infinity
            )
            if shall_we_ignore_the_conversion:
                ret = None
        if ret is None and self.__auto_detect_datetime:
            ret = _detect_date_value(cell_text)
        if ret is None:
            ret = cell_text
        return ret


class HtmlPage(BookReader):
    def __init__(self):
        BookReader.__init__(self)
        self._file_handle = None

    def open(self, file_name, **keywords):
        BookReader.open(self, file_name, **keywords)
        self._load_from_file()

    def open_stream(self, file_stream, **keywords):
        BookReader.open_stream(self, file_stream, **keywords)
        self._load_from_memory()

    def read_all(self):
        result = OrderedDict()
        for sheet in self._native_book:
            result.update(self.read_sheet(sheet))
        return result

    def read_sheet(self, native_sheet):
        sheet = HtmlTable(native_sheet, **self._keywords)
        return {sheet.name: sheet.to_array()}

    def _load_from_file(self):
        self._file_handle = open(self._file_name, 'r')
        self._native_book = self._parse_html(self._file_handle)

    def _load_from_memory(self):
        self._native_book = self._parse_html(self._file_stream)

    def _parse_html(self, file_handler):
        root = fromstring(file_handler.read())
        for index, table in enumerate(root.xpath('//table'), 1):
            name = 'Table %s' % index
            yield NamedContent(name, table)

    def close(self):
        if self._file_handle:
            self._file_handle.close()


def fromstring(s):
    tb = html5lib.getTreeBuilder("lxml", implementation=etree)
    p = html5lib.HTMLParser(tb, namespaceHTMLElements=False)
    return p.parse(s)


def _detect_date_value(csv_cell_text):
    """
    Read the date formats that were written by csv.writer
    """
    ret = None
    try:
        if len(csv_cell_text) == 10:
            ret = datetime.datetime.strptime(
                csv_cell_text,
                "%Y-%m-%d")
            ret = ret.date()
        elif len(csv_cell_text) == 19:
            ret = datetime.datetime.strptime(
                csv_cell_text,
                "%Y-%m-%d %H:%M:%S")
        elif len(csv_cell_text) > 19:
            ret = datetime.datetime.strptime(
                csv_cell_text[0:26],
                "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        pass
    return ret


def _detect_float_value(csv_cell_text):
    try:
        should_we_skip_it = (csv_cell_text.startswith('0') and
                             csv_cell_text.startswith('0.') is False)
        if should_we_skip_it:
            # do not convert if a number starts with 0
            # e.g. 014325
            return None
        else:
            return float(csv_cell_text)
    except ValueError:
        return None


def _detect_int_value(csv_cell_text):
    if csv_cell_text.startswith('0') and len(csv_cell_text) > 1:
        return None
    try:
        return int(csv_cell_text)
    except ValueError:
        pattern = '([0-9]+,)*[0-9]+$'
        if re.match(pattern, csv_cell_text):
            integer_string = csv_cell_text.replace(',', '')
            return int(integer_string)
        else:
            return None


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
