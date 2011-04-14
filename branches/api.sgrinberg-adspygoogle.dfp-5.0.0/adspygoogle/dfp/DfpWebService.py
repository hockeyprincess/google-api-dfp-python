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

"""Methods for sending and recieving SOAP XML requests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import time

from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common.Errors import Error
from adspygoogle.common.WebService import WebService
from adspygoogle.dfp import DfpSanityCheck
from adspygoogle.dfp import AUTH_TOKEN_EXPIRE
from adspygoogle.dfp import AUTH_TOKEN_SERVICE
from adspygoogle.dfp import LIB_SIG
from adspygoogle.dfp import LIB_URL
from adspygoogle.dfp.DfpErrors import ERRORS
from adspygoogle.dfp.DfpErrors import DfpApiError
from adspygoogle.dfp.DfpErrors import DfpError
from adspygoogle.dfp.DfpSoapBuffer import DfpSoapBuffer


class DfpWebService(WebService):

  """Implements DfpWebService.

  Responsible for sending and recieving SOAP XML requests.
  """

  def __init__(self, headers, config, op_config, url, lock, logger=None):
    """Inits DfpWebService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      url: str URL of the web service to call.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    self.__config = config
    self.__op_config = op_config
    super(DfpWebService, self).__init__(LIB_SIG, headers, config, op_config,
                                        url, lock, logger)

  def __ManageSoap(self, buf, start_time, stop_time, error={}):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      start_time: str Time before service call was invoked.
      stop_time: str Time after service call was invoked.
      [optional]
      error: dict Error, if any.
    """
    try:
      # Set up log handlers.
      handlers = [
          {
              'tag': 'xml_log',
              'name': 'soap_xml',
              'data': ''
          },
          {
              'tag': 'request_log',
              'name': 'request_info',
              'data': str('host=%s service=%s method=%s responseTime=%s '
                          'requestId=%s'
                          % (Utils.GetNetLocFromUrl(self._url),
                             buf.GetServiceName(), buf.GetCallName(),
                             buf.GetCallResponseTime(), buf.GetCallRequestId()))
          },
          {
              'tag': '',
              'name': 'dfp_api_lib',
              'data': ''
          }
      ]

      fault = super(DfpWebService, self)._ManageSoap(
          buf, handlers, LIB_URL, ERRORS, start_time, stop_time, error)
      if fault:
        # Raise a specific error, subclass of DfpApiError.
        if 'detail' in fault:
          if 'code' in fault['detail']:
            code = int(fault['detail']['code'])
            if code in ERRORS: raise ERRORS[code](fault)
          elif 'errors' in fault['detail']:
            type = fault['detail']['errors'][0]['type']
            if type in ERRORS: raise ERRORS[str(type)](fault)

        if isinstance(fault, str):
          raise DfpError(fault)
        elif isinstance(fault, dict):
          raise DfpApiError(fault)
    except DfpApiError, e:
      raise e
    except DfpError, e:
      raise e
    except Error, e:
      if error: e = error
      raise Error(e)

  def CallMethod(self, method_name, params, service_name=None, loc=None,
                 request=None):
    """Make an API call to specified method.

    Args:
      method_name: str API method name.
      params: list List of parameters to send to the API method.
      [optional]
      service_name: str API service name.
      loc: service Locator.
      request: instance Holder of the SOAP request.

    Returns:
      tuple/str Response from the API method. If 'raw_response' flag enabled a
                string is returned, tuple otherwise.
    """
    # Acquire thread lock.
    self._lock.acquire()

    try:
      headers = self._headers
      config = self._config
      config['data_injects'] = ()
      error = {}

      # Load/set authentication token. If authentication token has expired,
      # regenerate it.
      now = time.time()
      if ((('authToken' not in headers and
            'auth_token_epoch' not in config) or
           int(now - config['auth_token_epoch']) >= AUTH_TOKEN_EXPIRE)):
        headers['authToken'] = Utils.GetAuthToken(
            headers['email'], headers['password'], AUTH_TOKEN_SERVICE,
            LIB_SIG, config['proxy'])
        config['auth_token_epoch'] = time.time()
        self._headers = headers
        self._config = config

      headers = Utils.UnLoadDictKeys(Utils.CleanUpDict(headers),
                                     ['email', 'password'])
      name_space = '/'.join(['https://www.google.com/apis/ads/publisher',
                             self._op_config['version']])
      config['ns_target'] = (name_space, 'RequestHeader')

      # Load new authentication headers, starting with version v201103.
      data_injects = []
      if self.__op_config['version'] > 'v201101':
        new_headers = {}
        for key in headers:
          if key == 'authToken' and headers[key]:
            if config['soap_lib'] == SOAPPY:
              data_injects.append(
                  ('<authentication>',
                   '<authentication xsi3:type="ClientLogin">'))
              config['data_injects'] = tuple(data_injects)
            else:
              config['auth_type'] = 'ClientLogin'
            new_headers['authentication'] = {'token': headers['authToken']}
          elif key == 'oAuthToken' and headers[key]:
            # TODO(api.sgrinberg): Add support for OAuth.
            pass
          else:
            new_headers[key] = headers[key]
        headers = new_headers

      buf = DfpSoapBuffer(
          xml_parser=self._config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self._config['pretty_xml']))

      start_time = time.strftime('%Y-%m-%d %H:%M:%S')
      response = super(DfpWebService, self).CallMethod(
          headers, config, method_name, params, buf,
          DfpSanityCheck.IsJaxbApi(self._op_config['version']), LIB_SIG,
          LIB_URL, service_name, loc, request)
      stop_time = time.strftime('%Y-%m-%d %H:%M:%S')

      # Restore list type which was overwritten by SOAPpy.
      if config['soap_lib'] == SOAPPY and isinstance(response, tuple):
        from adspygoogle.common.soappy import MessageHandler
        holder = []
        for element in response:
          holder.append(MessageHandler.RestoreListType(
              element, ('results', 'afcFormats', 'sizes', 'targetedAdUnitIds',
                        'excludedAdUnitIds', 'targetedPlacementIds',
                        'frequencyCaps', 'creativeSizes')))
        response = tuple(holder)

      if isinstance(response, dict) or isinstance(response, Error):
        error = response

      if not Utils.BoolTypeConvert(self.__config['raw_debug']):
        self.__ManageSoap(buf, start_time, stop_time, error)
    finally:
      # Release thread lock.
      if self._lock.locked():
        self._lock.release()

    if Utils.BoolTypeConvert(self._config['raw_response']):
      return response
    return response

  def CallRawMethod(self, soap_message):
    """Make an API call by posting raw SOAP XML message.

    Args:
      soap_message: str SOAP XML message.

    Returns:
      tuple Response from the API method.
    """
    # Acquire thread lock.
    self._lock.acquire()

    try:
      buf = DfpSoapBuffer(
          xml_parser=self._config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self._config['pretty_xml']))

      super(DfpWebService, self).CallRawMethod(
          buf, Utils.GetNetLocFromUrl(self._op_config['server']), soap_message)

      self.__ManageSoap(buf, self._start_time, self._stop_time,
                        {'data': buf.GetBufferAsStr()})
    finally:
      # Release thread lock.
      if self._lock.locked():
        self._lock.release()
    return (self._response,)
