#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover UserService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class UserServiceTestV201002(unittest.TestCase):

  """Unittest suite for UserService using v201002."""

  SERVER_V201002 = SERVER
  VERSION_V201002 = 'v201002'
  client.debug = False
  service = None
  user1 = None
  user2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserService(
          self.__class__.SERVER_V201002, self.__class__.VERSION_V201002,
          HTTP_PROXY)

  def testGetUser(self):
    """Test whether we can fetch an existing user."""
    if not self.__class__.user1:
      self.testGetUsersByFilter()
    self.assert_(isinstance(self.__class__.service.GetUser(
        self.__class__.user1['id']), tuple))

  def testGetUsersByFilter(self):
    """Test whether we can fetch a list of existing users that match given
    filter."""
    filter = {'text': 'ORDER BY name LIMIT 500'}
    users = self.__class__.service.GetUsersByFilter(filter)
    sales = []
    traffickers = []
    admins = []
    for user in users[0]['results']:
      if user['roleName'] in ('Salesperson',):
        sales.append(user)
      elif user['roleName'] in ('Trafficker',):
        traffickers.append(user)
      elif user['roleName'] in ('Administrator',):
        admins.append(user)
    self.__class__.user1 = sales[0]
    self.__class__.user2 = traffickers[0]
    self.assert_(isinstance(users, tuple))

  def testPerformUserAction(self):
    """Test whether we can deactivate a user."""
    if not self.__class__.user1:
      self.testGetUsersByFilter()
    action = {'type': 'DeactivateUsers'}
    filter = {'text': 'WHERE id = \'%s\'' % self.__class__.user1['id']}
    self.assert_(isinstance(
        self.__class__.service.PerformUserAction(action, filter), tuple))

  def testUpdateUser(self):
    """Test whether we can update a user."""
    if not self.__class__.user1:
      self.testGetUsersByFilter()
    locale = 'fr_FR'
    self.__class__.user1['preferredLocale'] = locale
    user = self.__class__.service.UpdateUser(self.__class__.user1)
    self.assert_(isinstance(user, tuple))
    self.assertEqual(user[0]['preferredLocale'], locale)

  def testUpdateUsers(self):
    """Test whether we can update a list of users."""
    if not self.__class__.user1 or not self.__class__.user2:
      self.testGetUsersByFilter()
    locale = 'fr_FR'
    self.__class__.user1['preferredLocale'] = locale
    self.__class__.user2['preferredLocale'] = locale
    users = self.__class__.service.UpdateUsers([self.__class__.user1,
                                                self.__class__.user2])
    self.assert_(isinstance(users, tuple))
    for user in users:
      self.assertEqual(user['preferredLocale'], locale)


def makeTestSuiteV201002():
  """Set up test suite using v201002.

  Returns:
    TestSuite test suite using v201002.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserServiceTestV201002))
  return suite


if __name__ == '__main__':
  suite_v201002 = makeTestSuiteV201002()
  alltests = unittest.TestSuite([suite_v201002])
  unittest.main(defaultTest='alltests')
