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

"""This example updates a line item to add custom criteria targeting. To
determine which line items exist, run get_all_line_items.py. To determine which
custom targeting keys and values exist, run
get_all_custom_targeting_keys_and_values.py"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import pprint
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
line_item_service = client.GetLineItemService(
    'https://sandbox.google.com', 'v201103')

line_item_id = 'INSERT_LINE_ITEM_ID_HERE'
key_id1 = 'INSERT_FREE_FORM_CUSTOM_TARGETING_KEY_ID_HERE'
key_id2 = 'INSERT_FREE_FORM_CUSTOM_TARGETING_KEY_ID_HERE'

# Create the free-form custom criteria for targeting 'toyota'.
toyota_criteria = {
    'xsi_type': 'FreeFormCustomCriteria',
    'keyId': key_id1,
    'operator': 'IS',
    'values': [{
        'name': 'toyota',
        'matchType': 'EXACT'
    }]
}

# Create the free-form custom criteria for targeting 'honda'.
honda_criteria = {
    'xsi_type': 'FreeFormCustomCriteria',
    'keyId': key_id1,
    'operator': 'IS_NOT',
    'values': [{
        'name': 'honda',
        'matchType': 'EXACT'
    }]
}

# Create the free-form custom criteria for targeting 'ford'.
ford_criteria = {
    'xsi_type': 'FreeFormCustomCriteria',
    'keyId': key_id2,
    'operator': 'IS',
    'values': [{
        'name': 'ford',
        'matchType': 'EXACT'
    }]
}

# Create the custom criteria set that will resemble:
# (key1 == toyota OR (key1 != honda AND key2 == ford))
sub_set = {
    'xsi_type': 'CustomCriteriaSet',
    'logicalOperator': 'AND',
    'children': [honda_criteria, ford_criteria]
}

top_set = {
    'xsi_type': 'CustomCriteriaSet',
    'logicalOperator': 'OR',
    'children': [toyota_criteria, sub_set]
}

# Set custom criteria targeting on the line item.
line_item = line_item_service.GetLineItem(line_item_id)[0]
line_item['targeting']['customTargeting'] = top_set

# Update line item.
line_item = line_item_service.UpdateLineItem(line_item)[0]

# Display results.
if line_item:
  print ('Line item with id \'%s\' updated with custom criteria targeting:'
         % line_item['id'])
  pprint.pprint(line_item['targeting']['customTargeting'])
else:
  print 'No line items were updated.'
