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

from dfp_api import SanityCheck as glob_sanity_check
from dfp_api.Errors import ValidationError
from dfp_api.WebService import WebService


class LineItemService(object):

  """Wrapper for LineItemService.

  The LineItem Service provides methods for creating, updating and retrieving
  line items.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits LineItemService.

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
    self._web_services = web_services
    self.__loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self.__sanity_check = SanityCheck

  def CreateLineItem(self, line_item):
    """Create a new line item.

    Args:
      line_item: dict a line item to create.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateLineItem(line_item)

    method_name = 'createLineItem'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'lineItem': line_item},)),
                                     'LineItem', self.__loc, request)

  def CreateLineItems(self, line_items):
    """Create a list of new line item.

    Args:
      line_items: list the line item to create.

    Returns:
      tuple The response from the API method.
    """
    glob_sanity_check.ValidateTypes(((line_items, list),))
    for item in line_items:
      self.__sanity_check.ValidateLineItem(item)

    method_name = 'createLineItems'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'lineItems': line_items},)),
                                     'LineItem', self.__loc, request)

  def GetLineItem(self, line_item_id):
    """Return the line item uniquely identified by the given id.

    Args:
      line_item_id: str ID of the line item, which must already exist.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((line_item_id, (str, unicode)),))

    method_name = 'getLineItem'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'lineItemId': line_item_id},)),
                                     'LineItem', self.__loc, request)

  def GetLineItemsByStatement(self, filter_statement):
    """Return the line items that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of line items.

    Returns:
      tuple response from the API method.
    """
    filter_statement = self.__sanity_check.ValidateStatement(filter_statement,
                                                             self._web_services)

    method_name = 'getLineItemsByStatement'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'filterStatement': filter_statement},)),
                                     'LineItem', self.__loc, request)

  def PerformLineItemAction(self, action, filter_statement):
    """Perform action on line items that match the given filter.

    Args:
      action: dict the action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple response from the API method.
    """
    action = self.__sanity_check.ValidateAction(action, self._web_services)
    filter_statement = self.__sanity_check.ValidateStatement(filter_statement,
                                                             self._web_services)

    method_name = 'performLineItemAction'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'lineItemAction': action},
                                       {'filterStatement': filter_statement})),
                                     'LineItem', self.__loc, request)

  def UpdateLineItem(self, line_item):
    """Update the specified line item.

    Args:
      line_item: dict a line item to update.

    Returns:
      tuple response from the API method.
    """
    self.__sanity_check.ValidateLineItem(line_item)

    method_name = 'updateLineItem'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'lineItem': line_item},)),
                                     'LineItem', self.__loc, request)

  def UpdateLineItems(self, line_items):
    """Update a list of specified line items.

    Args:
      line_items: list the line items to update.

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((line_items, list),))
    for item in line_items:
      self.__sanity_check.ValidateLineItem(item)

    method_name = 'updateLineItems'
    request = eval('self._web_services.%sRequest()' % method_name)
    return self.__service.CallMethod(method_name,
                                     (({'lineItems': line_items},)),
                                     'LineItem', self.__loc, request)
