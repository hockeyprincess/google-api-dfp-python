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

"""This code example creates new image creatives for a given advertiser. To
determine which companies are advertisers, run get_companies_by_filter.py.
To determine which creatives already exist, run get_all_creatives.py."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
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
# sandbox environment.
creative_service = client.GetCreativeService()

# Set id of the advertiser that all creatives will be assigned to.
advertiser_id = 'INSERT_ADVERTISER_ID_HERE'

# Create creative objects.
creatives = []
image_data = open(os.path.join('..', '..', 'tests', 'data',
    'medium_rectangle.jpg').replace('\\', '/'), 'r').read()
for i in xrange(5):
  creative = {
      'type': 'ImageCreative',
      'name': 'Image Creative #%s' % str(time.time()).split('.')[0] + str(i),
      'advertiserId': advertiser_id,
      'destinationUrl': 'http://google.com',
      'imageName': 'image.jpg',
      'imageByteArray': image_data,
      'size': {'width': '300', 'height': '250'}
  }
  creatives.append(creative)

# Add creatives.
# The initialization of the service and addition of creatives could've been
# combined into a single statement. Ex:
# creatives = client.GetCreativeService().CreateCreatives(creatives)
creatives = creative_service.CreateCreatives(creatives)

# Display results.
for creative in creatives:
  print ('Image creative with id \'%s\', name \'%s\', and type \'%s\' was '
         'created and can be previewed at %s.'
         % (creative['id'], creative['name'], creative['Creative_Type'],
            creative['previewUrl']))
