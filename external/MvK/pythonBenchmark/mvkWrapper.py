import urllib
import urllib2

from mvk.impl.python.util.jsonserializer import MvKEncoder
from mvk.impl.client.jsondeserializer import MvKDecoder

class MvKWrapper(object):
    def __init__(self, host, port, protocol = "http"):
        self.requesturl = "%s://%s:%s/" % (protocol, host, port)
        print("Request URL: " + str(self.requesturl))
        self.encoder = MvKEncoder()
        self.decoder = MvKDecoder()

    def requestGET(self, function, data):
        query = "?func=" + str(function) + "&args=" + urllib.pathname2url(data)
        response = urllib2.urlopen(self.requesturl + query)
        r = response.read()
        return self.decoder.decode(r)

    def requestPOST(self, function, data):
        query = "func=" + str(function) + "&args=" + data
        response = urllib2.urlopen(self.requesturl, query)
        return self.decoder.decode(response.read())

    def create(self, mapping):
        return self.requestPOST("create", self.encoder.encode(mapping))

    def read(self, location):
        return self.requestGET("read", self.encoder.encode(location))

    def update(self, mapping):
        return self.requestPOST("update", self.encoder.encode(mapping))

    def delete(self, location):
        return self.requestPOST("delete", self.encoder.encode(location))

    def clear(self):
        return self.requestPOST("clear", "")

    def conforms_to(self, model, type_model):
        return self.requestPOST("conforms_to", "[[" + self.encoder.encode(model) + "," + self.encoder.encode(type_model) + "], {}]")

    def evaluate(self, *args, **kwargs):
        return self.requestPOST("evaluate", "[" + self.encoder.encode(args) + ", " + self.encoder.encode(kwargs) + "]")
