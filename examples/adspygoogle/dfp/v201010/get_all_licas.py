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

"""This code example gets all line item creative associations (LICA). To create
LICAs, run create_licas.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp import DfpUtils
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
lica_service = client.GetLineItemCreativeAssociationService(
    'https://sandbox.google.com', 'v201010')

# Get LICAs by statement.
licas = DfpUtils.GetAllEntitiesByStatement(client,
                                           'LineItemCreativeAssociation')

# Display results.
for lica in licas:
  print ('LICA with line item id \'%s\', creative id \'%s\', and status '
         '\'%s\' was found.' % (lica['lineItemId'], lica['creativeId'],
                                lica['status']))

print
print 'Number of results found: %s' % len(licas)
