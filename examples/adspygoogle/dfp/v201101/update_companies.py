#!/usr/bin/python
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

"""This code example updates the names of all companies that are advertisers by
appending ' LLC.' up to the first 500. To determine which companies exist, run
get_all_companies.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# the sandbox environment.
company_service = client.GetCompanyService(
    'https://sandbox.google.com', 'v201101')

# Create statement object to only select companies that are advertises.
filter_statement = {'query': 'WHERE type = \'ADVERTISER\' LIMIT 500'}

# Get companies by statement.
companies = company_service.GetCompaniesByStatement(
    filter_statement)[0]['results']

if companies:
  # Update each local company object by appending ' LLC.' to its name.
  for company in companies:
    company['name'] += ' LLC.'

  # Update companies remotely.
  companies = company_service.UpdateCompanies(companies)

  # Display results.
  if companies:
    for company in companies:
      print ('Company with id \'%s\' and name \'%s\' was updated.'
             % (company['id'], company['name']))
  else:
    print 'No companies were updated.'
else:
  print 'No companies found to update.'
