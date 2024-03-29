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

"""Interface for generating authentication token to access Google Account."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import urllib

from adspygoogle.common.Errors import AuthTokenError


class AuthToken(object):

  """Fetches authentication token.

  Responsible for generating the authentication token to access Google Account,
  https://www.google.com/accounts/NewAccount. The token is fetched via the
  ClientLogin API, http://code.google.com/apis/accounts/.
  """

  def __init__(self, email, password, service, lib_sig, proxy):
    """Inits AuthToken.

    Args:
      email: str Login email of the Google Account.
      password: str Login password of the Google Account.
      service: str Name of the Google service for which to authorize access.
      lib_sig: str Client library signature.
      proxy: str HTTP proxy to use.
    """
    self.__email = email
    self.__password = password
    self.__account_type = 'GOOGLE'
    self.__service = service
    self.__source = 'Google-%s' % lib_sig
    self.__proxy = proxy
    self.__sid = ''
    self.__lsid = ''
    self.__auth = ''

    self.__Login()

  def __Login(self):
    """Fetch Auth token and SID, LSID cookies from Google Account auth."""
    if self.__proxy: os.environ['http_proxy'] = self.__proxy
    url = 'https://www.google.com/accounts/ClientLogin'
    data = [('Email', self.__email),
            ('Passwd', self.__password),
            ('accountType', self.__account_type),
            ('service', self.__service),
            ('source', self.__source)]
    try:
      fh = urllib.urlopen(url, urllib.urlencode(data))
      try:
        tag, msg = fh.readline().split('=')
        if tag in ('SID', 'LSID', 'Auth'):
          self.__sid = msg.strip()
          self.__lsid = fh.readline().split('=')[1].strip()
          self.__auth = fh.readline().split('=')[1].strip()
        elif tag in ('Error',):
          raise AuthTokenError(msg.strip())
        elif tag in ('CaptchaToken',):
          raise AuthTokenError('Captcha token is %s' % msg.strip())
        else:
          raise AuthTokenError(msg.strip())
      finally:
        fh.close()
    except IOError, e:
      raise AuthTokenError(e)

  def GetSidToken(self):
    """Return SID cookie.

    Returns:
      str SID cookie.
    """
    return self.__sid

  def GetLsidToken(self):
    """Return LSID cookie.

    Returns:
      str LSDI cookie.
    """
    return self.__lsid

  def GetAuthToken(self):
    """Return Auth authentication token.

    Returns:
      str Auth authentication token.
    """
    return self.__auth
