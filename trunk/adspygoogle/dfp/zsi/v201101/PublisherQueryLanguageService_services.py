################################################## 
# PublisherQueryLanguageService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from PublisherQueryLanguageService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class PublisherQueryLanguageServiceLocator:
    PublisherQueryLanguageServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201101/PublisherQueryLanguageService"
    def getPublisherQueryLanguageServiceInterfaceAddress(self):
        return PublisherQueryLanguageServiceLocator.PublisherQueryLanguageServiceInterface_address
    def getPublisherQueryLanguageServiceInterface(self, url=None, **kw):
        return PublisherQueryLanguageServiceSoapBindingSOAP(url or PublisherQueryLanguageServiceLocator.PublisherQueryLanguageServiceInterface_address, **kw)

# Methods
class PublisherQueryLanguageServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: select
    def select(self, request):
        if isinstance(request, selectRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(selectResponse.typecode)
        return response

selectRequest = ns0.select_Dec().pyclass

selectResponse = ns0.selectResponse_Dec().pyclass
