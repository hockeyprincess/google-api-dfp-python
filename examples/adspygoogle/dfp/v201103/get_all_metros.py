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

"""This example gets all metros available to target."""

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
pql_service = client.GetPublisherQueryLanguageService(
    'https://sandbox.google.com', 'v201103')

select_statement = {'query': 'SELECT * FROM Metro WHERE targetable = true'}

# Get metros by statement.
result_set = pql_service.Select(select_statement)[0]

# Display results.
if result_set:
  column_labels = [label.values()[0] for label in result_set['columnTypes']]
  print 'Columns are: %s' % ', '.join(column_labels)
  for row in result_set['rows']:
    values = [value.values()[1] for value in row['values']]
    print 'Values are: %s' % ', '.join(values)
else:
  print 'No results found.'
