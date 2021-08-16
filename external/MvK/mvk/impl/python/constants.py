'''
Created on 25-feb.-2014

@author: Simon
'''
from mvk.impl.python.datavalue import IntegerValue, StringValue


class LogConstants(object):
    SUCCESS_CODE = IntegerValue(600)
    BAD_REQUEST_CODE = IntegerValue(700)
    NOT_FOUND_CODE = IntegerValue(701)
    MALFORMED_REQUEST_CODE = IntegerValue(797)
    METHOD_NOT_ALLOWED_CODE = IntegerValue(798)
    INTERNAL_ERROR_CODE = IntegerValue(799)

    OPERATION_NAME_KEY = StringValue("operation_name")
    STATUS_CODE_KEY = StringValue("status_code")
    STATUS_MESSAGE_KEY = StringValue("status_message")

    @classmethod
    def get_codes(cls):
        return set([cls.SUCCESS_CODE, cls.BAD_REQUEST_CODE,
                    cls.NOT_FOUND_CODE, cls.METHOD_NOT_ALLOWED_CODE,
                    cls.INTERNAL_ERROR_CODE])

    @classmethod
    def succes_codes(cls):
        return set([cls.SUCCESS_CODE])

    @classmethod
    def get_keys(cls):
        return set([cls.CHANGETYPE_KEY,
                    cls.STATUS_CODE_KEY,
                    cls.STATUS_MESSAGE_KEY])


class CRUDConstants(LogConstants):
    LOCATION_KEY = StringValue("location")
    TYPE_KEY = StringValue("type")
    CREATE_OPERATION = StringValue('create')
    READ_OPERATION = StringValue('read')
    UPDATE_OPERATION = StringValue('update')
    DELETE_OPERATION = StringValue('delete')
    COMPOSITE_OPERATION = StringValue('<composite>')

    @classmethod
    def get_keys(cls):
        return LogConstants.get_keys().union(set([cls.LOCATION_KEY]))


class ChangelogConstants(CRUDConstants):
    pass


class CreateConstants(ChangelogConstants):
    SUCCESS_CODE = LogConstants.SUCCESS_CODE + IntegerValue(10)
    BAD_REQUEST_CODE = LogConstants.BAD_REQUEST_CODE + IntegerValue(10)
    NOT_FOUND_CODE = LogConstants.NOT_FOUND_CODE + IntegerValue(10)

    ATTRS_KEY = StringValue("attributes")
    NAME_KEY = StringValue("name")
    VALUE_KEY = StringValue("value")

    @classmethod
    def get_keys(cls):
        return ChangelogConstants.get_keys().union(set([cls.ATTRS_KEY]))


class ReadConstants(CRUDConstants):
    SUCCESS_CODE = LogConstants.SUCCESS_CODE + IntegerValue(5)
    BAD_REQUEST_CODE = LogConstants.BAD_REQUEST_CODE + IntegerValue(5)
    NOT_FOUND_CODE = LogConstants.NOT_FOUND_CODE + IntegerValue(5)

    ITEM_KEY = StringValue("item")

    @classmethod
    def get_keys(cls):
        return CRUDConstants.get_keys().union(set([cls.ITEM_KEY]))


class UpdateConstants(ChangelogConstants):
    SUCCESS_CODE = LogConstants.SUCCESS_CODE + IntegerValue(25)
    BAD_REQUEST_CODE = LogConstants.BAD_REQUEST_CODE + IntegerValue(25)
    NOT_FOUND_CODE = LogConstants.NOT_FOUND_CODE + IntegerValue(25)

    ATTRS_KEY = StringValue("attributes")
    NAME_KEY = StringValue("name")
    NEW_VAL_KEY = StringValue("new_val")
    OLD_VAL_KEY = StringValue("old_val")

    @classmethod
    def get_keys(cls):
        return ChangelogConstants.get_keys().union(set([cls.ATTRS_KEY]))


class DeleteConstants(ChangelogConstants):
    SUCCESS_CODE = LogConstants.SUCCESS_CODE + IntegerValue(30)
    BAD_REQUEST_CODE = LogConstants.BAD_REQUEST_CODE + IntegerValue(30)
    NOT_FOUND_CODE = LogConstants.NOT_FOUND_CODE + IntegerValue(30)

    ITEM_KEY = StringValue("item")


class CompositeConstants(LogConstants):
    LOGS_KEY = StringValue("logs")

    @classmethod
    def get_keys(cls):
        return LogConstants.get_keys().union(set([cls.LOGS_KEY]))
    
'''Maris Jukss'''
class TransformationConstants(LogConstants):
    SUCCESS_CODE = LogConstants.SUCCESS_CODE + IntegerValue(40)
    FAILURE_CODE = LogConstants.NOT_FOUND_CODE + IntegerValue(40)
    
class RuleExecutionConstants(LogConstants):
    SUCCESS_CODE = LogConstants.SUCCESS_CODE + IntegerValue(35)
    NOT_APPLICABLE_CODE = LogConstants.BAD_REQUEST_CODE + IntegerValue(35)
    FAILURE_CODE = LogConstants.NOT_FOUND_CODE + IntegerValue(35)

