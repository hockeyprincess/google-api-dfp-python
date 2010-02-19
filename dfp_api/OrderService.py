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

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class OrderService(object):

  """Wrapper for OrderService.

  The Order Service provides methods for creating, updating and retrieving
  orders.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits OrderService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock
      logger: Logger the instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    from dfp_api import API_VERSIONS
    from dfp_api.zsi_toolkit import SanityCheck
    if op_config['version'] in API_VERSIONS:
      web_services = __import__('dfp_api.zsi_toolkit.%s.%s_services'
                                % (op_config['version'],
                                   self.__class__.__name__), globals(),
                                locals(), [''])
    else:
      msg = 'Invalid API version, not one of %s.' % str(list(API_VERSIONS))
      raise ValidationError(msg)
    self.__web_services = web_services
    self.__loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self.__sanity_check = SanityCheck

  def CreateOrder(self, order):
    """Create a new order.

    Args:
      order: dict an order to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateOrder(order)

    method_name = 'createOrder'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'order': order},)),
                                     'Order', self.__loc, request)

  def CreateOrders(self, orders):
    """Create a list of new orders.

    Args:
      orders: list the orders to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((orders, list),))
    for item in orders:
      self.__sanity_check.ValidateOrder(item)

    method_name = 'createOrders'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'orders': orders},)),
                                     'Order', self.__loc, request)

  def GetOrder(self, order_id):
    """Return the order uniquely identified by the given id.

    Args:
      order_id: str ID of the order, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((order_id, (str, unicode)),))

    method_name = 'getOrder'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'orderId': order_id},)),
                                     'Order', self.__loc, request)

  def GetOrdersByFilter(self, filter):
    """Return the orders that match the given filter.

    Args:
      filter: str Publisher Query Language filter.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((filter, dict),))

    method_name = 'getOrdersByFilter'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'filter': filter},)),
                                     'Order', self.__loc, request)

  def PerformOrderAction(self, action, filter):
    """Perform action on orders that match the given filter.

    Args:
      action: str the action to perform.
      filter: str Publisher Query Language filter.

    Returns:
      tuple response from the API method.
    """
    web_services = self.__web_services
    action = self.__sanity_check.ValidateAction(action, web_services)
    self.__sanity_check.ValidateFilter(filter)

    method_name = 'performOrderAction'
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'orderAction': action},
                                                    {'filter': filter})),
                                     'Order', self.__loc, request)

  def UpdateOrder(self, order):
    """Update the specified order.

    Args:
      order: dict an order to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateOrder(order)

    method_name = 'updateOrder'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'order': order},)),
                                     'Order', self.__loc, request)

  def UpdateOrders(self, orders):
    """Update a list of specified orders.

    Args:
      orders: list the orders to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((orders, list),))
    for item in orders:
      self.__sanity_check.ValidateOrder(item)

    method_name = 'updateOrders'
    web_services = self.__web_services
    request = eval('web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name, (({'orders': orders},)),
                                     'Order', self.__loc, request)
