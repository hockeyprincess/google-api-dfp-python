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

"""This example deletes a custom targeting key by its name. To determine which
custom targeting keys exist, run get_all_custom_targeting_keys_and_values.py."""

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
custom_targeting_service = client.GetCustomTargetingService(
    'https://sandbox.google.com', 'v201101')

key_name = 'INSERT_CUSTOM_TARGETING_KEY_NAME_HERE'
values = [{
    'key': 'name',
    'value': {
        'xsi_type': 'TextValue',
        'value': key_name
    }
}]
filter_statement = {'query': 'WHERE name = :name',
                    'values': values}

# Get custom targeting keys.
keys = custom_targeting_service.GetCustomTargetingKeysByStatement(
    filter_statement)[0]['results']
print 'Number of custom targeting keys to be deleted: %s' % len(keys)

if keys:
  key_ids = [key['id'] for key in keys]
  action = {'type': 'DeleteCustomTargetingKeyAction'}
  filter_statement = {'query': 'WHERE id IN (%s)' % ', '.join(key_ids)}

  # Delete custom targeting keys.
  result = custom_targeting_service.PerformCustomTargetingKeyAction(
      action, filter_statement)[0]

  # Display results.
  if result and result['numChanges'] > 0:
    print 'Number of custom targeting keys deleted: %s' % result['numChanges']
  else:
    print 'No custom targeting keys were deleted.'
