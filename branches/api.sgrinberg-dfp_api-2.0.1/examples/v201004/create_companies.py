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
import sys
sys.path.append('../..')
import time

# Import appropriate classes from the client library.
from dfp_api.Client import Client


# Initialize Client object. The "path" parameter should point to the location of
# pickles, which get generated after execution of "dfp_api_config.py" script.
# The same location is used for the "logs/" directory, if logging is enabled.
client = Client(path='../..')

# Temporarily disable debugging. If enabled, the debugging data will be sent to
# STDOUT.
client.debug = False

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
company_service = client.GetCompanyService()

# Create company objects.
companies = []
for i in xrange(5):
  company = {
      'name': 'Company #%s' % str(time.time()).split('.')[0] + str(i),
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
