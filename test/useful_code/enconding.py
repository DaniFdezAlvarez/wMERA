# coding=utf-8
__author__ = 'Dani'

import unicodedata

from wmera.utils import rel_path_to_file


print unicodedata.normalize('NFKD', u"Uñä çôsá qüè Ãencòntré¡¿").encode('utf-8', 'ignore')
print unicodedata.normalize('NFC', u"Uña çôsá qüè Ãencòntré¡¿").encode('utf-8', 'ignore')
print unicodedata.normalize('NFD', u"Uñä çôsá qüè Ãencòntré¡¿").encode('ascii', 'ignore')
print unicodedata.normalize('NFD', u"Uñä çôsá qüè Ãencòntré¡¿").encode('ascii', 'ignore')
# print unicodedata.normalize('NFD', unicode("Uñä çôsá qüè Ãencòntré¡¿")).encode('ascii', 'ignore')  # error
print unicodedata.normalize('NFKC', u"Uña çôsá qüè Ãencòntré¡¿").encode('ascii', 'ignore')

