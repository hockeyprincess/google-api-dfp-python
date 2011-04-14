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

"""Methods to access LineItemService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService


class LineItemService(ApiService):

  """Wrapper for LineItemService.

  The LineItem Service provides methods for creating, updating and retrieving
  line items.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits LineItemService.

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
    super(LineItemService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateLineItem(self, line_item):
    """Create a new line item.

    Args:
      line_item: dict Line item to create.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'createLineItem'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      self._sanity_check.ValidateLineItem(line_item)
      line_item = self._message_handler.PackDictAsXml(
          line_item, 'lineItem', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (line_item))
    elif self._config['soap_lib'] == ZSI:
      self._sanity_check.ValidateLineItem(line_item, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItem': line_item},)),
                                       'LineItem', self._loc, request)

  def CreateLineItems(self, line_items):
    """Create a list of new line items.

    Args:
      line_items: list Line items to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((line_items, list),))

    method_name = 'createLineItems'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_line_items = []
      for line_item in line_items:
        self._sanity_check.ValidateLineItem(line_item)
        new_line_items.append(self._message_handler.PackDictAsXml(
            line_item, 'lineItems', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_line_items)))
    elif self._config['soap_lib'] == ZSI:
      for item in line_items:
        self._sanity_check.ValidateLineItem(item, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItems': line_items},)),
                                       'LineItem', self._loc, request)

  def GetLineItem(self, line_item_id):
    """Return the line item uniquely identified by the given id.

    Args:
      line_item_id: str ID of the line item, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((line_item_id, (str, unicode)),))

    method_name = 'getLineItem'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      line_item_id = self._message_handler.PackDictAsXml(
          line_item_id, 'lineItemId', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (line_item_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItemId': line_item_id},)),
                                       'LineItem', self._loc, request)

  def GetLineItemsByStatement(self, filter_statement):
    """Return the line items that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of line items.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getLineItemsByStatement'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      filter_statement = self._message_handler.PackDictAsXml(
          self._sanity_check.ValidateStatement(filter_statement),
          'filterStatement', OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (filter_statement))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._sanity_check.ValidateStatement(
          filter_statement, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
          (({'filterStatement': filter_statement},)), 'LineItem', self._loc,
          request)

  def PerformLineItemAction(self, action, filter_statement):
    """Perform action on line items that match the given statement.

    Args:
      action: str Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'performLineItemAction'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      self._sanity_check.ValidateAction(action)
      action = self._message_handler.PackDictAsXml(action, 'lineItemAction',
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
          (({'lineItemAction': action}, {'filterStatement': filter_statement})),
          'LineItem', self._loc, request)

  def UpdateLineItem(self, line_item):
    """Update the specified line item.

    Args:
      line_item: dict Line item to update.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'updateLineItem'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      self._sanity_check.ValidateLineItem(line_item)
      line_item = self._message_handler.PackDictAsXml(line_item, 'lineItem',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (line_item))
    elif self._config['soap_lib'] == ZSI:
      self._sanity_check.ValidateLineItem(line_item, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItem': line_item},)),
                                       'LineItem', self._loc, request)

  def UpdateLineItems(self, line_items):
    """Update a list of specified line items.

    Args:
      line_items: list Line items to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((line_items, list),))

    method_name = 'updateLineItems'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      for item in line_items:
        self._sanity_check.ValidateLineItem(item)
      new_line_items = []
      for line_item in line_items:
        new_line_items.append(self._message_handler.PackDictAsXml(
            line_item, 'lineItems', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_line_items)))
    elif self._config['soap_lib'] == ZSI:
      for item in line_items:
        self._sanity_check.ValidateLineItem(item, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItems': line_items},)),
                                       'LineItem', self._loc, request)
