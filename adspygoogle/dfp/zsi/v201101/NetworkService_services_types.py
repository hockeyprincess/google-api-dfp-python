################################################## 
# NetworkService_services_types.py 
# generated by ZSI.generate.wsdl2python
##################################################


import ZSI
import ZSI.TCcompound
from ZSI.schema import LocalElementDeclaration, ElementDeclaration, TypeDefinition, GTD, GED

##############################
# targetNamespace
# https://www.google.com/apis/ads/publisher/v201101
##############################

class ns0:
    targetNamespace = "https://www.google.com/apis/ads/publisher/v201101"

    class ApiVersionError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ApiVersionError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.ApiVersionError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","ApiVersionError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.ApiVersionError_Def.__bases__:
                bases = list(ns0.ApiVersionError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.ApiVersionError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class AuthenticationError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "AuthenticationError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.AuthenticationError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","AuthenticationError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.AuthenticationError_Def.__bases__:
                bases = list(ns0.AuthenticationError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.AuthenticationError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class CommonError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "CommonError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.CommonError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","CommonError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.CommonError_Def.__bases__:
                bases = list(ns0.CommonError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.CommonError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class InternalApiError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "InternalApiError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.InternalApiError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","InternalApiError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.InternalApiError_Def.__bases__:
                bases = list(ns0.InternalApiError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.InternalApiError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class Network_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "Network")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.Network_Def.schema
            TClist = [ZSI.TC.String(pname=(ns,"id"), aname="_id", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"displayName"), aname="_displayName", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"networkCode"), aname="_networkCode", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"propertyCode"), aname="_propertyCode", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"timeZone"), aname="_timeZone", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"currencyCode"), aname="_currencyCode", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"effectiveRootAdUnitId"), aname="_effectiveRootAdUnitId", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._id = None
                    self._displayName = None
                    self._networkCode = None
                    self._propertyCode = None
                    self._timeZone = None
                    self._currencyCode = None
                    self._effectiveRootAdUnitId = None
                    return
            Holder.__name__ = "Network_Holder"
            self.pyclass = Holder

    class NotNullError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "NotNullError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.NotNullError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","NotNullError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.NotNullError_Def.__bases__:
                bases = list(ns0.NotNullError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.NotNullError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class ParseError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ParseError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.ParseError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","ParseError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.ParseError_Def.__bases__:
                bases = list(ns0.ParseError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.ParseError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class PermissionError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "PermissionError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.PermissionError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","PermissionError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.PermissionError_Def.__bases__:
                bases = list(ns0.PermissionError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.PermissionError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class QuotaError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "QuotaError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.QuotaError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","QuotaError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.QuotaError_Def.__bases__:
                bases = list(ns0.QuotaError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.QuotaError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class RequiredError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "RequiredError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.RequiredError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","RequiredError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.RequiredError_Def.__bases__:
                bases = list(ns0.RequiredError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.RequiredError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class ServerError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ServerError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.ServerError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","ServerError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.ServerError_Def.__bases__:
                bases = list(ns0.ServerError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.ServerError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class SoapResponseHeader_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "SoapResponseHeader")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.SoapResponseHeader_Def.schema
            TClist = [ZSI.TC.String(pname=(ns,"requestId"), aname="_requestId", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"responseTime"), aname="_responseTime", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._requestId = None
                    self._responseTime = None
                    return
            Holder.__name__ = "SoapResponseHeader_Holder"
            self.pyclass = Holder

    class StatementError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "StatementError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.StatementError_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","StatementError.Reason",lazy=False)(pname=(ns,"reason"), aname="_reason", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.StatementError_Def.__bases__:
                bases = list(ns0.StatementError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.StatementError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class TypeError_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "TypeError")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.TypeError_Def.schema
            TClist = []
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApiError_Def not in ns0.TypeError_Def.__bases__:
                bases = list(ns0.TypeError_Def.__bases__)
                bases.insert(0, ns0.ApiError_Def)
                ns0.TypeError_Def.__bases__ = tuple(bases)

            ns0.ApiError_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class SoapRequestHeader_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "SoapRequestHeader")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.SoapRequestHeader_Def.schema
            TClist = [ZSI.TC.String(pname=(ns,"authToken"), aname="_authToken", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"networkCode"), aname="_networkCode", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"applicationName"), aname="_applicationName", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"oAuthToken"), aname="_oAuthToken", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._authToken = None
                    self._networkCode = None
                    self._applicationName = None
                    self._oAuthToken = None
                    return
            Holder.__name__ = "SoapRequestHeader_Holder"
            self.pyclass = Holder

    class ApiError_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ApiError")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.ApiError_Def.schema
            TClist = [ZSI.TC.String(pname=(ns,"fieldPath"), aname="_fieldPath", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"trigger"), aname="_trigger", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"errorString"), aname="_errorString", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"ApiError.Type"), aname="_ApiError_Type", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._fieldPath = None
                    self._trigger = None
                    self._errorString = None
                    self._ApiError_Type = None
                    return
            Holder.__name__ = "ApiError_Holder"
            self.pyclass = Holder

    class ApiException_Def(TypeDefinition):
        #complexType/complexContent extension
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ApiException")
        def __init__(self, pname, ofwhat=(), extend=False, restrict=False, attributes=None, **kw):
            ns = ns0.ApiException_Def.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","ApiError",lazy=False)(pname=(ns,"errors"), aname="_errors", minOccurs=0, maxOccurs="unbounded", nillable=True, typed=False, encoded=kw.get("encoded"))]
            attributes = self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            if ns0.ApplicationException_Def not in ns0.ApiException_Def.__bases__:
                bases = list(ns0.ApiException_Def.__bases__)
                bases.insert(0, ns0.ApplicationException_Def)
                ns0.ApiException_Def.__bases__ = tuple(bases)

            ns0.ApplicationException_Def.__init__(self, pname, ofwhat=TClist, extend=True, attributes=attributes, **kw)

    class ApplicationException_Def(ZSI.TCcompound.ComplexType, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ApplicationException")
        def __init__(self, pname, ofwhat=(), attributes=None, extend=False, restrict=False, **kw):
            ns = ns0.ApplicationException_Def.schema
            TClist = [ZSI.TC.String(pname=(ns,"message"), aname="_message", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname=(ns,"ApplicationException.Type"), aname="_ApplicationException_Type", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            self.attribute_typecode_dict = attributes or {}
            if extend: TClist += ofwhat
            if restrict: TClist = ofwhat
            ZSI.TCcompound.ComplexType.__init__(self, None, TClist, pname=pname, inorder=0, **kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._message = None
                    self._ApplicationException_Type = None
                    return
            Holder.__name__ = "ApplicationException_Holder"
            self.pyclass = Holder

    class ApiVersionError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ApiVersionError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class AuthenticationError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "AuthenticationError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class CommonError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "CommonError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class InternalApiError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "InternalApiError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class NotNullError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "NotNullError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class ParseError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ParseError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class PermissionError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "PermissionError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class QuotaError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "QuotaError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class RequiredError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "RequiredError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class ServerError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "ServerError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class StatementError_Reason_Def(ZSI.TC.String, TypeDefinition):
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        type = (schema, "StatementError.Reason")
        def __init__(self, pname, **kw):
            ZSI.TC.String.__init__(self, pname, pyclass=None, **kw)
            class Holder(str):
                typecode = self
            self.pyclass = Holder

    class getAllNetworks_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "getAllNetworks"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            ns = ns0.getAllNetworks_Dec.schema
            TClist = []
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","getAllNetworks")
            kw["aname"] = "_getAllNetworks"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    return
            Holder.__name__ = "getAllNetworks_Holder"
            self.pyclass = Holder

    class getAllNetworksResponse_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "getAllNetworksResponse"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            ns = ns0.getAllNetworksResponse_Dec.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","Network",lazy=False)(pname=(ns,"rval"), aname="_rval", minOccurs=0, maxOccurs="unbounded", nillable=True, typed=False, encoded=kw.get("encoded"))]
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","getAllNetworksResponse")
            kw["aname"] = "_getAllNetworksResponse"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._rval = []
                    return
            Holder.__name__ = "getAllNetworksResponse_Holder"
            self.pyclass = Holder

    class ApiExceptionFault_Dec(ElementDeclaration):
        literal = "ApiExceptionFault"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","ApiExceptionFault")
            kw["aname"] = "_ApiExceptionFault"
            if ns0.ApiException_Def not in ns0.ApiExceptionFault_Dec.__bases__:
                bases = list(ns0.ApiExceptionFault_Dec.__bases__)
                bases.insert(0, ns0.ApiException_Def)
                ns0.ApiExceptionFault_Dec.__bases__ = tuple(bases)

            ns0.ApiException_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "ApiExceptionFault_Dec_Holder"

    class getCurrentNetwork_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "getCurrentNetwork"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            ns = ns0.getCurrentNetwork_Dec.schema
            TClist = []
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","getCurrentNetwork")
            kw["aname"] = "_getCurrentNetwork"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    return
            Holder.__name__ = "getCurrentNetwork_Holder"
            self.pyclass = Holder

    class getCurrentNetworkResponse_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "getCurrentNetworkResponse"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            ns = ns0.getCurrentNetworkResponse_Dec.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","Network",lazy=False)(pname=(ns,"rval"), aname="_rval", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","getCurrentNetworkResponse")
            kw["aname"] = "_getCurrentNetworkResponse"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._rval = None
                    return
            Holder.__name__ = "getCurrentNetworkResponse_Holder"
            self.pyclass = Holder

    class updateNetwork_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "updateNetwork"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            ns = ns0.updateNetwork_Dec.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","Network",lazy=False)(pname=(ns,"network"), aname="_network", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","updateNetwork")
            kw["aname"] = "_updateNetwork"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._network = None
                    return
            Holder.__name__ = "updateNetwork_Holder"
            self.pyclass = Holder

    class updateNetworkResponse_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "updateNetworkResponse"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            ns = ns0.updateNetworkResponse_Dec.schema
            TClist = [GTD("https://www.google.com/apis/ads/publisher/v201101","Network",lazy=False)(pname=(ns,"rval"), aname="_rval", minOccurs=0, maxOccurs=1, nillable=True, typed=False, encoded=kw.get("encoded"))]
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","updateNetworkResponse")
            kw["aname"] = "_updateNetworkResponse"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                typecode = self
                def __init__(self):
                    # pyclass
                    self._rval = None
                    return
            Holder.__name__ = "updateNetworkResponse_Holder"
            self.pyclass = Holder

    class RequestHeader_Dec(ElementDeclaration):
        literal = "RequestHeader"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","RequestHeader")
            kw["aname"] = "_RequestHeader"
            if ns0.SoapRequestHeader_Def not in ns0.RequestHeader_Dec.__bases__:
                bases = list(ns0.RequestHeader_Dec.__bases__)
                bases.insert(0, ns0.SoapRequestHeader_Def)
                ns0.RequestHeader_Dec.__bases__ = tuple(bases)

            ns0.SoapRequestHeader_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "RequestHeader_Dec_Holder"

    class ResponseHeader_Dec(ElementDeclaration):
        literal = "ResponseHeader"
        schema = "https://www.google.com/apis/ads/publisher/v201101"
        def __init__(self, **kw):
            kw["pname"] = ("https://www.google.com/apis/ads/publisher/v201101","ResponseHeader")
            kw["aname"] = "_ResponseHeader"
            if ns0.SoapResponseHeader_Def not in ns0.ResponseHeader_Dec.__bases__:
                bases = list(ns0.ResponseHeader_Dec.__bases__)
                bases.insert(0, ns0.SoapResponseHeader_Def)
                ns0.ResponseHeader_Dec.__bases__ = tuple(bases)

            ns0.SoapResponseHeader_Def.__init__(self, **kw)
            if self.pyclass is not None: self.pyclass.__name__ = "ResponseHeader_Dec_Holder"

# end class ns0 (tns: https://www.google.com/apis/ads/publisher/v201101)
