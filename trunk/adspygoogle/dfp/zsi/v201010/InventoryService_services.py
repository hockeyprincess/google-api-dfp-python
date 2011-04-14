################################################## 
# InventoryService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from InventoryService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class InventoryServiceLocator:
    InventoryServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201010/InventoryService"
    def getInventoryServiceInterfaceAddress(self):
        return InventoryServiceLocator.InventoryServiceInterface_address
    def getInventoryServiceInterface(self, url=None, **kw):
        return InventoryServiceSoapBindingSOAP(url or InventoryServiceLocator.InventoryServiceInterface_address, **kw)

# Methods
class InventoryServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: createAdUnit
    def createAdUnit(self, request):
        if isinstance(request, createAdUnitRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createAdUnitResponse.typecode)
        return response

    # op: createAdUnits
    def createAdUnits(self, request):
        if isinstance(request, createAdUnitsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createAdUnitsResponse.typecode)
        return response

    # get: getInventoryAdUnit
    def getAdUnit(self, request):
        if isinstance(request, getAdUnitRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdUnitResponse.typecode)
        return response

    # get: getInventoryAdUnitsByStatement
    def getAdUnitsByStatement(self, request):
        if isinstance(request, getAdUnitsByStatementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getAdUnitsByStatementResponse.typecode)
        return response

    # op: performAdUnitAction
    def performAdUnitAction(self, request):
        if isinstance(request, performAdUnitActionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(performAdUnitActionResponse.typecode)
        return response

    # op: updateAdUnit
    def updateAdUnit(self, request):
        if isinstance(request, updateAdUnitRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateAdUnitResponse.typecode)
        return response

    # op: updateAdUnits
    def updateAdUnits(self, request):
        if isinstance(request, updateAdUnitsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateAdUnitsResponse.typecode)
        return response

createAdUnitRequest = ns0.createAdUnit_Dec().pyclass

createAdUnitResponse = ns0.createAdUnitResponse_Dec().pyclass

createAdUnitsRequest = ns0.createAdUnits_Dec().pyclass

createAdUnitsResponse = ns0.createAdUnitsResponse_Dec().pyclass

getAdUnitRequest = ns0.getAdUnit_Dec().pyclass

getAdUnitResponse = ns0.getAdUnitResponse_Dec().pyclass

getAdUnitsByStatementRequest = ns0.getAdUnitsByStatement_Dec().pyclass

getAdUnitsByStatementResponse = ns0.getAdUnitsByStatementResponse_Dec().pyclass

performAdUnitActionRequest = ns0.performAdUnitAction_Dec().pyclass

performAdUnitActionResponse = ns0.performAdUnitActionResponse_Dec().pyclass

updateAdUnitRequest = ns0.updateAdUnit_Dec().pyclass

updateAdUnitResponse = ns0.updateAdUnitResponse_Dec().pyclass

updateAdUnitsRequest = ns0.updateAdUnits_Dec().pyclass

updateAdUnitsResponse = ns0.updateAdUnitsResponse_Dec().pyclass
