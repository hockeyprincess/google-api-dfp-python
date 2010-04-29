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

"""This code example updates the destination URL of all image creatives up to
the first 500. To determine which image creatives exist, run
get_all_creatives.py."""

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
creative_service = client.GetCreativeService()

# Create statement object to get all image creatives.
filter_statement = {'query': 'WHERE creativeType = \'ImageCreative\' LIMIT 500'}

# Get creatives by statement.
creatives = creative_service.GetCreativesByStatement(
    filter_statement)[0]['results']

if creatives:
  # Update each local creative object by changing its destination URL.
  for creative in creatives:
    creative['destinationUrl'] = 'http://news.google.com'

  # Update creatives remotely.
  creatives = creative_service.UpdateCreatives(creatives)

  # Display results.
  if creatives:
    for creative in creatives:
      print ('Image creative with id \'%s\' and destination URL \'%s\' was '
             'updated.' % (creative['id'], creative['destinationUrl']))
  else:
    print 'No orders were updated.'
else:
  print 'No orders found to update.'
