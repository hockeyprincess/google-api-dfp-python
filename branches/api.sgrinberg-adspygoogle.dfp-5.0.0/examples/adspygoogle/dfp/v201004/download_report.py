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

"""This code example downloads a completed report. To run a report, run
run_delivery_report.py."""

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
report_service = client.GetReportService(
    'https://sandbox.google.com', 'v201004')

# Set the id of the completed report.
report_job_id = 'INSERT_REPORT_JOB_ID_HERE'

# Change to your preffered export format.
export_format = 'CSV'

# Download report data.
data = report_service.DownloadReport(report_job_id, export_format)

# Display results.
print 'Data for report job with id \'%s\':\n%s' % (report_job_id, data)
