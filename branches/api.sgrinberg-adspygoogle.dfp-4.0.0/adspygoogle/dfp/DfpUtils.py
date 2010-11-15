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

"""Handy utility functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os

from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import LIB_HOME
from adspygoogle.dfp import MIN_API_VERSION


def GetCurrencies():
  """Get a list of available currencies.

  Returns:
    list available currencies.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'currencies.csv'))


def GetTimezones():
  """Get a list of available timezones.

  Returns:
    list Available timezones.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'timezones.csv'))


def GetAllEntitiesByStatement(client, service_name, query='', page_size=500,
                              server='https://sandbox.google.com',
                              version=MIN_API_VERSION, http_proxy=None):
  """Get all existing entities by statement.

  All existing entities are retrived for a given statement and page size. The
  retrieval of entities works across all services. Thus, the same method can
  be used to fetch companies, creatives, ad units, line items, etc. The results,
  even if they span multiple pages, are grouped into a single list of entities.

  Args:
    client: Client an instance of Client.
    service_name: str name of the service to use.
    [optional]
    query: str a statement filter to apply, if any. The default is empty string.
    page_size: int size of the page to use. If page size is less than 0 or
               greater than 500, defaults to 500.
    server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
    version: str API version to use.
    http_proxy: str HTTP proxy to use.

  Returns:
    list a list of existing entities.
  """
  service = eval('client.Get%sService(server, version, http_proxy)'
                 % service_name)
  if service_name == 'Inventory':
    service_name = 'AdUnit'
  if service_name[-1] == 'y':
    method_name = service_name[:-1] + 'ies'
  else:
    method_name = service_name + 's'
  method_name = 'Get%sByStatement' % method_name

  if page_size <= 0 or page_size > 500:
    page_size = 500

  if (query and
      (query.upper().find('LIMIT') > -1 or query.upper().find('OFFSET') > -1)):
    raise ValidationError('The filter query contains an option that is '
                          'incompatible with this method.')

  offset = 0
  all_entities = []
  while True:
    filter_statement = {'query': '%s LIMIT %s OFFSET %s' % (query, page_size,
                                                            offset)}
    entities = eval('service.%s(filter_statement)[0][\'results\']'
                    % method_name)

    if not entities: break
    all_entities.extend(entities)
    if len(entities) < page_size: break
    offset += page_size
  return all_entities
