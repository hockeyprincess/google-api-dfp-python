#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Handy utility functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import codecs
import csv
import datetime
import htmlentitydefs
import os
import re
import sys
import traceback
from urlparse import urlparse
from urlparse import urlunparse

from adspygoogle.common import SanityCheck
from adspygoogle.common.AuthToken import AuthToken
from adspygoogle.common.Buffer import Buffer
from adspygoogle.common.Errors import Error


def ReadFile(f_path):
  """Load data from a given file.

  Args:
    f_path: str Absolute path to the file to read.

  Returns:
    str Data loaded from the file, None otherwise.
  """
  data = ''

  if f_path:
    fh = open(f_path, 'r')
    try:
      data = fh.read()
    finally:
      fh.close()
  return data


def GetDataFromCsvFile(lib_home, file_name):
  """Get data from CSV file, given name of the file from "data/".

  Args:
    lib_home: str Path to the directory where client library's home is.
    file_name: str File name.

  Returns:
    list Data from CSV file.
  """
  f_path = os.path.join(lib_home, 'data', file_name)
  rows = []
  for row in csv.reader(ReadFile(f_path).split('\n')):
    if row:
      rows.append(row)
  return rows[1:]


def PurgeLog(log):
  """Clear content of a given log file.

  If the file cannot be opened, Error is raised.

  Args:
    log: str Absolute path to a log file.
  """
  try:
    fh = open(log, 'w')
    try:
      fh.write('')
    finally:
      fh.close()
  except IOError, e:
    raise Error(e)


def GetErrorFromHtml(data):
  """Return error message from HTML page.

  Args:
    data: str HTML data.

  Returns:
    str Error message.
  """
  pattern = re.compile('\n')
  data = pattern.sub('', data)
  # Fetch error message.
  pattern = re.compile('<title>(.*)</title>|<TITLE>(.*)</TITLE>')
  msg = pattern.findall(data)
  if msg:
    for item in msg[0]:
      if item:
        msg = item
        # Cut unnecessary wording.
        pattern = re.compile('Error: |ERROR: ')
        msg = pattern.sub('', msg, count=1)
  else:
    pattern = re.compile('<body>(.*)</body>')
    msg = pattern.findall(data)
    if msg: msg = msg[0].rstrip('.')
  # Fetch detail for the error message
  pattern = re.compile(('<blockquote><H1>.*</H1>(.*)<p></blockquote>|'
                        '<H1>.*</H1>(.*)</BODY>'))
  msg_detail = pattern.findall(data)
  if isinstance(msg_detail, list) and msg_detail:
    for item in msg_detail[0]:
      if item: msg_detail = item
    msg_detail = msg_detail.strip('.')
    # Cut any HTML tags that appear in the message.
    pattern = re.compile('<.?H2>|<.?p>|<.?A.*>|<.?P.*>|<.?HR.*>')
    msg_detail = pattern.sub(' ', msg_detail).strip(' ')
    if msg_detail == msg: msg_detail = ''
  else:
    msg_detail = ''

  if msg:
    if not msg_detail: return '%s.' % msg
    return '%s. %s.' % (msg, msg_detail)
  else:
    # Check for non standard HTML content, with just the <body>.
    pattern = re.compile('<body>(.*)</body>')
    msg = pattern.findall(data)
    if msg: return msg[0]
  return ''


def IsHtml(data):
  """Return True if data is HTML, False otherwise.

  Args:
    data: str Data to check.

  Returns:
    bool True if data is HTML, False otherwise.
  """
  # Remove banners and XML header. Convert to lower case for easy search.
  data = ''.join(data.split('\n')).lower()
  pattern = re.compile('<html>.*?<body.*?>.*?</body>.*?</html>')
  if pattern.findall(data):
    return True
  else:
    return False


def DecodeNonASCIIText(text, encoding='utf-8'):
  """Decode a non-ASCII text into a unicode, using given encoding.

  A full list of supported encodings is available at
  http://docs.python.org/lib/standard-encodings.html. If unable to find given
  encoding, Error is raised.

  Args:
    text: str Text to encode.
    [optional]
    encoding: str Encoding format to use.

  Returns:
    tuple Decoded text with the text length, (text, len(text)).
  """
  if isinstance(text, unicode): return (text, len(text))

  dec_text = ''
  try:
    decoder = codecs.getdecoder(encoding)
    dec_text = decoder(text)
  except LookupError, e:
    msg = 'Unable to find \'%s\' encoding. %s.' % (encoding, e)
    raise Error(msg)
  except Exception, e:
    raise Error(e)
  return dec_text


def MakeTextXMLReady(text):
  """Convert given text into an XML ready text.

  XML ready text with all non-ASCII characters properly decoded.

  Args:
    text: str Text to convert.

  Returns:
    str Converted text.
  """
  dec_text = DecodeNonASCIIText(text)[0]
  items = []
  for char in dec_text:
    try:
      char = char.encode('ascii')
    except UnicodeEncodeError:
      # We have a non-ASCII character of type unicode. Convert it into an
      # XML-ready format.
      try:
        str(char)
        char.encode('utf-8')
      except UnicodeEncodeError:
        char = '%s;' % hex(ord(char)).replace('0x', '&#x')
    items.append(char)
  return ''.join(items)


def __ParseUrl(url):
  """Parse URL into components.

  Args:
    url: str URL to parse.
  """
  return urlparse(url)


def GetSchemeFromUrl(url):
  """Return scheme portion of the URL.

  Args:
    url: str URL to parse.
  """
  return __ParseUrl(url)[0]


