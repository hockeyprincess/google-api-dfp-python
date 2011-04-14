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

"""Validation and type conversion functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import Utils
from adspygoogle.common import SanityCheck
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.zsi import SanityCheck as ZsiSanityCheck


def ValidateCompany(company):
  """Validate Company object.

  Args:
    company: dict Company object.
  """
  SanityCheck.ValidateOneLevelObject(company)


def ValidateString_ParamMapEntry(param, web_services):
  """Validate String_ParamMapEntry object.

  Args:
    param: dict Param object.
    web_services: module Web services.

  Returns:
   String_ParamMapEntry instance.
  """
  if ZsiSanityCheck.IsPyClass(param):
    return param

  SanityCheck.ValidateTypes(((param, dict),))
  new_param = ZsiSanityCheck.GetPyClass('String_ParamMapEntry', web_services)
  for key in param:
    SanityCheck.ValidateTypes(((param[key], (str, unicode)),))
    if key in ('value',):
      if 'xsi_type' in param:
        value = ZsiSanityCheck.GetPyClass(param['xsi_type'], web_services)
      elif 'type' in param:
        value = ZsiSanityCheck.GetPyClass(param['type'], web_services)
      else:
        msg = ('The type of the param is missing.')
        raise ValidationError(msg)
      value.__dict__.__setitem__('_%s' % key, param[key])
      data = value
    else:
      data = param[key]
    new_param.__dict__.__setitem__('_%s' % key, data)
  return new_param


def ValidateString_ValueMapEntry(value, web_services):
  """Validate String_ValueMapEntry object.

  Args:
    value: dict Value object.
    web_services: module Web services.

  Returns:
   String_ValueMapEntry instance.
  """
  if ZsiSanityCheck.IsPyClass(value):
    return value

  SanityCheck.ValidateTypes(((value, dict),))
  new_value = ZsiSanityCheck.GetPyClass('String_ValueMapEntry', web_services)
  for key in value:
    if key in ('value',):
      SanityCheck.ValidateTypes(((value[key], dict),))
      if 'xsi_type' in value[key]:
        value_obj = ZsiSanityCheck.GetPyClass(value[key]['xsi_type'],
                                              web_services)
      else:
        msg = ('The \'xsi_type\' of the value is missing.')
        raise ValidationError(msg)
      for sub_key in value[key]:
        value_obj.__dict__.__setitem__('_%s' % sub_key, value[key][sub_key])
      data = value_obj
    else:
      SanityCheck.ValidateTypes(((value[key], (str, unicode)),))
      data = value[key]
    new_value.__dict__.__setitem__('_%s' % key, data)
  return new_value


def ValidateStatement(statement, web_services):
  """Validate Statement object.

  Args:
    statement: dict Statement object.
    web_services: module Web services.

  Returns:
    Statement instance.
  """
  if ZsiSanityCheck.IsPyClass(statement):
    return statement

  SanityCheck.ValidateTypes(((statement, dict),))
  new_statement = ZsiSanityCheck.GetPyClass('Statement', web_services)
  for key in statement:
    if key in ('params',):
      SanityCheck.ValidateTypes(((statement[key], list),))
      if len(statement[key]) > 1:
        msg = ('Map \'params\' must contain a single element in the list.')
        raise ValidationError(msg)
      params = []
      for param in statement[key]:
        params.append(ValidateString_ParamMapEntry(param, web_services))
      data = params
    elif key in ('values',):
      SanityCheck.ValidateTypes(((statement[key], list),))
      if len(statement[key]) > 1:
        msg = ('Map \'values\' must contain a single element in the list.')
        raise ValidationError(msg)
      values = []
      for value in statement[key]:
        values.append(ValidateString_ValueMapEntry(value, web_services))
      data = values
    else:
      SanityCheck.ValidateTypes(((statement[key], (str, unicode)),))
      data = statement[key]
    new_statement.__dict__.__setitem__('_%s' % key, data)
  return new_statement


def ValidateSize(size):
  """Validate Size object.

  Args:
    size: dict Size object.
  """
  SanityCheck.ValidateOneLevelObject(size)


def ValidateCreative(creative, web_services):
  """Validate Creative object.

  Args:
    creative: dict Creative object.
    web_services: module Web services.

  Returns:
    Creative instance.
  """
  if ZsiSanityCheck.IsPyClass(creative):
    return creative

  SanityCheck.ValidateTypes(((creative, dict),))
  if 'creativeType' in creative:
    new_creative = ZsiSanityCheck.GetPyClass(creative['creativeType'],
                                             web_services)
  elif 'Creative_Type' in creative:
    new_creative = ZsiSanityCheck.GetPyClass(creative['Creative_Type'],
                                             web_services)
  elif 'xsi_type' in creative:
    new_creative = ZsiSanityCheck.GetPyClass(creative['xsi_type'], web_services)
  elif 'type' in creative:
    new_creative = ZsiSanityCheck.GetPyClass(creative['type'], web_services)
  else:
    msg = ('The type of the creative is missing.')
    raise ValidationError(msg)
  for key in creative:
    if creative[key] == 'None': continue
    if key in ('size', 'flashAssetSize', 'fallbackAssetSize', 'assetSize'):
      ValidateSize(creative[key])
      new_size = ZsiSanityCheck.GetPyClass('Size', web_services)
      for sub_key in creative[key]:
        new_size.__dict__.__setitem__('_%s' % sub_key, creative[key][sub_key])
      data = new_size
    else:
      SanityCheck.ValidateTypes(((creative[key], (str, unicode)),))
      data = creative[key]
    new_creative.__dict__.__setitem__('_%s' % key, data)
  return new_creative


def ValidateSize_StringMapEntry(map_entry):
  """Validate Size_StringMapEntry object.

  Args:
    map_entry: dict Size_StringMapEntry object.
  """
  SanityCheck.ValidateTypes(((map_entry, dict),))
  for key in map_entry:
    if map_entry[key] == 'None': continue
    if key in ('key',):
      ValidateSize(map_entry[key])
    else:
      SanityCheck.ValidateTypes(((map_entry[key], (str, unicode)),))


def ValidateAdSenseSettings(settings):
  """Validate AdSenseSettings object.

  Args:
    settings: dict AdSenseSettings object.
  """
  SanityCheck.ValidateTypes(((settings, dict),))
  for key in settings:
    if settings[key] == 'None': continue
    if key in ('afcFormats',):
      SanityCheck.ValidateTypes(((settings[key], list),))
      for item in settings[key]:
        ValidateSize_StringMapEntry(item)
    else:
      SanityCheck.ValidateTypes(((settings[key], (str, unicode)),))


def ValidateInheritedPropertySource(property_source):
  """Validate InheritedPropertySource object.

  Args:
    property_source: dict InheritedPropertySource object.
  """
  SanityCheck.ValidateOneLevelObject(property_source)


def ValidateAdSenseSettingsInheritedProperty(property):
  """Validate AdSenseSettingsInheritedProperty object.

  Args:
    property: dict AdSenseSettingsInheritedProperty object.
  """
  SanityCheck.ValidateTypes(((property, dict),))
  for key in property:
    if property[key] == 'None': continue
    if key in ('value',):
      ValidateAdSenseSettings(property[key])
    elif key in ('valueSource',):
      ValidateInheritedPropertySource(property[key])


def ValidateAdUnit(ad_unit):
  """Validate AdUnit object.

  Args:
    ad_unit: dict AdUnit object.
  """
  SanityCheck.ValidateTypes(((ad_unit, dict),))
  for key in ad_unit:
    if ad_unit[key] == 'None': continue
    if key in ('inheritedAdSenseSettings',):
      ValidateAdSenseSettingsInheritedProperty(ad_unit[key])
    elif key in ('sizes',):
      SanityCheck.ValidateTypes(((ad_unit[key], list),))
      for item in ad_unit[key]:
        ValidateSize(item)
    else:
      SanityCheck.ValidateTypes(((ad_unit[key], (str, unicode)),))


def ValidateDate(date):
  """Validate Date object.

  Args:
    date: dict Date object.
  """
  SanityCheck.ValidateOneLevelObject(date)


def ValidateDateTime(date_time):
  """Validate DateTime object.

  Args:
    date_time: dict DateTime object.
  """
  SanityCheck.ValidateTypes(((date_time, dict),))
  for key in date_time:
    if date_time[key] == 'None': continue
    if key in ('date',):
      ValidateDate(date_time[key])
    else:
      SanityCheck.ValidateTypes(((date_time[key], (str, unicode)),))


def ValidateMoney(money):
  """Validate Money object.

  Args:
    money: dict Money object.
  """
  SanityCheck.ValidateOneLevelObject(money)


def ValidateOrder(order):
  """Validate Order object.

  Args:
    order: dict Order object.
  """
  SanityCheck.ValidateTypes(((order, dict),))
  for key in order:
    if order[key] == 'None': continue
    if key in ('startDateTime', 'endDateTime'):
      ValidateDateTime(order[key])
    elif key in ('totalBudget',):
      ValidateMoney(order[key])
    else:
      SanityCheck.ValidateTypes(((order[key], (str, unicode)),))


def ValidateUser(user):
  """Validate User object.

  Args:
    user: dict User object.
  """
  SanityCheck.ValidateOneLevelObject(user)


def ValidateFrequencyCap(cap):
  """Validate FrequencyCap object.

  Args:
    cap: dict FrequencyCap object.
  """
  SanityCheck.ValidateOneLevelObject(cap)


def ValidateCustomCriteria(criteria, web_services):
  """Validate CustomCriteria object.

  Args:
    criteria: dict CustomCriteria object.
    web_services: module Web services.

  Returns:
    CustomCriteria instance.
  """
  if ZsiSanityCheck.IsPyClass(criteria): return criteria

  SanityCheck.ValidateTypes(((criteria, dict),))
  new_criteria = ZsiSanityCheck.GetPyClass(criteria['xsi_type'], web_services)
  for key in criteria:
    if key in ('values',):
      values = []
      for item in criteria[key]:
        SanityCheck.ValidateTypes(((item, dict),))
        value = ZsiSanityCheck.GetPyClass('CustomTargetingValue', web_services)
        for sub_key in item:
          SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
          value.__dict__.__setitem__('_%s' % sub_key, item[sub_key])
        values.append(value)
      data = values
    elif key in ('valueIds',):
      SanityCheck.ValidateTypes(((criteria[key], list),))
      for item in criteria[key]:
        SanityCheck.ValidateTypes(((item, (str, unicode)),))
      data = criteria[key]
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))
      data = criteria[key]
    new_criteria.__dict__.__setitem__('_%s' % key, data)
  return new_criteria


def ValidateCustomCriteriaSet(criteria_set, web_services):
  """Validate CustomCriteriaSet object.

  Args:
    criteria_set: dict CustomCriteriaSet object.
    web_services: module Web services.

  Returns:
    CustomCriteriaSet instance.
  """
  if ZsiSanityCheck.IsPyClass(criteria_set): return criteria_set

  SanityCheck.ValidateTypes(((criteria_set, dict),))
  new_set = ZsiSanityCheck.GetPyClass(criteria_set['xsi_type'], web_services)
  for key in criteria_set:
    if key in ('children',):
      SanityCheck.ValidateTypes(((criteria_set[key], list),))
      children = []
      for item in criteria_set[key]:
        if 'xsi_type' in item:
          if item['xsi_type'] in ('FreeFormCustomCriteria',
                                  'PredefinedCustomCriteria'):
            children.append(ValidateCustomCriteria(item, web_services))
          else:
            children.append(ValidateCustomCriteriaSet(item, web_services))
        else:
          msg = 'The \'xsi_type\' of node is missing.'
          raise ValidationError(msg)
      data = children
    else:
      SanityCheck.ValidateTypes(((criteria_set[key], (str, unicode)),))
      data = criteria_set[key]
    new_set.__dict__.__setitem__('_%s' % key, data)
  return new_set


def ValidateDayPart(part):
  """Validate DayPart object.

  Args:
    part: dict DayPart object.
  """
  SanityCheck.ValidateTypes(((part, dict),))
  for key in part:
    if part[key] == 'None': continue
    if key in ('startTime', 'endTime'):
      ValidateDate(part[key])
    else:
      SanityCheck.ValidateTypes(((part[key], (str, unicode)),))


def ValidateTargeting(targeting, web_services):
  """Validate Targeting object.

  Args:
    targeting: dict Targeting object.
    web_services: module Web services.

  Returns:
    Targeting instance.
  """
  if ZsiSanityCheck.IsPyClass(targeting): return targeting

  SanityCheck.ValidateTypes(((targeting, dict),))
  for key in targeting:
    if targeting[key] == 'None' or not targeting[key]: continue
    if key in ('inventoryTargeting', 'geoTargeting'):
      SanityCheck.ValidateTypes(((targeting[key], dict),))
      target = targeting[key]
      for sub_key in target:
        SanityCheck.ValidateTypes(((target[sub_key], list),))
        targets = []
        for item in target[sub_key]:
          if key in ('inventoryTargeting',):
            SanityCheck.ValidateTypes(((item, (str, unicode)),))
            targets.append(item)
          elif key in ('geoTargeting',):
            SanityCheck.ValidateTypes(((item, dict),))
            if 'xsi_type' in item:
              location = ZsiSanityCheck.GetPyClass(item['xsi_type'],
                                                   web_services)
            else:
              msg = 'The \'xsi_type\' of the geo targeting location is missing.'
              raise ValidationError(msg)
            for sub_sub_key in item:
              SanityCheck.ValidateTypes(((item[sub_sub_key], (str, unicode)),))
              location.__dict__.__setitem__('_%s' % sub_sub_key,
                                            item[sub_sub_key])
            targets.append(location)
        # If value is an empty list, remove key from the dictionary.
        if not target[sub_key]:
          target = Utils.UnLoadDictKeys(target, [sub_key])
        target[sub_key] = targets
      data = target
    elif key in ('customTargeting',):
      data = ValidateCustomCriteriaSet(targeting[key], web_services)
    elif key in ('dayPartTargeting', 'userDomainTargeting'):
      SanityCheck.ValidateTypes(((targeting[key], dict),))
      target = targeting[key]
      for sub_key in target:
        if sub_key in ('dayParts',):
          SanityCheck.ValidateTypes(((target[sub_key], list),))
          targets = []
          for item in target[sub_key]:
            ValidateDayPart(item)
        elif sub_key in ('domains',):
          SanityCheck.ValidateTypes(((target[sub_key], list),))
          for item in target[sub_key]:
            SanityCheck.ValidateTypes(((item, (str, unicode)),))
        else:
          SanityCheck.ValidateTypes(((target[sub_key], (str, unicode)),))
      data = target
  return data


def ValidateLineItem(line_item, web_services):
  """Validate LineItem object.

  Args:
    line_item: dict LineItem object.
    web_services: module Web services.
  """
  SanityCheck.ValidateTypes(((line_item, dict),))
  for key in line_item:
    if line_item[key] == 'None': continue
    if key in ('creativeSizes',):
      SanityCheck.ValidateTypes(((line_item[key], list),))
      for item in line_item[key]:
        ValidateSize(item)
    elif key in ('startDateTime', 'endDateTime'):
      ValidateDateTime(line_item[key])
    elif key in ('costPerUnit', 'valueCostPerUnit', 'budget'):
      ValidateMoney(line_item[key])
    elif key in ('frequencyCaps',):
      SanityCheck.ValidateTypes(((line_item[key], list),))
      for item in line_item[key]:
        ValidateFrequencyCap(item)
    elif key in ('targeting',):
      ValidateTargeting(line_item[key], web_services)
    else:
      SanityCheck.ValidateTypes(((line_item[key], (str, unicode)),))


def ValidateLica(lica):
  """Validate LineItemCreativeAssociation object.

  Args:
    lica: dict LineItemCreativeAssociation object.
  """
  SanityCheck.ValidateTypes(((lica, dict),))
  for key in lica:
    if lica[key] == 'None': continue
    if key in ('startTime', 'endTime'):
      ValidateDateTime(lica[key])
    elif key in ('sizes',):
      SanityCheck.ValidateTypes(((lica[key], list),))
      for item in lica[key]:
        ValidateSize(item)
    else:
      SanityCheck.ValidateTypes(((lica[key], (str, unicode)),))


def ValidatePlacement(placement):
  """Validate Placement object.

  Args:
    placement: dict Placement object.
  """
  SanityCheck.ValidateTypes(((placement, dict),))
  for key in placement:
    if placement[key] == 'None': continue
    if key in ('targetedAdUnitIds',):
      SanityCheck.ValidateTypes(((placement[key], list),))
      for item in placement[key]:
        SanityCheck.ValidateTypes(((item, (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((placement[key], (str, unicode)),))


def ValidateAction(action, web_services):
  """Validate Action object.

  Args:
    action: dict Action to perform.
    web_services: module Web services.

  Returns:
    Action instance.
  """
  if ZsiSanityCheck.IsPyClass(action): return action

  SanityCheck.ValidateTypes(((action, dict),))
  if 'xsi_type' in action:
    new_action = ZsiSanityCheck.GetPyClass(action['xsi_type'], web_services)
  elif 'type' in action:
    new_action = ZsiSanityCheck.GetPyClass(action['type'], web_services)
  else:
    msg = 'The type of the action is missing.'
    raise ValidationError(msg)
  for key in action:
    SanityCheck.ValidateTypes(((action[key], (str, unicode)),))
    new_action.__dict__.__setitem__('_%s' % key, action[key])
  return new_action


def ValidateReportQuery(report_query):
  """Validate ReportQuery object.

  Args:
    report_query: dict ReportQuery object.
  """
  SanityCheck.ValidateTypes(((report_query, dict),))
  for key in report_query:
    if key in ('dimensions', 'columns', 'dimensionFilters'):
      SanityCheck.ValidateTypes(((report_query[key], list),))
      for item in report_query[key]:
        SanityCheck.ValidateTypes(((item, (str, unicode)),))
    elif key in ('startDateTime', 'startDate', 'endDateTime', 'endDate'):
      ValidateDateTime(report_query[key])
    else:
      SanityCheck.ValidateTypes(((report_query[key], (str, unicode)),))


def ValidateReportJob(report_job):
  """Validate ReportJob object.

  Args:
    report_job: dict ReportJob object.
  """
  SanityCheck.ValidateTypes(((report_job, dict),))
  for key in report_job:
    if key in ('reportQuery',):
      ValidateReportQuery(report_job[key])
    else:
      SanityCheck.ValidateTypes(((report_job[key], (str, unicode)),))


def ValidateNetwork(network):
  """Validate Network object.

  Args:
    network: dict Network object.
  """
  SanityCheck.ValidateOneLevelObject(network)


def ValidateCustomTargetingKey(key):
  """Validate CustomTargetingKey object.

  Args:
    key: dict CustomTargetingKey object.
  """
  SanityCheck.ValidateOneLevelObject(key)


def ValidateCustomTargetingValue(value):
  """Validate CustomTargetingValue object.

  Args:
    value: dict CustomTargetingValue object.
  """
  SanityCheck.ValidateOneLevelObject(value)
