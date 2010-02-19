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

"""This code example updates an ad unit by adding a new size to the first 500.
To determine which ad units exist, run get_all_ad_units.py or
get_inventory_tree.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')

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
# the sandbox environment.
inventory_service = client.GetInventoryService()

# Create filter object to get all ad units.
filter = {'text': 'LIMIT 500'}

# Get ad units by filter.
ad_units = inventory_service.GetAdUnitsByFilter(filter)[0]['results']

if ad_units:
  # Update each local ad unit object by adding new size.
  for ad_unit in ad_units:
    ad_unit['sizes'].extend([{'width': '728', 'height': '90'}])

  # Update ad units remotely.
  ad_units = inventory_service.UpdateAdUnits(ad_units)

  # Display results.
  if ad_units:
    for ad_units in ad_units:
      print ('Ad unit with id \'%s\' and name \'%s\' was updated.'
             % (ad_unit['id'], ad_unit['name']))
  else:
    print 'No ad units were updated.'
else:
  print 'No ad units found to update.'
