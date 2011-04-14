#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Settings and configuration for the SOAPpy toolkit."""


# The order map for objects' keys that themselves point to complex objects. For
# APIs that run incoming SOAP message through XML validation, this map allows
# for placing object's fields in correct order. Required for users of SOAPpy.
#
# type: The type of the object to which key is pointing. It can hold one of
#       three values. A type itself, if fields and their order is specific to
#       particular object (e.g., Size). An empty string, if multiple objects
#       may share the same set of fields and order. And a None, when specific
#       type is determined at runtime (e.g., Creative).
#
# order: A tuple of object's fields in particular order.
#
# native_type: A boolean value to indicate whether an object has a 'type' field
#              of its own.
#
# TODO(api.sgrinberg): Automate the process of generating object order by
# loading this info from a WSDL or generated class interface. Should be part of
# the gen_wsdl_services.py script.
OBJ_KEY_ORDER_MAP = {
    'company': [
        {
            'type': 'Company',
            'order': ('id', 'name', 'type'),
            'native_type': True
        }
    ],
    'companies': [
        {
            'type': 'Company',
            'order': ('id', 'name', 'type'),
            'native_type': True
        }
    ],
    'filterStatement': [
        {
            'type': 'Statement',
            'order': ('query', 'params')
        }
    ],
    'params': [
        {
            'type': None,
            'order': ('key', 'value')

        }
    ],
    'keys': [
        {
            'type': 'CustomTargetingKey',
            'order': ('name', 'displayName', 'type'),
            'native_type': True
        }
    ],
    'values': [
        {
            'type': 'CustomTargetingValue',
            'order': ('customTargetingKeyId', 'name', 'displayName',
                      'matchType')
        },
        {
            'type': None,
            'order': ('key', 'value')
        }
    ],
    'creative': [
        {
            'type': None,
            'order': ('advertiserId', 'id', 'name', 'size', 'previewUrl',
                      'destinationUrl', 'snippet', 'expandedSnippet',
                      'formatStatus', 'flashName', 'flashByteArray',
                      'fallbackImageName', 'fallbackImageByteArray',
                      'imageName', 'imageUrl', 'imageByteArray'
                      'overrideSize', 'assetSize', 'clickTagRequired',
                      'flashUrl', 'fallbackPreviewUrl', 'flashAssetSize',
                      'fallbackAssetSize')
        }
    ],
    'creatives': [
        {
            'type': None,
            'order': ('advertiserId', 'id', 'name', 'size', 'previewUrl',
                      'destinationUrl', 'snippet', 'expandedSnippet',
                      'formatStatus', 'flashName', 'flashByteArray',
                      'fallbackImageName', 'fallbackImageByteArray',
                      'imageName', 'imageUrl', 'imageByteArray'
                      'overrideSize', 'assetSize', 'clickTagRequired',
                      'flashUrl', 'fallbackPreviewUrl', 'flashAssetSize',
                      'fallbackAssetSize')
        }
    ],
    'size': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'flashAssetSize': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'fallbackAssetSize': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'assetSize': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'sizes': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'creativeSizes': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'key': [
        {
            'type': 'Size',
            'order': ('width', 'height')
        }
    ],
    'adUnit': [
        {
            'type': 'AdUnit',
            'order': ('id', 'parentId', 'name', 'description', 'targetWindow',
                      'status', 'adUnitCode', 'sizes',
                      'inheritedAdSenseSettings')
        }
    ],
    'adUnits': [
        {
            'type': 'AdUnit',
            'order': ('id', 'parentId', 'name', 'description', 'targetWindow',
                      'status', 'adUnitCode', 'sizes',
                      'inheritedAdSenseSettings')
        }
    ],
    'inheritedAdSenseSettings': [
        {
            'type': 'AdSenseSettingsInheritedProperty',
            'order': ('value',)
        }
    ],
    'value': [
        {
            'type': 'AdSenseSettings',
            'order': ('adSenseEnabled', 'borderColor', 'titleColor',
                      'backgroundColor', 'textColor', 'urlColor', 'adType',
                      'borderStyle', 'afcFormats')
        },
        {
            'type': '',
            'order': ('value',)
        }
    ],
    'afcFormats': [
        {
            'type': 'Size_StringMapEntry',
            'order': ('key', 'value')
        }
    ],
    'adUnitAction': [
        {
            'type': 'AssignAdUnitsToPlacement',
            'order': ('placementId',)
        },
        {
            'type': None,
            'order': ()
        }
    ],
    'lineItemCreativeAssociation': [
        {
            'type': 'LineItemCreativeAssociation',
            'order': ('lineItemId', 'creativeId',
                      'manualCreativeRotationWeight', 'startDateTime',
                      'endDateTime', 'destinationUrl', 'sizes',
                      'status')
        }
    ],
    'lineItemCreativeAssociations': [
        {
            'type': 'LineItemCreativeAssociation',
            'order': ('lineItemId', 'creativeId',
                      'manualCreativeRotationWeight', 'startDateTime',
                      'endDateTime', 'destinationUrl', 'sizes',
                      'status')
        }
    ],
    'startDateTime': [
        {
            'type': 'DateTime',
            'order': ('date', 'hour', 'minute', 'second', 'timeZoneID')
        }
    ],
    'startTime': [
        {
            'type': 'TimeOfDay',
            'order': ('hour', 'minute')
        }
    ],
    'endDateTime': [
        {
            'type': 'DateTime',
            'order': ('date', 'hour', 'minute', 'second', 'timeZoneID')
        }
    ],
    'endTime': [
        {
            'type': 'TimeOfDay',
            'order': ('hour', 'minute')
        }
    ],
    'date': [
        {
            'type': 'Date',
            'order': ('year', 'month', 'day')
        }
    ],
    'lineItemCreativeAssociationAction': [
        {
            'type': None,
            'order': ()
        }
    ],
    'lineItem': [
        {
            'type': 'LineItem',
            'order': ('orderId', 'id', 'name', 'startDateTime', 'startType',
                      'endDateTime', 'unlimitedEndDateTime',
                      'creativeRotationType', 'deliveryRateType',
                      'roadblockingType', 'frequencyCaps', 'lineItemType',
                      'unitType', 'duration', 'unitsBought', 'costPerUnit',
                      'valueCostPerUnit', 'costType', 'discountType',
                      'discount', 'creativeSizes', 'allowOverbook',
                      'budget', 'status', 'inventoryStatus', 'targeting')
        }
    ],
    'lineItems': [
        {
            'type': 'LineItem',
            'order': ('orderId', 'id', 'name', 'startDateTime', 'startType',
                      'endDateTime', 'unlimitedEndDateTime',
                      'creativeRotationType', 'deliveryRateType',
                      'roadblockingType', 'frequencyCaps', 'lineItemType',
                      'unitType', 'duration', 'unitsBought', 'costPerUnit',
                      'valueCostPerUnit', 'costType', 'discountType',
                      'discount', 'creativeSizes', 'allowOverbook',
                      'budget', 'status', 'inventoryStatus', 'targeting')
        }
    ],
    'frequencyCaps': [
        {
            'type': 'FrequencyCap',
            'order': ('maxImpressions', 'timeUnit')
        }
    ],
    'costPerUnit': [
        {
            'type': 'Money',
            'order': ('currencyCode', 'microAmount')
        }
    ],
    'valueCostPerUnit': [
        {
            'type': 'Money',
            'order': ('currencyCode', 'microAmount')
        }
    ],
    'totalBudget': [
        {
            'type': 'Money',
            'order': ('currencyCode', 'microAmount')
        }
    ],
    'targeting': [
        {
            'type': 'Targeting',
            'order': ('geoTargeting', 'inventoryTargeting', 'customTargeting')
        }
    ],
    'geoTargeting': [
        {
            'type': 'Targeting',
            'order': ('targetedLocations', 'excludedLocations')
        }
    ],
    'targetedLocations': [
        {
            'type': 'Location',
            'order': ('cityName', 'regionCode', 'metroCode', 'countryCode')
        }
    ],
    'excludedLocations': [
        {
            'type': 'Location',
            'order': ('cityName', 'regionCode', 'metroCode', 'countryCode')
        }
    ],
    'inventoryTargeting': [
        {
            'type': 'InventoryTargeting',
            'order': ('targetedAdUnitIds', 'excludedAdUnitIds',
                      'targetedPlacementIds')
        }
    ],
    'customTargeting': [
        {
            'type': 'CustomCriteriaSet',
            'order': ('logicalOperator', 'children')
        }
    ],
    'children': [
        {
            'type': None,
            'order': ('keyId', 'operator', 'values', 'valueIds',
                      'logicalOperator', 'children')
        }
    ],
    'values': [
        {
            'type': 'CustomTargetingValue',
            'order': ('customTargetingKeyId', 'name', 'displayName',
                      'matchType')
        }
    ],
    'lineItemAction': [
        {
            'type': None,
            'order': ()
        }
    ],
    'order': [
        {
            'type': 'Order',
            'order': ('id', 'name', 'startDateTime', 'endDateTime',
                      'unlimitedEndDateTime', 'status', 'isArchived', 'notes',
                      'externalId', 'currencyCode', 'advertiserId', 'creatorId',
                      'traffickerId', 'salespersonId',
                      'totalImpressionsDelivered', 'totalClicksDelivered',
                      'totalBudget')
        }
    ],
    'orders': [
        {
            'type': 'Order',
            'order': ('id', 'name', 'startDateTime', 'endDateTime',
                      'unlimitedEndDateTime', 'status', 'isArchived', 'notes',
                      'externalId', 'currencyCode', 'advertiserId', 'creatorId',
                      'traffickerId', 'salespersonId',
                      'totalImpressionsDelivered', 'totalClicksDelivered',
                      'totalBudget')
        }
    ],
    'orderAction': [
        {
            'type': None,
            'order': ()
        }
    ],
    'placement': [
        {
            'type': 'Placement',
            'order': ('targetingDescription', 'targetingSiteName',
                      'targetingAdLocation', 'id', 'name', 'description',
                      'placementCode', 'status', 'isAdSenseTargetingEnabled',
                      'isAdPlannerTargetingEnabled', 'adSenseTargetingLocale',
                      'targetedAdUnitIds')
        }
    ],
    'placements': [
        {
            'type': 'Placement',
            'order': ('targetingDescription', 'targetingSiteName',
                      'targetingAdLocation', 'id', 'name', 'description',
                      'placementCode', 'status', 'isAdSenseTargetingEnabled',
                      'isAdPlannerTargetingEnabled', 'adSenseTargetingLocale',
                      'targetedAdUnitIds')
        }
    ],
    'placementAction': [
        {
            'type': None,
            'order': ()
        }
    ],
    'user': [
        {
            'type': 'User',
            'order': ('id', 'name', 'email', 'roleId', 'roleName',
                      'preferredLocale', 'isActive',
                      'isEmailNotificationAllowed')
        }
    ],
    'users': [
        {
            'type': 'User',
            'order': ('id', 'name', 'email', 'roleId', 'roleName',
                      'preferredLocale', 'isActive',
                      'isEmailNotificationAllowed')
        }
    ],
    'userAction': [
        {
            'type': None,
            'order': ()
        }
    ]
}
