#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Settings and configuration for the unit tests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.dfp.DfpClient import DfpClient


HTTP_PROXY = None
SERVER_V201004 = 'https://sandbox.google.com'
SERVER_V201010 = 'https://sandbox.google.com'
SERVER_V201101 = 'https://sandbox.google.com'
SERVER_V201103 = 'https://sandbox.google.com'
VERSION_V201004 = 'v201004'
VERSION_V201010 = 'v201010'
VERSION_V201101 = 'v201101'
VERSION_V201103 = 'v201103'
client = DfpClient(path=os.path.join('..', '..', '..'))
client.soap_lib = ZSI
