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

"""This code example creates new ad units under a previously created ad unit. To
determine which ad units exist, run get_ad_unin_tree.py or
get_all_ad_units.py"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')
import time

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

# Set the parent ad unit's id for all ad units to be created under.
parent_ad_unit_id = 'INSERT_AD_UNIT_ID_HERE'

# Create ad unit objects.
ad_units = []
for i in xrange(5):
  ad_unit = {
      'name': 'Ad_Unit_%s' % str(time.time()).split('.')[0] + str(i),
      'parentId': parent_ad_unit_id,
      'sizes': [{'width': '300', 'height': '250'}]
  }
  ad_units.append(ad_unit)

# Add ad units.
# The initialization of the service and addition of ad units can be
# combined into a single statement. Ex:
# ad_units = client.GetInventoryService().CreateAdUnits(ad_units)
ad_units = inventory_service.CreateAdUnits(ad_units)

# Display results.
for ad_unit in ad_units:
  print ('Ad unit with id \'%s\' was created under parent with id \'%s\'.'
         % (ad_unit['id'], parent_ad_unit_id))
