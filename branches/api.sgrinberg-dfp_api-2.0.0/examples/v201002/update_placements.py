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

"""This code example updates all placements to include the root ad unit up to
the first 500. To determine which placements exist,
run get_all_placements.py."""

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
# sandbox environment.
placement_service = client.GetPlacementService()
inventory_service = client.GetInventoryService()

# Get the root ad unit by filter.
root_ad_unit_id = inventory_service.GetAdUnitsByFilter(
    {'text': 'WHERE parentId IS NULL LIMIT 1'})[0]['results'][0]['id']

# Create a filter to select first 500 placements.
filter = {'text': 'LIMIT 500'}

# Get placements by filter.
placements = placement_service.GetPlacementsByFilter(filter)[0]['results']
if placements:
  # Update each local placement object by adding the root ad unit.
  for placement in placements:
    if root_ad_unit_id not in placement['targetedAdUnitIds']:
      placement['targetedAdUnitIds'].append(root_ad_unit_id)

  # Update placements remotely.
  placements = placement_service.UpdatePlacements(placements)

  # Display results.
  if placements:
    for placement in placements:
      print ('Placement with id \'%s\', name \'%s\', and containing ad units '
             '{%s} was updated.' % (placement['id'], placement['name'],
                                   ', '.join(placement['targetedAdUnitIds'])))
  else:
    print 'No placements were updated.'
else:
  print 'No placements found to update.'
