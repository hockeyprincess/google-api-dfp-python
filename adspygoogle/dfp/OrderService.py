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

"""Methods to access OrderService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp.DfpWebService import DfpWebService


class OrderService(ApiService):

  """Wrapper for OrderService.

  The Order Service provides methods for creating, updating and retrieving
  orders.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits OrderService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: Dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = DfpWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(OrderService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateOrder(self, order):
    """Create a new order.

    Args:
      order: dict Order to create.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateOrder(order)

    method_name = 'createOrder'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      order = self._message_handler.PackDictAsXml(order, 'order',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (order))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'order': order},)),
                                       'Order', self._loc, request)

  def CreateOrders(self, orders):
    """Create a list of new orders.

    Args:
      orders: list Orders to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((orders, list),))
    for item in orders:
      self._sanity_check.ValidateOrder(item)

    method_name = 'createOrders'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_orders = []
      for order in orders:
        new_orders.append(self._message_handler.PackDictAsXml(
            order, 'orders', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_orders)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'orders': orders},)),
                                       'Order', self._loc, request)

  def GetOrder(self, order_id):
    """Return the order uniquely identified by the given id.

    Args:
      order_id: str ID of the order, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((order_id, (str, unicode)),))

    method_name = 'getOrder'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      order_id = self._message_handler.PackDictAsXml(order_id, 'orderId',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (order_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'orderId': order_id},)),
                                       'Order', self._loc, request)

  def GetOrdersByStatement(self, filter_statement):
    """Return the orders that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of orders.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getOrdersByStatement'
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
          (({'filterStatement': filter_statement},)), 'Order', self._loc,
          request)

  def PerformOrderAction(self, action, filter_statement):
    """Perform action on orders that match the given statement.

    Args:
      action: str Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'performOrderAction'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      self._sanity_check.ValidateAction(action)
      action = self._message_handler.PackDictAsXml(action, 'orderAction',
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
          (({'orderAction': action}, {'filterStatement': filter_statement})),
          'Order', self._loc, request)

  def UpdateOrder(self, order):
    """Update the specified order.

    Args:
      order: dict Order to update.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateOrder(order)

    method_name = 'updateOrder'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      order = self._message_handler.PackDictAsXml(order, 'order',
          OBJ_KEY_ORDER_MAP)
      return self.__service.CallMethod(method_name, (order))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'order': order},)),
                                       'Order', self._loc, request)

  def UpdateOrders(self, orders):
    """Update a list of specified orders.

    Args:
      orders: list Orders to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((orders, list),))
    for item in orders:
      self._sanity_check.ValidateOrder(item)

    method_name = 'updateOrders'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.dfp.soappy import OBJ_KEY_ORDER_MAP
      new_orders = []
      for order in orders:
        new_orders.append(self._message_handler.PackDictAsXml(
            order, 'orders', OBJ_KEY_ORDER_MAP))
      return self.__service.CallMethod(method_name, (''.join(new_orders)))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'orders': orders},)),
                                       'Order', self._loc, request)
