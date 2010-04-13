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

"""Classes for handling errors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'


class Error(Exception):

  """Implements Error.

  Responsible for handling exceptions.
  """

  def __init__(self, msg):
    self.message = msg

  def __str__(self):
    return str(self.message)

  def __call__(self):
    return (self.message,)


class DetailError(object):

  """Implements DetailError.

  Responsible for handling details of a user error.  Thrown as part of an
  ApiException.
  """

  def __init__(self, index=0, code=0, trigger='', fieldPath='', reason='',
               type=''):
    self.index = int(index)
    self.code = int(code)
    self.trigger = trigger
    self.field_path = fieldPath
    self.reason = reason
    self.type = type

  def __call__(self):
    return (self.index, self.code, self.trigger, self.fieldPath, self.reason,
            type)


class ApiError(Error):

  """Implements ApiException.

  Responsible for handling API exceptions.
  """

  def __init__(self, fault):
    (self.fault_code, self.fault_string) = ('', '')
    if 'faultcode' in fault:
      self.fault_code = fault['faultcode']
    if 'faultstring' in fault:
      self.fault_string = fault['faultstring']

    (self.code, self.message, self.trigger) = (-1, '', '')
    if 'detail' in fault and 'code' in fault['detail']:
      self.code = int(fault['detail']['code'])
    if 'detail' in fault and 'message' in fault['detail']:
      self.message = fault['detail']['message']
    elif not self.message:
      self.message = self.fault_string
    if 'detail' in fault and 'trigger' in fault['detail']:
      self.trigger = fault['detail']['trigger']

    self.errors = []
    errors = [None]
    if 'detail' in fault and 'errors' in fault['detail']:
      errors = fault['detail']['errors']
    elif 'detail' not in fault:
      errors[0] = {}
    else:
      errors[0] = fault['detail']
    for error in errors:
      # Keys need to be of type str not unicode.
      error_dct = dict([(str(key), value) for key, value in error.items()])
      if 'message' in error_dct:
        error_dct['detail'] = error_dct['message']
        del error_dct['message']
      # TODO(api.sgrinberg): Rework to get rid of the ** magic.
      self.errors.append(DetailError(**error_dct))

  def __str__(self):
    return self.fault_string

  def __call__(self):
    return (self.fault,)


class ApiAsStrError(Error):

  """Implements ApiAsStrError.

  Responsible for handling API exceptions that come in a form of a
  string.
  """

  def __init__(self, msg):
    lines = msg.split('\n')
    fault = {}
    for line in lines:
      if not line or line == 'Error:':
        continue
      try:
        (key, value) = line.split(': ', 1)
        fault[key] = value
      except:
        continue
    try:
      self.code = fault['code']
      self.msg = fault['message']
    except:
      # Unknown error code, likely a stackTrace was returned (see SOAP XML log).
      self.code = -1
      self.msg = fault['faultstring']

  def __str__(self):
    return 'Code %s: %s' % (self.code, self.msg)

  def __call__(self):
    return (self.code, self.msg,)


class InvalidInputError(Error):

  """Implements InvalidInputError.

  Responsible for handling invalid local input errors.
  """

  pass


class ValidationError(Error):

  """Implements ValidationError.

  Responsible for handling validation errors that are caught locally by the
  client library.
  """

  pass


class ApiVersionNotSupportedError(Error):

  """Implements ApiVersionNotSupportedError.

  Responsible for handling errors due to unsupported version of API.
  """

  pass


class MissingPackageError(Error):

  """Implements MissingPackageError.

  Responsible for handling missing package errors.
  """

  pass


class MalformedBufferError(Error):

  """Implements MalformedBufferError.

  Responsible for handling malformaed SOAP buffer errors.
  """

  pass


class AuthTokenError(Error):

  """Implements AuthTokenError.

  Responsible for handling auth token errors.
  """

  pass


class RequestError(ApiError):

  """Implements RequestError.

  Responsible for handling API errors
  """

  pass


class GoogleInternalError(ApiError):

  """Implements GoogleInternalError.

  Responsible for handling API errors
  """

  pass


class AuthenticationError(ApiError):

  """Implements AuthenticationError.

  Responsible for handling API errors
  """

  pass


# Map error codes and types to their corresponding classes.
ERRORS = {}
ERROR_TYPES = ['AdUnitAfcSizeError', 'AdUnitCodeError', 'ApiError',
               'AuthenticationError', 'CommonError', 'CreativeError',
               'FileError', 'FlashCreativeError', 'InternalApiError',
               'InvalidEmailError', 'InvalidUrlError',
               'InventoryTargetingError', 'LineItemCreativeAssociationError',
               'LineItemCreativeAssociationOperationError',
               'LineItemFlightDateError', 'LineItemOperationError',
               'NotNullError', 'NullError', 'OrderActionError', 'ParseError',
               'QuotaError', 'RangeError', 'RegExError',
               'RequiredCollectionError', 'RequiredError',
               'RequiredNumberError', 'RequiredSizeError',
               'ReservationDetailsError', 'ServerError', 'StringLengthError',
               'TypeError', 'UniqueError']
for index in ERROR_TYPES:
  if index in ('AdUnitAfcSizeError', 'AdUnitCodeError', 'ApiError',
               'CommonError', 'CreativeError', 'FileError',
               'FlashCreativeError', 'InvalidEmailError', 'InvalidUrlError',
               'InventoryTargetingError', 'LineItemCreativeAssociationError',
               'LineItemCreativeAssociationOperationError',
               'LineItemFlightDateError', 'LineItemOperationError',
               'NotNullError', 'NullError', 'OrderActionError', 'ParseError',
               'RangeError', 'RegExError', 'RequiredCollectionError',
               'RequiredError', 'RequiredNumberError', 'RequiredSizeError',
               'ReservationDetailsError', 'StringLengthError', 'TypeError',
               'UniqueError'):
    ERRORS[index] = RequestError
  elif index in ('InternalApiError', 'QuotaError', 'ServerError'):
    ERRORS[index] = GoogleInternalError
  elif index in ('AuthenticationError', 'InvalidEmailError'):
    ERRORS[index] = AuthenticationError
