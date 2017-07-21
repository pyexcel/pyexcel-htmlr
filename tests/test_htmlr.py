import os
from nose.tools import eq_
import pyexcel as p


def test_htmlr():
    sheet = p.Sheet([[1]])
    sheet2 = p.Sheet()
    sheet2.html = sheet.html
    assert sheet2[0, 0] == 1


def test_html_html():
    sheet = p.get_sheet(file_name=get_fixture('html.html'))
    eq_(sheet.number_of_rows(), 200)
    eq_(sheet[0, 0], 'HDI Rank')
    eq_(sheet[0, 1], 'Country')
    eq_(sheet[0, 4], 2010)


def test_table_names():
    book = p.get_book(file_name=get_fixture('html.html'))
    eq_(book[0].name, 'Table 1')
    eq_(book[1].name, 'Table 2')
    eq_(book[2].name, 'Table 3')


def test_invisible_text_html():
    sheet = p.get_sheet(file_name=get_fixture('invisible_text.html'))
    eq_(sheet.number_of_rows(), 4)
    eq_(sheet[1, 5], '1 July 1879')


def test_complex_html():
    book = p.get_book(file_name=get_fixture('complex.html'))
    eq_(book[0].number_of_rows(), 1)
    eq_(book[0][0, 0], 'headfootbody')


def test_span():
    sheet = p.get_sheet(file_name=get_fixture('rowcolspan.html'))
    print(sheet)
    eq_(sheet[0, 0], '05')
    eq_(sheet[2, 0], 25)
    eq_(sheet[2, 4], 29)
    eq_(sheet[3, 0], '')
    eq_(sheet[3, 1], 36)
    eq_(sheet[3, 4], 39)
    eq_(sheet[6, 1], 66)
    eq_(sheet[7, 4], 79)
    eq_(sheet[8, 4], 89)


def get_fixture(file_name):
    return os.path.join("tests", "fixtures", file_name)
