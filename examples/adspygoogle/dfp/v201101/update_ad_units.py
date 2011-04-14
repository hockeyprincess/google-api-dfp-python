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

"""This code example updates an ad unit by enabling AdSense to the first 500.
To determine which ad units exist, run get_all_ad_units.py or
get_inventory_tree.py."""

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
inventory_service = client.GetInventoryService(
    'https://sandbox.google.com', 'v201101')

# Create statement object to get all ad units.
filter_statement = {'query': 'LIMIT 500'}

# Get ad units by filter.
ad_units = inventory_service.GetAdUnitsByStatement(
    filter_statement)[0]['results']

if ad_units:
  # Update each local ad unit object by enabling AdSense.
  for ad_unit in ad_units:
    ad_unit['inheritedAdSenseSettings']['value']['adSenseEnabled'] = 'true'

  # Update ad units remotely.
  ad_units = inventory_service.UpdateAdUnits(ad_units)

  # Display results.
  if ad_units:
    for ad_units in ad_units:
      print ('Ad unit with id \'%s\', name \'%s\', and is AdSense enabled '
             '\'%s\' was updated.'
             % (ad_unit['id'], ad_unit['name'],
                ad_unit['inheritedAdSenseSettings']['value']['adSenseEnabled']))
  else:
    print 'No ad units were updated.'
else:
  print 'No ad units found to update.'
