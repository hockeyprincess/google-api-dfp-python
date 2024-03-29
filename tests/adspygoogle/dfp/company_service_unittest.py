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

"""Unit tests to cover CompanyService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import SERVER_V201010
from tests.adspygoogle.dfp import SERVER_V201101
from tests.adspygoogle.dfp import SERVER_V201103
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import VERSION_V201010
from tests.adspygoogle.dfp import VERSION_V201101
from tests.adspygoogle.dfp import VERSION_V201103
from tests.adspygoogle.dfp import client


class CompanyServiceTestV201004(unittest.TestCase):

  """Unittest suite for CompanyService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  company1 = None
  company2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateCompany(self):
    """Test whether we can create a company."""
    company = {
        'name': 'Company #%s' % Utils.GetUniqueName(),
        'type': 'ADVERTISER'
    }
    self.assert_(isinstance(self.__class__.service.CreateCompany(company),
                            tuple))

  def testCreateCompanies(self):
    """Test whether we can create a list of companies."""
    companies = [
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      },
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
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

  def testGetCompaniesByStatement(self):
    """Test whether we can fetch a list of existing companies that match given
    statement."""
    if self.__class__.company1 is None:
      self.testCreateCompanies()
    filter_statement = {'query': 'WHERE id = %s ORDER BY name LIMIT 1'
                        % self.__class__.company1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetCompaniesByStatement(filter_statement),
        tuple))

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


class CompanyServiceTestV201010(unittest.TestCase):

  """Unittest suite for CompanyService using v201010."""

  SERVER = SERVER_V201010
  VERSION = VERSION_V201010
  client.debug = False
  service = None
  company1 = None
  company2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateCompany(self):
    """Test whether we can create a company."""
    company = {
        'name': 'Company #%s' % Utils.GetUniqueName(),
        'type': 'ADVERTISER'
    }
    self.assert_(isinstance(self.__class__.service.CreateCompany(company),
                            tuple))

  def testCreateCompanies(self):
    """Test whether we can create a list of companies."""
    companies = [
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      },
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
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

  def testGetCompaniesByStatement(self):
    """Test whether we can fetch a list of existing companies that match given
    statement."""
    if self.__class__.company1 is None:
      self.testCreateCompanies()
    filter_statement = {'query': 'WHERE id = %s ORDER BY name LIMIT 1'
                        % self.__class__.company1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetCompaniesByStatement(filter_statement),
        tuple))

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


class CompanyServiceTestV201101(unittest.TestCase):

  """Unittest suite for CompanyService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  company1 = None
  company2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateCompany(self):
    """Test whether we can create a company."""
    company = {
        'name': 'Company #%s' % Utils.GetUniqueName(),
        'type': 'ADVERTISER'
    }
    self.assert_(isinstance(self.__class__.service.CreateCompany(company),
                            tuple))

  def testCreateCompanies(self):
    """Test whether we can create a list of companies."""
    companies = [
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      },
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
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

  def testGetCompaniesByStatement(self):
    """Test whether we can fetch a list of existing companies that match given
    statement."""
    if self.__class__.company1 is None:
      self.testCreateCompanies()
    filter_statement = {'query': 'WHERE id = %s ORDER BY name LIMIT 1'
                        % self.__class__.company1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetCompaniesByStatement(filter_statement),
        tuple))

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


class CompanyServiceTestV201103(unittest.TestCase):

  """Unittest suite for CompanyService using v201103."""

  SERVER = SERVER_V201103
  VERSION = VERSION_V201103
  client.debug = False
  service = None
  company1 = None
  company2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCompanyService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCreateCompany(self):
    """Test whether we can create a company."""
    company = {
        'name': 'Company #%s' % Utils.GetUniqueName(),
        'type': 'ADVERTISER'
    }
    self.assert_(isinstance(self.__class__.service.CreateCompany(company),
                            tuple))

  def testCreateCompanies(self):
    """Test whether we can create a list of companies."""
    companies = [
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
          'type': 'ADVERTISER'
      },
      {
          'name': 'Company #%s' % Utils.GetUniqueName(),
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

  def testGetCompaniesByStatement(self):
    """Test whether we can fetch a list of existing companies that match given
    statement."""
    if self.__class__.company1 is None:
      self.testCreateCompanies()
    filter_statement = {'query': 'WHERE id = %s ORDER BY name LIMIT 1'
                        % self.__class__.company1['id']}
    self.assert_(isinstance(
        self.__class__.service.GetCompaniesByStatement(filter_statement),
        tuple))

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


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CompanyServiceTestV201004))
  return suite


def makeTestSuiteV201010():
  """Set up test suite using v201010.

  Returns:
    TestSuite test suite using v201010.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CompanyServiceTestV201010))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CompanyServiceTestV201101))
  return suite


def makeTestSuiteV201103():
  """Set up test suite using v201103.

  Returns:
    TestSuite test suite using v201103.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CompanyServiceTestV201103))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  suite_v201010 = makeTestSuiteV201010()
  suite_v201101 = makeTestSuiteV201101()
  suite_v201103 = makeTestSuiteV201103()
  alltests = unittest.TestSuite([suite_v201004, suite_v201010, suite_v201101,
                                 suite_v201103])
  unittest.main(defaultTest='alltests')
