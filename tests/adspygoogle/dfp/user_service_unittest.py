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

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import client


class UserServiceTestV201004(unittest.TestCase):

  """Unittest suite for UserService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  user1 = None
  user2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllRoles(self):
    """Test whether we can fetch all roles."""
    self.assert_(isinstance(self.__class__.service.GetAllRoles(), tuple))

  def testGetUser(self):
    """Test whether we can fetch an existing user."""
    if not self.__class__.user1:
      self.testGetUsersByStatement()
    self.assert_(isinstance(self.__class__.service.GetUser(
        self.__class__.user1['id']), tuple))

  def testGetUsersByStatement(self):
    """Test whether we can fetch a list of existing users that match given
    statement."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    users = self.__class__.service.GetUsersByStatement(filter_statement)
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
    filter_statement = {'query': 'WHERE id = \'%s\''
                        % self.__class__.user1['id']}
    self.assert_(isinstance(
        self.__class__.service.PerformUserAction(action, filter_statement),
        tuple))

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


class UserServiceTestV201010(unittest.TestCase):

  """Unittest suite for UserService using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  service = None
  user1 = None
  user2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllRoles(self):
    """Test whether we can fetch all roles."""
    self.assert_(isinstance(self.__class__.service.GetAllRoles(), tuple))

  def testGetUser(self):
    """Test whether we can fetch an existing user."""
    if not self.__class__.user1:
      self.testGetUsersByStatement()
    self.assert_(isinstance(self.__class__.service.GetUser(
        self.__class__.user1['id']), tuple))

  def testGetUsersByStatement(self):
    """Test whether we can fetch a list of existing users that match given
    statement."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    users = self.__class__.service.GetUsersByStatement(filter_statement)
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
    filter_statement = {'query': 'WHERE id = \'%s\''
                        % self.__class__.user1['id']}
    self.assert_(isinstance(
        self.__class__.service.PerformUserAction(action, filter_statement),
        tuple))

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


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserServiceTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserServiceTestV201010))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010])
  unittest.main(defaultTest='alltests')
