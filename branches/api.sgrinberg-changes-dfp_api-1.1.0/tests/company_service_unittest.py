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

"""Unit tests to cover CompanyService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import time
import unittest

from tests import HTTP_PROXY
from tests import SERVER
from tests import client


class CompanyServiceTestV201002(unittest.TestCase):

  """Unittest suite for CompanyService using v201002."""

  SERVER_v201002 = SERVER
  VERSION_v201002 = 'v201002'
  client.debug = False
  service = None
  company1 = None
  company2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCompanyService(
          self.__class__.SERVER_v201002, self.__class__.VERSION_v201002,
          HTTP_PROXY)

  def testCreateCompany(self):
    """Test whether we can create a company."""
    company = {
      'name': 'Company #%s' % time.time(),
      'type': 'ADVERTISER'
    }
    self.assert_(isinstance(self.__class__.service.CreateCompany(company),
                            tuple))

  def testCreateCompanies(self):
    """Test whether we can create a list of companies."""
    companies = [
      {
          'name': 'Company #%s' % time.time(),
          'type': 'ADVERTISER'
      },
      {
          'name': 'Company #%s' % str(time.time() + 0.01),
          'type': 'ADVERTISER'
      }
    ]
    companies = self.__class__.service.CreateCompanies(companies)
    self.__class__.company1 = companies[0]
    self.__class__.company2 = companies[1]
    self.assert_(isinstance(companies, tuple))

  def testGetCompany(self):
    """Test whether we can fetch an existing company."""
    if self.__class__.company1 is None:
      self.testCreateCompanies()
    self.assert_(isinstance(
        self.__class__.service.GetCompany(self.__class__.company1['id']),
        tuple))

  def testGetCompaniesByFilter(self):
    """Test whether we can fetch a list of existing companies that match given
    filter."""
    filter = {'text': 'WHERE type = \'ADVERTISER\' ORDER BY name LIMIT 500'}
    self.assert_(isinstance(
        self.__class__.service.GetCompaniesByFilter(filter), tuple))

  def testUpdateCompany(self):
    """Test whether we can update a company."""
    if self.__class__.company1 is None:
      self.testCreateCompanies()
    postfix = ' Corp.'
    self.__class__.company1['name'] = self.__class__.company1['name'] + postfix
    company = self.__class__.service.UpdateCompany(
        self.__class__.company1)
    self.assert_(isinstance(company, tuple))
    self.assertTrue(company[0]['name'].find(postfix) > -1)

  def testUpdateCompanies(self):
    """Test whether we can update a list of companies."""
    if self.__class__.company1 is None or self.__class__.company2 is None:
      self.testCreateCompanies()
    postfix = ' LLC'
    self.__class__.company1['name'] = self.__class__.company1['name'] + postfix
    self.__class__.company2['name'] = self.__class__.company2['name'] + postfix
    companies = self.__class__.service.UpdateCompanies(
        [self.__class__.company1, self.__class__.company2])
    self.assert_(isinstance(companies, tuple))
    for company in companies:
      self.assertTrue(company['name'].find(postfix) > -1)


def makeTestSuiteV201002():
  """Set up test suite using v201002.

  Returns:
    TestSuite test suite using v201002.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CompanyServiceTestV201002))
  return suite


if __name__ == '__main__':
  suite_v201002 = makeTestSuiteV201002()
  alltests = unittest.TestSuite([suite_v201002])
  unittest.main(defaultTest='alltests')