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

"""This code example gets a line item by its id. To determine which line items
exist, run get_all_line_items.py."""

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
line_item_service = client.GetLineItemService(
    'https://sandbox.google.com', 'v201101')

# Set the id of the line item to get.
line_item_id = 'INSERT_LINE_ITEM_ID_HERE'

# Get company.
line_item = line_item_service.GetLineItem(line_item_id)[0]

# Display results.
print ('Line item with id \'%s\', belonging to order id \'%s\', and named '
       '\'%s\' was found.' % (line_item['id'], line_item['orderId'],
                              line_item['name']))
