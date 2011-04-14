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

"""This code example creates new companies. To determine which companies exist,
run get_all_companies.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.common import Utils
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
company_service = client.GetCompanyService(
    'https://sandbox.google.com', 'v201004')

# Create company objects.
companies = []
for i in xrange(5):
  company = {
      'name': 'Company #%s' % Utils.GetUniqueName(),
      'type': 'ADVERTISER'
  }
  companies.append(company)

# Add companies.
# The initialization of the service and addition of companies could've been
# combined into a single statement. Ex:
# companies = client.GetCompanyService().CreateCompanies(companies)
companies = company_service.CreateCompanies(companies)

# Display results.
for company in companies:
  print ('Company with id \'%s\', name \'%s\', and type \'%s\' was created.'
         % (company['id'], company['name'], company['type']))
