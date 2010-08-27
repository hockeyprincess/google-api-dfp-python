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

"""Unit tests to cover ReportService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201004
from tests.adspygoogle.dfp import VERSION_V201004
from tests.adspygoogle.dfp import client


class ReportServiceTestV201004(unittest.TestCase):

  """Unittest suite for ReportService using v201004."""

  SERVER = SERVER_V201004
  VERSION = VERSION_V201004
  client.debug = False
  service = None
  report_job_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testRunDeliveryReport(self):
    """Test whether we can run a delivery report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['ORDER'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'AD_SERVER_CTR', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    report_job = self.__class__.service.RunReportJob(report_job)
    self.__class__.report_job_id = report_job[0]['id']
    self.assert_(isinstance(report_job, tuple))

  def testRunInventoryReport(self):
    """Test whether we can run an inventory report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['DATE'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'ADSENSE_IMPRESSIONS', 'ADSENSE_CLICKS',
                        'TOTAL_IMPRESSIONS', 'TOTAL_REVENUE'],
            'dateRangeType': 'LAST_WEEK'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testRunSalesReport(self):
    """Test whether we can run a sales report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['SALESPERSON'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testGetReportJob(self):
    """Test whether we can retrieve existing report job."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportJob(
        self.__class__.report_job_id), tuple))

  def testGetReportDownloadUrl(self):
    """Test whether we can retrieve report download URL."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportDownloadURL(
        self.__class__.report_job_id, 'CSV'), tuple))

  def testDownloadCsvReport(self):
    """Test whether we can download a CSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'CSV'), str))

  def testDownloadTsvReport(self):
    """Test whether we can download a TSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'TSV'), str))


def makeTestSuiteV201004():
  """Set up test suite using v201004.

  Returns:
    TestSuite test suite using v201004.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV201004))
  return suite


if __name__ == '__main__':
  suite_v201004 = makeTestSuiteV201004()
  alltests = unittest.TestSuite([suite_v201004])
  unittest.main(defaultTest='alltests')
