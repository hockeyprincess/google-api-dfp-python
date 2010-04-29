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

"""Interface for accessing all other services."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import pickle
import re
import thread
import time

from dfp_api import PYXML
from dfp_api import LIB_NAME
from dfp_api import LIB_SHORT_NAME
from dfp_api import LIB_VERSION
from dfp_api import MIN_API_VERSION
from dfp_api import SanityCheck
from dfp_api import Utils
from dfp_api.CompanyService import CompanyService
from dfp_api.CreativeService import CreativeService
from dfp_api.Errors import AuthTokenError
from dfp_api.Errors import ValidationError
from dfp_api.InventoryService import InventoryService
from dfp_api.LineItemCreativeAssociationService import LineItemCreativeAssociationService
from dfp_api.LineItemService import LineItemService
from dfp_api.Logger import Logger
from dfp_api.OrderService import OrderService
from dfp_api.PlacementService import PlacementService
from dfp_api.UserService import UserService
from dfp_api.WebService import WebService


class Client(object):

  """Provides entry point to all web services.

  Allows instantiation of every DFP API web service.
  """

  home = os.getcwd()
  auth_pkl = os.path.join(home, 'auth.pkl')
  config_pkl = os.path.join(home, 'config.pkl')

  def __init__(self, headers=None, config=None, path=None):
    """Inits Client.

    Args:
      [optional]
      headers: dict object with populated authentication credentials.
      config: dict object with client configuration values.
      path: str relative or absolute path to home directory (i.e. location of
            pickles and logs/).

        Ex:
          headers = {
            'email': 'johndoe@example.com',
            'password': 'secret',
            'applicationName': 'GoogleTest',
            'networkCode': 'ca-01234567',
          }
          config = {
            'home': '/path/to/home',
            'log_home': '/path/to/logs/home',
            'xml_parser': PYXML,
            'debug': 'n',
            'xml_log': 'y',
            'request_log': 'y',
            'raw_response': 'n',
            'use_strict': 'y',
            'use_pretty_xml': 'y',
            'access': ''
          }
          path = '/path/to/home'
    """
    self.__lock = thread.allocate_lock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of Client, based on provided
      # relative path.
      if os.path.isabs(path):
        Client.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to Client.home. Otherwise, may break when multiple
        # instances of Client exist during program run.
        Client.home = os.path.join(os.getcwd(), path)
      # Update location for both pickles.
      Client.auth_pkl = os.path.join(Client.home, 'auth.pkl')
      Client.config_pkl = os.path.join(Client.home, 'config.pkl')

    # Only load from the pickle if config wasn't specified.
    self.__config = config or self.__LoadConfigValues()
    self.__SetMissingDefaultConfigValues(self.__config)
    self.__config['home'] = Client.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self.__config['xml_parser'])

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self.__headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self.__config['use_strict']):
        SanityCheck.ValidateRequiredHeaders(headers)
      self.__headers = headers

    # Load/set authentication token.
    try:
      if headers and 'authToken' in headers and headers['authToken']:
        self.__headers['authToken'] = headers['authToken']
      elif 'email' in self.__headers and 'password' in self.__headers:
        self.__headers['authToken'] = Utils.GetAuthToken(
            self.__headers['email'], self.__headers['password'])
      else:
        msg = 'Authentication data, email or/and password, is missing.'
        raise ValidationError(msg)
      self.__config['auth_token_epoch'] = time.time()
    except AuthTokenError:
      # We would end up here if non-valid Google Account's credentials were
      # specified.
      self.__headers['authToken'] = None
      self.__config['auth_token_epoch'] = 0

    # Insert library name and version into application name.
    if (self.__headers['applicationName'].rfind(
        '%s v%s' % (LIB_SHORT_NAME, LIB_VERSION)) == -1):
      # Make sure library name shows up only once.
      if (self.__headers['applicationName'].rfind(LIB_SHORT_NAME) > -1 or
          self.__headers['applicationName'].rfind(LIB_NAME) > -1):
        pattern = re.compile('.*?: ')
        self.__headers['applicationName'] = pattern.sub(
            '', self.__headers['applicationName'], 1)
      self.__headers['applicationName'] = (
          '%s v%s: %s' % (LIB_SHORT_NAME, LIB_VERSION,
                          self.__headers['applicationName']))

      # Sync library's version in the new application name with the one in the
      # pickle.
      if headers is None:
        self.__WriteUpdatedAuthValue('applicationName',
                                     self.__headers['applicationName'])

    # Initialize logger.
    self.__logger = Logger(self.__config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from auth.pkl.

    Returns:
      dict dictionary object with populated authentication credentials.
    """
    auth = {}
    if os.path.exists(Client.auth_pkl):
      fh = open(Client.auth_pkl, 'r')
      try:
        auth = pickle.load(fh)
      finally:
        fh.close()

    if not auth:
      msg = 'Authentication data is missing.'
      raise ValidationError(msg)

    return auth

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in auth.pkl.

    Args:
      key: str a key to update.
      new_value: str a new value to update the key with.
    """
    auth = Client.__LoadAuthCredentials(self)
    auth[key] = new_value

    # Only write to an existing pickle.
    if os.path.exists(Client.auth_pkl):
      fh = open(Client.auth_pkl, 'w')
      try:
        pickle.dump(auth, fh)
      finally:
        fh.close()

  def __LoadConfigValues(self):
    """Load existing configuration values from config.pkl.

    Returns:
      dict dictionary object with populated configuration values.
    """
    config = {}
    if os.path.exists(Client.config_pkl):
      fh = open(Client.config_pkl, 'r')
      try:
        config = pickle.load(fh)
      finally:
        fh.close()

    if not config:
      # Proceed to set default config values.
      pass

    return config

  def __SetMissingDefaultConfigValues(self, config=None):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict object with client configuration values.
    """
    default_config = {
        'home': Client.home,
        'log_home': os.path.join(Client.home, 'logs'),
        'xml_parser': PYXML,
        'debug': 'n',
        'xml_log': 'y',
        'request_log': 'y',
        'raw_response': 'n',
        'use_strict': 'y',
        'auth_token_epoch': 0,
        'use_pretty_xml': 'y',
        'access': ''
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]

  def GetAuthCredentials(self):
    """Return authentication credentials.

    Returns:
      dict authentiaction credentials.
    """
    return self.__headers

  def GetConfigValues(self):
    """Return configuration values.

    Returns:
      dict configuration values.
    """
    return self.__config

  def SetDebug(self, new_state):
    """Temporarily change debug mode for a given Client instance.

    Args:
      new_state: bool new state of the debug mode.
    """
    self.__config['debug'] = Utils.BoolTypeConvert(new_state)

  def __GetDebug(self):
    """Return current state of the debug mode.

    Returns:
      bool state of the debug mode.
    """
    return self.__config['debug']

  def __SetDebug(self, new_state):
    """Temporarily change debug mode for a given Client instance.

    Args:
      new_state: bool new state of the debug mode.
    """
    self.__config['debug'] = Utils.BoolTypeConvert(new_state)

  debug = property(__GetDebug, __SetDebug)

  def __GetUseStrict(self):
    """Return current state of the strictness mode.

    Returns:
      str state of the strictness mode.
    """
    return self.__config['use_strict']

  def __SetUseStrict(self, new_state):
    """Temporarily change strictness mode for a given Client instance.

    Args:
      new_state: bool new state of the strictness mode.
    """
    self.__config['use_strict'] = Utils.BoolTypeConvert(new_state)

  use_strict = property(__GetUseStrict, __SetUseStrict)

  def __GetXmlParser(self):
    """Return current state of the xml parser in use.

    Returns:
      bool state of the xml parser in use.
    """
    return self.__config['xml_parser']

  def __SetXmlParser(self, new_state):
    """Temporarily change xml parser in use for a given Client instance.

    Args:
      new_state: bool new state of the xml parser to use.
    """
    self.__config['xml_parser'] = Utils.BoolTypeConvert(new_state)

  xml_parser = property(__GetXmlParser, __SetXmlParser)

  def CallRawMethod(self, soap_message, url, http_proxy):
    """Call API method directly, using raw SOAP message.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      soap_message: str SOAP XML message.
      url: str URL of the API service for the method to call.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple response from the API method (SOAP XML response message).
    """
    headers = self.__headers

    # Load additional configuration data.
    op_config = {'http_proxy': http_proxy}

    service = WebService(headers, self.__config, op_config, url, self.__lock,
                         self.__logger)
    return service.CallRawMethod(soap_message)

  def CallMethod(self, url, method, params, http_proxy):
    """Call API method directly, using its service's URL.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      url: str URL of the API service for the method to call.
      method: str name of the API method to call.
      params: list list of parameters to send to the API method.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple response from the API method.
    """
    headers = self.__headers

    # Load additional configuration data.
    op_config = {
      'server': Utils.GetServerFromUrl(url),
      'version': Utils.GetVersionFromUrl(url),
      'http_proxy': http_proxy
    }

    service = WebService(headers, self.__config, op_config, url, self.__lock,
                         self.__logger)

    # Check format of parameters. Example of valid formats,
    # - ()
    # - ({'dummy': 0},)
    # - ({'campaignIds': ['11111']},
    #    {'startDay': '2008-07-01'},
    #    {'endDay': '2008-07-31'})
    #
    # TODO(api.sgrinberg): Figure out how to match the order of params with
    # those in Holder object below. Then, we don't need to require client code
    # to provide key/value pairs, just values will be enough (see, issue# 31).
    try:
      SanityCheck.ValidateTypes(((params, tuple),))
      for item in params:
        SanityCheck.ValidateTypes(((item, dict),))
    except ValidationError:
      msg = 'Invalid format of parameters, expecting a tuple of dicts.'
      raise ValidationError(msg)

    # From the URL, get service being accessed and version used.
    url_parts = url.split('/')
    service_name = url_parts[len(url_parts) - 1].split('Service')[0]
    version = url_parts[len(url_parts) - 2]

    web_services = __import__('dfp_api.zsi_toolkit.%s.%sService_services'
                              % (version, service_name), globals(),
                              locals(), [''])
    eval('%sService' % service_name).web_services = web_services
    self.__loc = eval(('%sService.web_services.%sServiceLocator()'
                       % (service_name, service_name)))
    request = eval('%sService.web_services.%sRequest()' % (service_name,
                                                           method))
    return service.CallMethod(method, (params), service_name, self.__loc,
                              request)

  # TODO(api.sgrinberg): When API launches in production, change default server.
  def GetCompanyService(self, server='https://sandbox.google.com', version=None,
                        http_proxy=None):
    """Call API method in CompanyService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CompanyService new instance of CompanyService object.
    """
    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return CompanyService(self.__headers, self.__config, op_config, self.__lock,
                          self.__logger)

  def GetCreativeService(self, server='https://sandbox.google.com',
                         version=None, http_proxy=None):
    """Call API method in CreativeService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CreativeService new instance of CreativeService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return CreativeService(headers, self.__config, op_config, self.__lock,
                           self.__logger)

  def GetInventoryService(self, server='https://sandbox.google.com',
                          version=None, http_proxy=None):
    """Call API method in InventoryService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      InventoryService new instance of InventoryService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return InventoryService(headers, self.__config, op_config, self.__lock,
                            self.__logger)

  def GetLineItemCreativeAssociationService(self,
                                            server='https://sandbox.google.com',
                                            version=None, http_proxy=None):
    """Call API method in LineItemCreativeAssociationService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      LineItemCreativeAssociationService new instance of
          LineItemCreativeAssociationService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return LineItemCreativeAssociationService(headers, self.__config, op_config,
                                              self.__lock, self.__logger)

  def GetLineItemService(self, server='https://sandbox.google.com',
                         version=None, http_proxy=None):
    """Call API method in LineItemService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      LineItemService new instance of LineItemService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return LineItemService(headers, self.__config, op_config, self.__lock,
                           self.__logger)

  def GetOrderService(self, server='https://sandbox.google.com', version=None,
                      http_proxy=None):
    """Call API method in OrderService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      OrderService new instance of OrderService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return OrderService(headers, self.__config, op_config, self.__lock,
                        self.__logger)

  def GetPlacementService(self, server='https://sandbox.google.com',
                          version=None, http_proxy=None):
    """Call API method in PlacementService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      PlacementService new instance of PlacementService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return PlacementService(headers, self.__config, op_config, self.__lock,
                            self.__logger)

  def GetUserService(self, server='https://sandbox.google.com', version=None,
                     http_proxy=None):
    """Call API method in UserService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      UserService new instance of UserService object.
    """
    headers = self.__headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return UserService(headers, self.__config, op_config, self.__lock,
                       self.__logger)
