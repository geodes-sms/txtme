"""
A simple serializer class that creates a server response
"""

import StringIO
import json

class ResponseSerializer:

    @staticmethod
    def error(msg, dic = None):
        """
        an error message
        :param msg: the message
        :param dic: optional extra information about the the response
        :return: a json serialized version of the response
        """
        ret = {}
        ret['response_status'] = 'ERROR'
        ret['message'] = msg

        if dic:
            for key in dic.keys():
                ret[key] = dic[key]

        io = StringIO.StringIO()
        json.dump(ret, io)
        return io.getvalue()

    @staticmethod
    def success(dic = None):
        """
        an success response
        :param dic: optional requested information
        :return: a json a json serialized version of the response
        """

        ret = {}
        ret['response_status'] = 'OK'

        if dic:
            for key in dic.keys():
                ret[key] = dic[key]

        io = StringIO.StringIO()
        json.dump(ret, io)
        return io.getvalue()