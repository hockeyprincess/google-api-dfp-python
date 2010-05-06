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

"""Methods to access InventoryService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService
from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP


class InventoryService(ApiService):

  """Wrapper for InventoryService.

  The Inventory Service provides operations for creating, updating and
  retrieving ad units.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits InventoryService.

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
    super(InventoryService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateAdUnit(self, ad_unit):
    """Create a new ad unit.

    Args:
      ad_unit: dict Ad unit to create.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateAdUnit(ad_unit)

    method_name = 'createAdUnit'
    if self._config['soap_lib'] == SOAPPY:
      ad_unit = self._message_handler.PackDictAsXml(ad_unit, 'adUnit',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (ad_unit))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'adUnit': ad_unit},)),
                                       'Inventory', self._loc, request)

  def CreateAdUnits(self, ad_units):
    """Create a list of new ad units.

    Args:
      ad_units: list Ad units to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((ad_units, list),))
    for item in ad_units:
      self._sanity_check.ValidateAdUnit(item)

    method_name = 'createAdUnits'
    if self._config['soap_lib'] == SOAPPY:
      new_ad_units = []
      for ad_unit in ad_units:
        new_ad_units.append(self._message_handler.PackDictAsXml(
            ad_unit, 'adUnits', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_ad_units)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'adUnits': ad_units},)),
                                       'Inventory', self._loc, request)

  def GetAdUnit(self, ad_unit_id):
    """Return the ad unit uniquely identified by the given id.

    Args:
      ad_unit_id: str ID of the ad unit, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((ad_unit_id, (str, unicode)),))

    method_name = 'getAdUnit'
    if self._config['soap_lib'] == SOAPPY:
      ad_unit_id = self._message_handler.PackDictAsXml(
          ad_unit_id, 'adUnitId', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (ad_unit_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'adUnitId': ad_unit_id},)),
                                       'Inventory', self._loc, request)

  def GetAdUnitsByStatement(self, filter_statement):
    """Return the ad units that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of ad units.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAdUnitsByStatement'
    if self._config['soap_lib'] == SOAPPY:
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (filter_statement))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'filterStatement': filter_statement},)), 'Inventory', self._loc,
          request)

  def PerformAdUnitAction(self, action, filter_statement):
    """Perform action on ad units that match the given statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'performAdUnitAction'
    if self._config['soap_lib'] == SOAPPY:
      self._sanity_check.ValidateAction(action)
      action = self._message_handler.PackDictAsXml(action, 'adUnitAction',
          OBJ_KEY_ORDER_MAP)
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._sanity_check.ValidateAction(action, self._web_services)
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'adUnitAction': action}, {'filterStatement': filter_statement})),
          'Inventory', self._loc, request)

  def UpdateAdUnit(self, ad_unit):
    """Update the specified ad unit.

    Args:
      ad_unit: dict Ad unit to update.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateAdUnit(ad_unit)

    method_name = 'updateAdUnit'
    if self._config['soap_lib'] == SOAPPY:
      ad_unit = self._message_handler.PackDictAsXml(ad_unit, 'adUnit',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (ad_unit))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'adUnit': ad_unit},)),
                                       'Inventory', self._loc, request)

  def UpdateAdUnits(self, ad_units):
    """Update a list of specified ad units.

    Args:
      ad_units: list Ad units to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((ad_units, list),))
    for item in ad_units:
      self._sanity_check.ValidateAdUnit(item)

    method_name = 'updateAdUnits'
    if self._config['soap_lib'] == SOAPPY:
      new_ad_units = []
      for ad_unit in ad_units:
        new_ad_units.append(self._message_handler.PackDictAsXml(
            ad_unit, 'adUnits', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_ad_units)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'adUnits': ad_units},)),
                                       'Inventory', self._loc, request)
