################################################## 
# LineItemCreativeAssociationService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from LineItemCreativeAssociationService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class LineItemCreativeAssociationServiceLocator:
    LineItemCreativeAssociationServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201103/LineItemCreativeAssociationService"
    def getLineItemCreativeAssociationServiceInterfaceAddress(self):
        return LineItemCreativeAssociationServiceLocator.LineItemCreativeAssociationServiceInterface_address
    def getLineItemCreativeAssociationServiceInterface(self, url=None, **kw):
        return LineItemCreativeAssociationServiceSoapBindingSOAP(url or LineItemCreativeAssociationServiceLocator.LineItemCreativeAssociationServiceInterface_address, **kw)

# Methods
class LineItemCreativeAssociationServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: createLineItemCreativeAssociation
    def createLineItemCreativeAssociation(self, request):
        if isinstance(request, createLineItemCreativeAssociationRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createLineItemCreativeAssociationResponse.typecode)
        return response

    # op: createLineItemCreativeAssociations
    def createLineItemCreativeAssociations(self, request):
        if isinstance(request, createLineItemCreativeAssociationsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createLineItemCreativeAssociationsResponse.typecode)
        return response

    # get: getLineItemCreativeAssociation
    def getLineItemCreativeAssociation(self, request):
        if isinstance(request, getLineItemCreativeAssociationRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getLineItemCreativeAssociationResponse.typecode)
        return response

    # get: getLineItemCreativeAssociationsByStatement
    def getLineItemCreativeAssociationsByStatement(self, request):
        if isinstance(request, getLineItemCreativeAssociationsByStatementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getLineItemCreativeAssociationsByStatementResponse.typecode)
        return response

    # op: performLineItemCreativeAssociationAction
    def performLineItemCreativeAssociationAction(self, request):
        if isinstance(request, performLineItemCreativeAssociationActionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(performLineItemCreativeAssociationActionResponse.typecode)
        return response

    # op: updateLineItemCreativeAssociation
    def updateLineItemCreativeAssociation(self, request):
        if isinstance(request, updateLineItemCreativeAssociationRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateLineItemCreativeAssociationResponse.typecode)
        return response

    # op: updateLineItemCreativeAssociations
    def updateLineItemCreativeAssociations(self, request):
        if isinstance(request, updateLineItemCreativeAssociationsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updateLineItemCreativeAssociationsResponse.typecode)
        return response

createLineItemCreativeAssociationRequest = ns0.createLineItemCreativeAssociation_Dec().pyclass

createLineItemCreativeAssociationResponse = ns0.createLineItemCreativeAssociationResponse_Dec().pyclass

createLineItemCreativeAssociationsRequest = ns0.createLineItemCreativeAssociations_Dec().pyclass

createLineItemCreativeAssociationsResponse = ns0.createLineItemCreativeAssociationsResponse_Dec().pyclass

getLineItemCreativeAssociationRequest = ns0.getLineItemCreativeAssociation_Dec().pyclass

getLineItemCreativeAssociationResponse = ns0.getLineItemCreativeAssociationResponse_Dec().pyclass

getLineItemCreativeAssociationsByStatementRequest = ns0.getLineItemCreativeAssociationsByStatement_Dec().pyclass

getLineItemCreativeAssociationsByStatementResponse = ns0.getLineItemCreativeAssociationsByStatementResponse_Dec().pyclass

performLineItemCreativeAssociationActionRequest = ns0.performLineItemCreativeAssociationAction_Dec().pyclass

performLineItemCreativeAssociationActionResponse = ns0.performLineItemCreativeAssociationActionResponse_Dec().pyclass

updateLineItemCreativeAssociationRequest = ns0.updateLineItemCreativeAssociation_Dec().pyclass

updateLineItemCreativeAssociationResponse = ns0.updateLineItemCreativeAssociationResponse_Dec().pyclass

updateLineItemCreativeAssociationsRequest = ns0.updateLineItemCreativeAssociations_Dec().pyclass

updateLineItemCreativeAssociationsResponse = ns0.updateLineItemCreativeAssociationsResponse_Dec().pyclass
