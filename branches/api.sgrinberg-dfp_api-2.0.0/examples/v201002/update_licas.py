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

"""This code example updates the destination URL of all line item creative
associations (LICA) up to the first 500. To determine which LICAs exist, run
get_all_licas.py."""

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
lica_service = client.GetLineItemCreativeAssociationService()

# Create filter object to get all LICAs.
filter = {'text': 'LIMIT 500'}

# Get LICAs by filter.
licas = lica_service.GetLineItemCreativeAssociationsByFilter(
    filter)[0]['results']

if licas:
  # Update each local LICA object by changing its destination URL.
  for lica in licas:
    lica['destinationUrl'] = 'http://news.google.com'

  # Update LICAs remotely.
  licas = lica_service.UpdateLineItemCreativeAssociations(licas)

  # Display results.
  if licas:
    for lica in licas:
      print ('LICA with line item id \'%s\', creative id \'%s\', and status '
             '\'%s\' was updated.' % (lica['lineItemId'], lica['creativeId'],
                                      lica['status']))
  else:
    print 'No LICAs were updated.'
else:
  print 'No LICAs found to update.'
