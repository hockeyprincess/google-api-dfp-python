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

"""This code example gets all companies that are advertisers. The statement
retrieves up to the maximum page size limit of 500. To create companies, run
create_companies.py."""

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
# sandbox environment.
company_service = client.GetCompanyService(
    'https://sandbox.google.com', 'v201004')

# Create statement object to only select companies that are advertisers sorted
# by name.
params = [{
    'type': 'StringParam',
    'key': 'type',
    'value': 'ADVERTISER'
}]
filter_statement = {'query': 'WHERE type = :type ORDER BY name LIMIT 500',
                    'params': params}

# Get companies by statement.
companies = company_service.GetCompaniesByStatement(
    filter_statement)[0]['results']

# Display results.
for company in companies:
  print ('Company with id \'%s\', name \'%s\', and type \'%s\' was found.'
         % (company['id'], company['name'], company['type']))

print
print 'Number of results found: %s' % len(companies)