def GetNetLocFromUrl(url):
  """Return netloc portion of the URL.

  Args:
    url: str URL to parse.

  Returns:
    str Netloc portion of the URL.
  """
  return __ParseUrl(url)[1]


def GetPathFromUrl(url):
  """Return path portion of the URL.

  Args:
    url: str URL to parse.

  Returns:
    str Path portion of the URL.
  """
  return __ParseUrl(url)[2]


def GetServerFromUrl(url):
  """Return reconstructed scheme and netloc portion of the URL.

  Args:
    url: str URL to parse.
  """
  return urlunparse((GetSchemeFromUrl(url), GetNetLocFromUrl(url), '', '', '',
                     ''))


def GetAuthToken(email, password, service, lib_sig):
  """Return an authentication token for Google Account.

  If an error occurs, AuthTokenError is raised.

  Args:
    email: str Google Account's login email.
    password: str Google Account's password.
    service: str Name of the Google service for which to authorize access.
    lib_sig: str Signature of the client library.

  Returns:
    str Authentication token for Google Account.
  """
  return AuthToken(email, password, service, lib_sig).GetAuthToken()


def GetCurrentFuncName():
  """Return current function/method name.

  Returns:
    str Current function/method name.
  """
  return sys._getframe(1).f_code.co_name


def UnLoadDictKeys(dct, keys_lst):
  """Return newly built dictionary with out the keys in keys_lst.

  Args:
    dct: dict Dictionary to unload keys from.
    keys_lst: list List of keys to unload from a dictionary.

  Returns:
    dict New dictionary with out given keys.
  """
  if not keys_lst: return dct
  SanityCheck.ValidateTypes(((dct, dict), (keys_lst, list)))

  new_dct = {}
  for key in dct:
    if key in keys_lst:
      continue
    new_dct[key] = dct[key]
  return new_dct

def CleanUpDict(dct):
  """Return newly built dictionary with out the keys that point to no values.

  Args:
    dct: dict Dictionary to clean up.

  Returns:
    dict New dictionary with out empty keys.
  """
  SanityCheck.ValidateTypes(((dct, dict),))

  new_dct = {}
  for key in dct:
    if dct[key]:
      new_dct[key] = dct[key]
  return new_dct


def BoolTypeConvert(bool_type):
  """Convert bool to local bool and vice versa.

  Args:
    bool_type: bool or str a type to convert (i.e. True<=>'y', False<=>'n',
               'true'=>True, 'false'=>False).

  Returns:
    bool or str converted type.
  """
  if isinstance(bool_type, bool):
    if bool_type:
      return 'y'
    else:
      return 'n'
  elif isinstance(bool_type, str):
    if bool_type == 'y' or bool_type.lower() == 'true':
      return True
    elif bool_type == 'n' or bool_type.lower() == 'false':
      return False


def LastStackTrace():
  """Fetch last stack traceback.

  Returns:
    str Last stack traceback.
  """
  # Temporarily redirect traceback from STDOUT into a buffer.
  trace_buf = Buffer()
  old_stdout = sys.stdout
  sys.stdout = trace_buf

  try:
    traceback.print_exc(file=sys.stdout)
  except AttributeError:
    # No exception for traceback exist.
    print ''

  # Restore STDOUT.
  sys.stdout = old_stdout
  return trace_buf.GetBufferAsStr().strip()


def HtmlUnescape(text):
  """Removes HTML or XML character references and entities from a text string.

  See http://effbot.org/zone/re-sub.htm#unescape-html.

  Args:
    text: str HTML (or XML) source text.

  Returns:
    str/unicode Plain text, as a Unicode string, if necessary.
  """
  def fixup(m):
    text = m.group(0)
    if text[:2] == "&#":
        # character reference
      try:
        if text[:3] == "&#x":
          return unichr(int(text[3:-1], 16))
        else:
          return unichr(int(text[2:-1]))
      except ValueError:
        pass
    else:
      # named entity
      try:
        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
      except KeyError:
        pass
    return text # leave as is
  return re.sub("&#?\w+;", fixup, text)


def HtmlEscape(text):
  """Escapes characters in a given text string.

  See http://wiki.python.org/moin/EscapingHtml.

  Args:
    text: str Text to HTML escape.

  Returns:
    str HTML escaped string.
  """
  html_escape_table = {
    '&': '&amp;',
    '"': '&quot;',
    '\'': '&apos;',
    '>': '&gt;',
    '>': '&lt;'
  }
  return ''.join(html_escape_table.get(char, char) for char in text)


def CsvEscape(text):
  """Escapes data entry for consistency with CSV format.

  The CSV format rules:
    - Fields with embedded commas must be enclosed within double-quote
      characters.
    - Fields with embedded double-quote characters must be enclosed within
      double-quote characters, and each of the embedded double-quote characters
      must be represented by a pair of double-quote characters.
    - Fields with embedded line breaks must be enclosed within double-quote
      characters.
    - Fields with leading or trailing spaces must be enclosed within
      double-quote characters.

  Args:
    text: str Data entry.

  Returns:
    str CSV encoded data entry.
  """
  if not text: return ''
  if text.find('"') > -1: text = text.replace('"', '""')
  if (text == '' or text.find(',') > -1 or text.find('"') > -1 or
      text.find('\n') > -1 or text.find('\r') > -1 or text[0] == ' ' or
      text[-1] == ' '):
    text = '"%s"' % text
  return text


def GetUniqueName():
  """Returns a unique value consisting of parts from datetime.datetime.now().

  Returns:
    str Unique name.
  """
  dt = datetime.datetime.now()
  return '%s%s%s%s%s%s%s' % (dt.year, dt.month, dt.day, dt.hour, dt.minute,
                             dt.second, dt.microsecond)
