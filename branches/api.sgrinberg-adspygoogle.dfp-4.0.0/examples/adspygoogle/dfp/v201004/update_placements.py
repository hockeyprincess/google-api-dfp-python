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

"""This code example updates all placements to allow for AdSense targeting up to
the first 500. To determine which placements exist,
run get_all_placements.py."""

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
placement_service = client.GetPlacementService(
    'https://sandbox.google.com', 'v201004')
inventory_service = client.GetInventoryService(
    'https://sandbox.google.com', 'v201004')

# Get the root ad unit by statement.
root_ad_unit_id = inventory_service.GetAdUnitsByStatement(
    {'query': 'WHERE parentId IS NULL LIMIT 1'})[0]['results'][0]['id']

# Create a statement to select first 500 placements.
filter_statement = {'query': 'LIMIT 500'}

# Get placements by statement.
placements = placement_service.GetPlacementsByStatement(
    filter_statement)[0]['results']
if placements:
  # Update each local placement object by enabling AdSense targeting.
  for placement in placements:
    if not placement['targetingDescription']:
      placement['targetingDescription'] = 'Generic description'
    placement['targetingAdLocation'] = 'All images on sports pages.'
    placement['targetingSiteName'] = 'http://code.google.com'
    placement['isAdSenseTargetingEnabled'] = 'true'

  # Update placements remotely.
  placements = placement_service.UpdatePlacements(placements)

  # Display results.
  if placements:
    for placement in placements:
      ad_unit_ids = ''
      if 'targetedAdUnitIds' in placement:
        ad_unit_ids = ', '.join(placement['targetedAdUnitIds'])
      print ('Placement with id \'%s\', name \'%s\', and AdSense targeting '
             'enabled \'%s\' was updated.'
             % (placement['id'], placement['name'],
                placement['isAdSenseTargetingEnabled']))
  else:
    print 'No placements were updated.'
else:
  print 'No placements found to update.'
