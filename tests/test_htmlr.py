import os

import pyexcel as p


def test_htmlr():
    sheet = p.Sheet([[1]])
    sheet2 = p.Sheet()
    x = sheet.html
    sheet2.html = x
    assert sheet2[0, 0] == 1


def test_html_html():
    sheet = p.get_sheet(file_name=get_fixture("html.html"))
    assert sheet.number_of_rows() == 200
    assert sheet[0, 0] == "HDI Rank"
    assert sheet[0, 1] == "Country"
    assert sheet[0, 4] == 2010


def test_table_names():
    book = p.get_book(file_name=get_fixture("html.html"))
    assert book[0].name == "Table 1"
    assert book[1].name == "Table 2"
    assert book[2].name == "Table 3"


def test_invisible_text_html():
    sheet = p.get_sheet(file_name=get_fixture("invisible_text.html"))
    assert sheet.number_of_rows() == 4
    assert sheet[1, 5] == "1 July 1879"


def test_complex_html():
    book = p.get_book(file_name=get_fixture("complex.html"))
    assert book[0].number_of_rows() == 1
    assert book[0][0, 0] == "headfootbody"


def test_span():
    sheet = p.get_sheet(file_name=get_fixture("rowcolspan.html"))
    print(sheet)
    assert sheet[0, 0] == "05"
    assert sheet[2, 0] == 25
    assert sheet[2, 4] == 29
    assert sheet[3, 0] == ""
    assert sheet[3, 1] == 36
    assert sheet[3, 4] == 39
    assert sheet[6, 1] == 66
    assert sheet[7, 4] == 79
    assert sheet[8, 4] == 89


def get_fixture(file_name):
    return os.path.join("tests", "fixtures", file_name)
