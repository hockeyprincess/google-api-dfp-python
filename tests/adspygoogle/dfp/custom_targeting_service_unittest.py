#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unit tests to cover CustomTargetingService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfp.DfpErrors import DfpApiError
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201101
from tests.adspygoogle.dfp import SERVER_V201103
from tests.adspygoogle.dfp import VERSION_V201101
from tests.adspygoogle.dfp import VERSION_V201103
from tests.adspygoogle.dfp import client


class CustomTargetingServiceTestV201101(unittest.TestCase):

  """Unittest suite for CustomTargetingService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  key1 = None
  key2 = None
  value1 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCustomTargetingService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateCustomTargetingKeys(self):
    """Test whether we can create custom targeting keys."""
    keys = [
        {
            'displayName': 'gender',
            'name': Utils.GetUniqueName(10),
            'type': 'PREDEFINED'
        },
        {
            'displayName': 'car model',
            'name': Utils.GetUniqueName(10),
            'type': 'FREEFORM'
        }
    ]
    try:
      keys = self.__class__.service.CreateCustomTargetingKeys(keys)
      self.__class__.key1 = keys[0]
      self.__class__.key2 = keys[1]
      self.assert_(isinstance(keys, tuple))
    except DfpApiError, e:
      if e.message.find('CustomTargetingError.KEY_COUNT_TOO_LARGE') > -1:
        self.testDeleteCustomTargetingKeys()
      else:
        raise e

  def testCreateCustomTargetingValues(self):
    """Test whether we can create custom targeting values."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()

    values = [
        {
          'customTargetingKeyId': self.__class__.key1['id'],
          'displayName': 'male',
          'name': Utils.GetUniqueName(40),
          'matchType': 'EXACT'
        },
        {
          'customTargetingKeyId': self.__class__.key1['id'],
          'displayName': 'female',
          'name': Utils.GetUniqueName(40),
          'matchType': 'EXACT'
        }
    ]
    try:
      values = self.__class__.service.CreateCustomTargetingValues(values)
      self.__class__.value1 = values[0]
      self.assert_(isinstance(values, tuple))
    except DfpApiError, e:
      if e.message.find('CustomTargetingError.VALUE_NAME_DUPLICATE') > -1:
        self.testDeleteCustomTargetingValues()
      else:
        raise e

  def testGetAllCustomTargetingKeys(self):
    """Test whether we can retrieve all custom targeting keys."""
    values = [{
        'key': 'type',
        'value': {
            'xsi_type': 'TextValue',
            'value': 'PREDEFINED'
        }
    }]
    filter_statement = {'query': 'WHERE type = :type LIMIT 500',
                        'values': values}
    self.assert_(isinstance(
        self.__class__.service.GetCustomTargetingKeysByStatement(
            filter_statement), tuple))

  def testGetAllCustomTargetingValues(self):
    """Test whether we can retrieve all custom targeting values."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()

    values = [{
        'key': 'keyId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': self.__class__.key1['id']
        }
    }]
    filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId '
                                 'LIMIT 500',
                        'values': values}
    self.assert_(isinstance(
        self.__class__.service.GetCustomTargetingValuesByStatement(
            filter_statement), tuple))

  def testUpdateCustomTargetingKeys(self):
    """Test whether we can update existing custom targeting keys."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()

    keys = [self.__class__.key1, self.__class__.key2]
    for key in keys:
      key['displayName'] += ' (Deprecated)'
    self.assert_(isinstance(
        self.__class__.service.UpdateCustomTargetingKeys(keys), tuple))

  def testUpdateCustomTargetingValues(self):
    """Test whether we can update existing custom targeting values."""
    if not self.__class__.value1:
      self.testCreateCustomTargetingValues()

    values = [self.__class__.value1]
    for value in values:
      value['displayName'] += ' (Deprecated)'
    self.assert_(isinstance(
        self.__class__.service.UpdateCustomTargetingValues(values), tuple))

  def testDeleteCustomTargetingKeys(self):
    """Test whether we can delete existing custom targeting keys."""
    action = {'type': 'DeleteCustomTargetingKeyAction'}
    filter_statement = {'query': 'LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.PerformCustomTargetingKeyAction(
            action, filter_statement), tuple))
    self.__class__.key1 = None
    self.__class__.key2 = None

  def testDeleteCustomTargetingValues(self):
    """Test whether we can delete existing custom targeting values."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()
    if not self.__class__.value1:
      self.testCreateCustomTargetingValues()

    action = {'type': 'DeleteCustomTargetingValueAction'}
    values = [{
        'key': 'keyId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': self.__class__.key1['id']
        }
    }]
    filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId '
                                 'AND id IN (%s)' % self.__class__.value1['id'],
                        'values': values}
    self.assert_(isinstance(
        self.__class__.service.PerformCustomTargetingValueAction(
            action, filter_statement), tuple))
    self.__class__.value1 = None


class CustomTargetingServiceTestV201103(unittest.TestCase):

  """Unittest suite for CustomTargetingService using v201103."""

  SERVER = SERVER_V201103
  VERSION = VERSION_V201103
  client.debug = False
  service = None
  key1 = None
  key2 = None
  value1 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCustomTargetingService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateCustomTargetingKeys(self):
    """Test whether we can create custom targeting keys."""
    keys = [
        {
            'displayName': 'gender',
            'name': Utils.GetUniqueName(10),
            'type': 'PREDEFINED'
        },
        {
            'displayName': 'car model',
            'name': Utils.GetUniqueName(10),
            'type': 'FREEFORM'
        }
    ]
    try:
      keys = self.__class__.service.CreateCustomTargetingKeys(keys)
      self.__class__.key1 = keys[0]
      self.__class__.key2 = keys[1]
      self.assert_(isinstance(keys, tuple))
    except DfpApiError, e:
      if e.message.find('CustomTargetingError.KEY_COUNT_TOO_LARGE') > -1:
        self.testDeleteCustomTargetingKeys()
      else:
        raise e

  def testCreateCustomTargetingValues(self):
    """Test whether we can create custom targeting values."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()

    values = [
        {
          'customTargetingKeyId': self.__class__.key1['id'],
          'displayName': 'male',
          'name': Utils.GetUniqueName(40),
          'matchType': 'EXACT'
        },
        {
          'customTargetingKeyId': self.__class__.key1['id'],
          'displayName': 'female',
          'name': Utils.GetUniqueName(40),
          'matchType': 'EXACT'
        }
    ]
    try:
      values = self.__class__.service.CreateCustomTargetingValues(values)
      self.__class__.value1 = values[0]
      self.assert_(isinstance(values, tuple))
    except DfpApiError, e:
      if e.message.find('CustomTargetingError.VALUE_NAME_DUPLICATE') > -1:
        self.testDeleteCustomTargetingValues()
      else:
        raise e

  def testGetAllCustomTargetingKeys(self):
    """Test whether we can retrieve all custom targeting keys."""
    values = [{
        'key': 'type',
        'value': {
            'xsi_type': 'TextValue',
            'value': 'PREDEFINED'
        }
    }]
    filter_statement = {'query': 'WHERE type = :type LIMIT 500',
                        'values': values}
    self.assert_(isinstance(
        self.__class__.service.GetCustomTargetingKeysByStatement(
            filter_statement), tuple))

  def testGetAllCustomTargetingValues(self):
    """Test whether we can retrieve all custom targeting values."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()

    values = [{
        'key': 'keyId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': self.__class__.key1['id']
        }
    }]
    filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId '
                                 'LIMIT 500',
                        'values': values}
    self.assert_(isinstance(
        self.__class__.service.GetCustomTargetingValuesByStatement(
            filter_statement), tuple))

  def testUpdateCustomTargetingKeys(self):
    """Test whether we can update existing custom targeting keys."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()

    keys = [self.__class__.key1, self.__class__.key2]
    for key in keys:
      key['displayName'] += ' (Deprecated)'
    self.assert_(isinstance(
        self.__class__.service.UpdateCustomTargetingKeys(keys), tuple))

  def testUpdateCustomTargetingValues(self):
    """Test whether we can update existing custom targeting values."""
    if not self.__class__.value1:
      self.testCreateCustomTargetingValues()

    values = [self.__class__.value1]
    for value in values:
      value['displayName'] += ' (Deprecated)'
    self.assert_(isinstance(
        self.__class__.service.UpdateCustomTargetingValues(values), tuple))

  def testDeleteCustomTargetingKeys(self):
    """Test whether we can delete existing custom targeting keys."""
    action = {'type': 'DeleteCustomTargetingKeys'}
    filter_statement = {'query': 'LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.PerformCustomTargetingKeyAction(
            action, filter_statement), tuple))
    self.__class__.key1 = None
    self.__class__.key2 = None

  def testDeleteCustomTargetingValues(self):
    """Test whether we can delete existing custom targeting values."""
    if not self.__class__.key1 or not self.__class__.key2:
      self.testCreateCustomTargetingKeys()
    if not self.__class__.value1:
      self.testCreateCustomTargetingValues()

    action = {'type': 'DeleteCustomTargetingValues'}
    values = [{
        'key': 'keyId',
        'value': {
            'xsi_type': 'NumberValue',
            'value': self.__class__.key1['id']
        }
    }]
    filter_statement = {'query': 'WHERE customTargetingKeyId = :keyId '
                                 'AND id IN (%s)' % self.__class__.value1['id'],
                        'values': values}
    self.assert_(isinstance(
        self.__class__.service.PerformCustomTargetingValueAction(
            action, filter_statement), tuple))
    self.__class__.value1 = None


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CustomTargetingServiceTestV201101))
  return suite


def makeTestSuiteV201103():
  """Set up test suite using v201103.

  Returns:
    TestSuite test suite using v201103.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CustomTargetingServiceTestV201103))
  return suite


if __name__ == '__main__':
  suite_v201101 = makeTestSuiteV201101()
  suite_v201103 = makeTestSuiteV201103()
  alltests = unittest.TestSuite([suite_v201101, suite_v201103])
  unittest.main(defaultTest='alltests')
