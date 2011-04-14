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
import re
import thread
import time

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Client import Client
from adspygoogle.common.Errors import AuthTokenError
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.Logger import Logger
from adspygoogle.dfp import AUTH_TOKEN_SERVICE
from adspygoogle.dfp import LIB_SHORT_NAME
from adspygoogle.dfp import LIB_SIG
from adspygoogle.dfp import MIN_API_VERSION
from adspygoogle.dfp import REQUIRED_SOAP_HEADERS
from adspygoogle.dfp import DfpSanityCheck
from adspygoogle.dfp.CompanyService import CompanyService
from adspygoogle.dfp.CreativeService import CreativeService
from adspygoogle.dfp.CustomTargetingService import CustomTargetingService
from adspygoogle.dfp.DfpWebService import DfpWebService
from adspygoogle.dfp.ForecastService import ForecastService
from adspygoogle.dfp.InventoryService import InventoryService
from adspygoogle.dfp.LineItemCreativeAssociationService import LineItemCreativeAssociationService
from adspygoogle.dfp.LineItemService import LineItemService
from adspygoogle.dfp.NetworkService import NetworkService
from adspygoogle.dfp.OrderService import OrderService
from adspygoogle.dfp.PlacementService import PlacementService
from adspygoogle.dfp.PublisherQueryLanguageService import PublisherQueryLanguageService
from adspygoogle.dfp.ReportService import ReportService
from adspygoogle.dfp.UserService import UserService


