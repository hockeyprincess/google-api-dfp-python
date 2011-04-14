#!/usr/bin/python
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

"""Methods to access PublisherQueryLanguageService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService


class PublisherQueryLanguageService(ApiService):

  """Wrapper for PublisherQueryLanguageService.

  The PublisherQueryLanguage Service provides operations for executing a PQL
  statement to retrieve information from the system.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits PublisherQueryLanguageService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = DfpWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(PublisherQueryLanguageService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def Select(self, select_statement):
    """Return rows of data for a given statement.

    Args:
      select_statement: dict Publisher Query Language statement used to specify
                        what data to return.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'select'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      select_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(select_statement),
          'selectStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (select_statement))
    elif self._config['soap_lib'] == ZSI:
      select_statement = self._sanity_check.ValidateStatement(
          select_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'selectStatement': select_statement},)), 'PublisherQueryLanguage',
          self._loc, request)
