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

"""This code example deactivates all active ad units. To determine which ad
units exist, run get_all_ad_units.py."""

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
inventory_service = client.GetInventoryService(
    'https://sandbox.google.com', 'v201103')

# Create query.
query = 'WHERE status = \'ACTIVE\''

# Get ad units by statement.
ad_units = DfpUtils.GetAllEntitiesByStatement(client, 'Inventory', query)
for ad_unit in ad_units:
  print ('Ad unit with id \'%s\', name \'%s\', and status \'%s\' will be '
         'deactivated.' % (ad_unit['id'], ad_unit['name'], ad_unit['status']))
print 'Number of ad units to be deactivated: %s' % len(ad_units)

# Perform action.
result = inventory_service.PerformAdUnitAction({'type': 'DeactivateAdUnits'},
                                               {'query': query})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of ad units deactivated: %s' % result['numChanges']
else:
  print 'No ad units were deactivated.'