class DfpClient(Client):

  """Provides entry point to all web services.

  Allows instantiation of all DFP API web services.
  """

  auth_pkl_name = 'dfp_api_auth.pkl'
  config_pkl_name = 'dfp_api_config.pkl'

  def __init__(self, headers=None, config=None, path=None):
    """Inits Client.

    Args:
      [optional]
      headers: dict Object with populated authentication credentials.
      config: dict Object with client configuration values.
      path: str Relative or absolute path to home directory (i.e. location of
            pickles and logs/).

      Ex:
        headers = {
          'email': 'johndoe@example.com',
          'password': 'secret',
          'authToken': '...',
          'applicationName': 'GoogleTest',
          'networkCode': 'ca-01234567',
        }
        config = {
          'home': '/path/to/home',
          'log_home': '/path/to/logs/home',
          'proxy': 'http://example.com:8080',
          'soap_lib': ZSI,
          'xml_parser': PYXML,
          'debug': 'n',
          'raw_debug': 'n',
          'xml_log': 'y',
          'request_log': 'y',
          'raw_response': 'n',
          'strict': 'y',
          'pretty_xml': 'y',
          'compress': 'y',
          'access': ''
        }
        path = '/path/to/home'
    """
    super(DfpClient, self).__init__(headers, config, path)

    self.__lock = thread.allocate_lock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of DfpClient, based on
      # provided relative path.
      if os.path.isabs(path):
        DfpClient.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to DfpClient.home. Otherwise, may break when
        # multiple instances of DfpClient exist during program run.
        DfpClient.home = os.path.join(os.getcwd(), path)

      # If pickles don't exist at given location, default to "~".
      if (not headers and not config and
          (not os.path.exists(os.path.join(DfpClient.home,
                                           DfpClient.auth_pkl_name)) or
           not os.path.exists(os.path.join(DfpClient.home,
                                           DfpClient.config_pkl_name)))):
        DfpClient.home = os.path.expanduser('~')
    else:
      DfpClient.home = os.path.expanduser('~')

    # Update location for both pickles.
    DfpClient.auth_pkl = os.path.join(DfpClient.home,
                                      DfpClient.auth_pkl_name)
    DfpClient.config_pkl = os.path.join(DfpClient.home,
                                        DfpClient.config_pkl_name)

    # Only load from the pickle if config wasn't specified.
    self._config = config or self.__LoadConfigValues()
    self._config = self.__SetMissingDefaultConfigValues(self._config)
    self._config['home'] = DfpClient.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self._config['xml_parser'])

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self._headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self._config['strict']):
        SanityCheck.ValidateRequiredHeaders(headers, REQUIRED_SOAP_HEADERS)
      self._headers = headers

    # Load/set authentication token.
    try:
      if headers and 'authToken' in headers and headers['authToken']:
        self._headers['authToken'] = headers['authToken']
      elif 'email' in self._headers and 'password' in self._headers:
        self._headers['authToken'] = Utils.GetAuthToken(
            self._headers['email'], self._headers['password'],
            AUTH_TOKEN_SERVICE, LIB_SIG, self._config['proxy'])
      else:
        msg = 'Authentication data, email or/and password, is missing.'
        raise ValidationError(msg)
      self._config['auth_token_epoch'] = time.time()
    except AuthTokenError:
      # We would end up here if non-valid Google Account's credentials were
      # specified.
      self._headers['authToken'] = None
      self._config['auth_token_epoch'] = 0

    # Insert library's signature into application name.
    if self._headers['applicationName'].rfind(LIB_SIG) == -1:
      # Make sure library name shows up only once.
      if self._headers['applicationName'].rfind(LIB_SHORT_NAME) > -1:
        pattern = re.compile('.*\|')
        self._headers['applicationName'] = pattern.sub(
            '', self._headers['applicationName'], 1)
      self._headers['applicationName'] = (
          '%s|%s' % (LIB_SIG, self._headers['applicationName']))

      # Sync library's version in the new application name with the one in the
      # pickle.
      if headers is None:
        self.__WriteUpdatedAuthValue('applicationName',
                                     self._headers['applicationName'])

    # Initialize logger.
    self.__logger = Logger(LIB_SIG, self._config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from dfp_api_auth.pkl.

    Returns:
      dict Dictionary object with populated authentication credentials.
    """
    return super(DfpClient, self)._LoadAuthCredentials()

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in dfp_api_auth.pkl.

    Args:
      key: str Key to update.
      new_value: str New value to update the key with.
    """
    super(DfpClient, self)._WriteUpdatedAuthValue(key, new_value)

  def __LoadConfigValues(self):
    """Load existing configuration values from dfp_api_config.pkl.

    Returns:
      dict Dictionary object with populated configuration values.
    """
    return super(DfpClient, self)._LoadConfigValues()

  def __SetMissingDefaultConfigValues(self, config={}):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict Object with client configuration values.
    """
    config = super(DfpClient, self)._SetMissingDefaultConfigValues(config)
    default_config = {
        'home': DfpClient.home,
        'log_home': os.path.join(DfpClient.home, 'logs')
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]
    return config

  def CallRawMethod(self, soap_message, url, server, http_proxy):
    """Call API method directly, using raw SOAP message.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      soap_message: str SOAP XML message.
      url: str URL of the API service for the method to call.
      server: str API server to access for this API call.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple Response from the API method (SOAP XML response message).
    """
    headers = self._headers

    # Load additional configuration data.
    op_config = {
      'http_proxy': http_proxy,
      'server': server
    }

    service = DfpWebService(headers, self._config, op_config, url, self.__lock,
                            self.__logger)
    return service.CallRawMethod(soap_message)

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
      CompanyService New instance of CompanyService object.
    """
    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CompanyService(self._headers, self._config, op_config, self.__lock,
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
      CreativeService New instance of CreativeService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CreativeService(headers, self._config, op_config, self.__lock,
                           self.__logger)

  def GetCustomTargetingService(self, server='https://sandbox.google.com',
                                version=None, http_proxy=None):
    """Call API method in CustomTargetingService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CustomTargetingService New instance of CustomTargetingService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CustomTargetingService(headers, self._config, op_config, self.__lock,
                                  self.__logger)

  def GetForecastService(self, server='https://sandbox.google.com',
                         version=None, http_proxy=None):
    """Call API method in ForecastService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ForecastService New instance of ForecastService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return ForecastService(headers, self._config, op_config, self.__lock,
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
      InventoryService New instance of InventoryService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return InventoryService(headers, self._config, op_config, self.__lock,
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
      LineItemCreativeAssociationService New instance of
          LineItemCreativeAssociationService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return LineItemCreativeAssociationService(headers, self._config, op_config,
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
      LineItemService New instance of LineItemService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return LineItemService(headers, self._config, op_config, self.__lock,
                           self.__logger)

  def GetNetworkService(self, server='https://sandbox.google.com', version=None,
                        http_proxy=None):
    """Call API method in NetworkService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      NetworkService New instance of NetworkService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return NetworkService(headers, self._config, op_config, self.__lock,
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
      OrderService New instance of OrderService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return OrderService(headers, self._config, op_config, self.__lock,
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
      PlacementService New instance of PlacementService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return PlacementService(headers, self._config, op_config, self.__lock,
                            self.__logger)

  def GetPublisherQueryLanguageService(self,
                                       server='https://sandbox.google.com',
                                       version=None, http_proxy=None):
    """Call API method in PublisherQueryLanguageService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      PublisherQueryLanguageService New instance of
                                    PublisherQueryLanguageService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return PublisherQueryLanguageService(headers, self._config, op_config,
                                         self.__lock, self.__logger)

  def GetReportService(self, server='https://sandbox.google.com',
                       version=None, http_proxy=None):
    """Call API method in ReportService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ReportService New instance of ReportService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return ReportService(headers, self._config, op_config, self.__lock,
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
      UserService New instance of UserService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return UserService(headers, self._config, op_config, self.__lock,
                       self.__logger)
