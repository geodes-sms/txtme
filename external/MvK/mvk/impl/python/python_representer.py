"""
Created on 28-dec.-2013

@author: Simon
"""
import json
import os
import cPickle as pickle
import traceback

from mvk.impl.python.action import *
from mvk.impl.python.changelog import MvKCreateLog, MvKReadLog, MvKDeleteLog, MvKUpdateLog, MvKLog, MvKCompositeLog, MvKOperationLog
from mvk.impl.python.constants import CreateConstants, ReadConstants, DeleteConstants, UpdateConstants, LogConstants, CRUDConstants, CompositeConstants
from mvk.impl.python.datavalue import IntegerValue, StringValue, LocationValue
from mvk.impl.python.exception import MvKKeyError
from mvk.impl.python.object import Model, Clabject, Association, Composition, Aggregation, Attribute, Package, Inherits
import mvk.interfaces.datavalue
from mvk.interfaces.representer import Representer
from mvk.util.logger import get_logger


logger = get_logger('python_representer')


class RootPackage(Package):
    ''' Basically, a package which is not the parent of its elements, but does
    keep track of them... Necessary to cleanly implement the
    top level package. '''
    location = LocationValue("")
    def add_element(self, element):
        assert isinstance(element, mvk.interfaces.element.NamedElement)
        assert logger.debug("Adding element with name %s to the root package." %
                            element.get_name())
        self.name_lookup[element.get_name()] = element
        assert element.get_name() in self.name_lookup


class PythonRepresenter(Representer):
    """
    Implements the Representer interface. This mapper maps elements onto
    their representation, which are Python objects.
    """
    PACKAGE = LocationValue('mvk.object.Package')
    MODEL = LocationValue('mvk.object.Model')
    CLABJECT = LocationValue('mvk.object.Clabject')
    ASSOCIATION = LocationValue('mvk.object.Association')
    COMPOSITION = LocationValue('mvk.object.Composition')
    AGGREGATION = LocationValue('mvk.object.Aggregation')
    ATTRIBUTE = LocationValue('mvk.object.Attribute')
    INHERITS = LocationValue('mvk.object.Inherits')
    FUNCTION = LocationValue('mvk.action.Function')
    BODY = LocationValue('mvk.action.Body')
    PARAMETER = LocationValue('mvk.action.Parameter')
    EXPRESSIONSTATEMENT = LocationValue('mvk.action.ExpressionStatement')
    RETURNSTATEMENT = LocationValue('mvk.action.ReturnStatement')
    DECLARATIONSTATEMENT = LocationValue('mvk.action.DeclarationStatement')
    WHILELOOP = LocationValue('mvk.action.WhileLoop')
    IFSTATEMENT = LocationValue('mvk.action.IfStatement')
    BREAKSTATEMENT = LocationValue('mvk.action.BreakStatement')
    CONTINUESTATEMENT = LocationValue('mvk.action.ContinueStatement')
    CONSTANT = LocationValue('mvk.action.Constant')
    IDENTIFIER = LocationValue('mvk.action.Identifier')
    NAVIGATION = LocationValue('mvk.action.Navigation')
    ASSIGNMENT = LocationValue('mvk.action.Assignment')
    FUNCTIONCALL = LocationValue('mvk.action.FunctionCall')
    ARGUMENT = LocationValue('mvk.action.Argument')
    NOT = LocationValue('mvk.action.Not')
    OR = LocationValue('mvk.action.Or')
    AND = LocationValue('mvk.action.And')
    EQUAL = LocationValue('mvk.action.Equal')
    LESSTHAN = LocationValue('mvk.action.LessThan')
    GREATERTHAN = LocationValue('mvk.action.GreaterThan')
    IN = LocationValue('mvk.action.In')
    PLUS = LocationValue('mvk.action.Plus')
    MINUS = LocationValue('mvk.action.Minus')
    MULTIPLICATION = LocationValue('mvk.action.Multiplication')
    DIVISION = LocationValue('mvk.action.Division')
    MODULO = LocationValue('mvk.action.Modulo')

    CLS_TO_PHYS_TYPE = {RootPackage: PACKAGE,
                        Package: PACKAGE,
                        Model: MODEL,
                        Clabject: CLABJECT,
                        Association: ASSOCIATION,
                        Composition: COMPOSITION,
                        Aggregation: AGGREGATION,
                        Attribute: ATTRIBUTE,
                        Inherits: INHERITS,
                        Function: FUNCTION,
                        Body: BODY,
                        Parameter: PARAMETER,
                        ExpressionStatement: EXPRESSIONSTATEMENT,
                        ReturnStatement: RETURNSTATEMENT,
                        DeclarationStatement: DECLARATIONSTATEMENT,
                        WhileLoop: WHILELOOP,
                        IfStatement: IFSTATEMENT,
                        BreakStatement: BREAKSTATEMENT,
                        ContinueStatement: CONTINUESTATEMENT,
                        Constant: CONSTANT,
                        Identifier: IDENTIFIER,
                        Navigation: NAVIGATION,
                        Assignment: ASSIGNMENT,
                        FunctionCall: FUNCTIONCALL,
                        Argument: ARGUMENT,
                        Not: NOT,
                        Or: OR,
                        Equal: EQUAL,
                        LessThan: LESSTHAN,
                        GreaterThan: GREATERTHAN,
                        In: IN,
                        Plus: PLUS,
                        Minus: MINUS,
                        Multiplication: MULTIPLICATION,
                        Division: DIVISION,
                        Modulo: MODULO}

    """ === CONSTRUCTOR === """
    def __init__(self):
        self.root = RootPackage(name=StringValue(""))
        super(PythonRepresenter, self).__init__()

    """ === PUBLIC INTERFACE === """
    def create(self, params):
        try:
            if not CreateConstants.TYPE_KEY in params:
                clog = MvKCreateLog()
                clog.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
                clog.set_status_message(StringValue('No type given!'))
                return clog
            ptype = params[CreateConstants.TYPE_KEY]
            return PythonRepresenter.types()[ptype].create(params)
        except Exception:
            ''' TODO: Eventually, this catch-all should be removed. '''
            cl = MvKCreateLog()
            cl.set_status_code(CreateConstants.INTERNAL_ERROR_CODE)
            tb = traceback.format_exc()
            print tb
            cl.set_status_message(StringValue(tb))
            assert logger.error(tb)
            return cl

    def read(self, location):
        try:
            if not (isinstance(location, mvk.interfaces.datavalue.LocationValue) and
                    isinstance(location.typed_by(), mvk.interfaces.datatype.LocationType)):
                rlog = MvKReadLog()
                rlog.set_status_code(ReadConstants.MALFORMED_REQUEST_CODE)
                rlog.set_status_message(StringValue('Expected a location value.'))
                return rlog
            return self.root.read(location)
        except Exception:
            ''' TODO: Eventually, this catch-all should be removed. '''
            rl = MvKReadLog()
            rl.set_status_code(ReadConstants.INTERNAL_ERROR_CODE)
            tb = traceback.format_exc()
            print tb
            rl.set_status_message(StringValue(tb))
            assert logger.error(tb)
            return rl

    def update(self, params):
        try:
            ulog = MvKUpdateLog()
            if not UpdateConstants.LOCATION_KEY in params:
                ulog.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
                ulog.set_status_message(StringValue('Need the location of the element to update!'))
                return ulog
            location = params[UpdateConstants.LOCATION_KEY]
            if not (isinstance(location, mvk.interfaces.datavalue.LocationValue) and
                    isinstance(location.typed_by(), mvk.interfaces.datatype.LocationType)):
                ulog.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
                ulog.set_status_message(StringValue('Expected a location value.'))
                return ulog
            if location == LocationValue(''):
                ulog.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                ulog.set_status_message(StringValue('Cannot update the root of \
                                                     the modelverse.'))
                return ulog
            read_log = self.read(location)
            if read_log.is_success():
                old_name = read_log.get_item().get_name()
                ulog = read_log.get_item().update(params)
                if location.find(StringValue('.')) == IntegerValue(-1):
                    ''' A root element is updated. '''
                    if old_name != read_log.get_item().get_name():
                        ''' We assume here that read_log.get_item() is a
                        reference to the updated element... Which is
                        reasonable. '''
                        self.root.update_element(old_name, read_log.get_item())
                return ulog
            else:
                ulog.set_status_code(read_log.get_status_code())
                ulog.set_status_message(read_log.get_status_message())
                return ulog
        except Exception:
            ''' TODO: Eventually, this catch-all should be removed. '''
            ul = MvKUpdateLog()
            ul.set_status_code(UpdateConstants.INTERNAL_ERROR_CODE)
            tb = traceback.format_exc()
            print tb
            ul.set_status_message(StringValue(tb))
            assert logger.error(tb)
            return ul

    def delete(self, location):
        try:
            dlog = MvKDeleteLog()
            if not (isinstance(location, mvk.interfaces.datavalue.LocationValue) and
                    isinstance(location.typed_by(), mvk.interfaces.datatype.LocationType)):
                dlog.set_status_code(DeleteConstants.MALFORMED_REQUEST_CODE)
                dlog.set_status_message(StringValue('Expected a location value.'))
                return dlog
            if location == LocationValue(''):
                dlog.set_status_code(DeleteConstants.BAD_REQUEST_CODE)
                dlog.set_status_message(StringValue('Cannot delete the root of \
                                                     the modelverse.'))
                return dlog
            read_log = self.read(location)
            if read_log.is_success():
                return read_log.get_item().delete()
            else:
                dlog.set_status_code(read_log.get_status_code())
                dlog.set_status_message(read_log.get_status_message())
                return dlog
        except Exception:
            ''' TODO: Eventually, this catch-all should be removed. '''
            dl = MvKDeleteLog()
            dl.set_status_code(DeleteConstants.INTERNAL_ERROR_CODE)
            tb = traceback.format_exc()
            print tb
            dl.set_status_message(StringValue(tb))
            assert logger.error(tb)
            return dl

    def clear(self):
        protected = None
        try:
            protected = self.root.get_element(StringValue('protected'))
        except MvKKeyError:
            pass
        self.root = RootPackage(name=StringValue(''))
        if protected:
            self.root.add_element(protected)

    def apply(self, params):
        clog = MvKLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            clog.set_status_code(LogConstants.MALFORMED_REQUEST_CODE)
            clog.set_status_message(StringValue('Expected a MappingValue'))
            return clog
        if not LogConstants.OPERATION_NAME_KEY in params:
            clog.set_status_code(LogConstants.MALFORMED_REQUEST_CODE)
            clog.set_status_message(StringValue('Expected an operation name.'))
            return clog
        op_name = params[LogConstants.OPERATION_NAME_KEY]
        if op_name == CRUDConstants.CREATE_OPERATION:
            return self.create(params)
        elif op_name == CRUDConstants.READ_OPERATION:
            if not ReadConstants.LOCATION_KEY in params:
                clog.set_status_code(LogConstants.MALFORMED_REQUEST_CODE)
                clog.set_status_message(StringValue('Expected a location.'))
                return clog
            return self.read(params[ReadConstants.LOCATION_KEY])
        elif op_name == CRUDConstants.UPDATE_OPERATION:
            return self.update(params)
        elif op_name == CRUDConstants.DELETE_OPERATION:
            if not DeleteConstants.LOCATION_KEY in params:
                clog.set_status_code(LogConstants.MALFORMED_REQUEST_CODE)
                clog.set_status_message(StringValue('Expected a location.'))
                return clog
            return self.delete(params[ReadConstants.LOCATION_KEY])
        elif op_name == CRUDConstants.COMPOSITE_OPERATION:
            if not CompositeConstants.LOGS_KEY in params:
                clog.set_status_code(LogConstants.MALFORMED_REQUEST_CODE)
                clog.set_status_message(StringValue('Expected logs.'))
                return clog
            logs = params[CompositeConstants.LOGS_KEY]
            if not (isinstance(logs, mvk.interfaces.datavalue.SequenceValue) and
                    isinstance(logs.typed_by(), mvk.interfaces.datatype.SequenceType)):
                clog.set_status_code(LogConstants.MALFORMED_REQUEST_CODE)
                clog.set_status_message(StringValue('Expected logs to be a SequenceValue'))
                return clog
            ret_log = MvKCompositeLog()
            it = logs.__iter__()
            while it.has_next():
                ret_log.add_log(self.apply(it.next()))
            return ret_log

    ''' === PYTHON SPECIFIC === '''
    @classmethod
    def types(cls):
        return {cls.MODEL: Model,
                cls.CLABJECT: Clabject,
                cls.ASSOCIATION: Association,
                cls.COMPOSITION: Composition,
                cls.AGGREGATION: Aggregation,
                cls.ATTRIBUTE: Attribute,
                cls.PACKAGE: Package,
                cls.INHERITS: Inherits,
                cls.FUNCTION: Function,
                cls.BODY: Body,
                cls.PARAMETER: Parameter,
                cls.EXPRESSIONSTATEMENT: ExpressionStatement,
                cls.RETURNSTATEMENT: ReturnStatement,
                cls.DECLARATIONSTATEMENT: DeclarationStatement,
                cls.WHILELOOP: WhileLoop,
                cls.IFSTATEMENT: IfStatement,
                cls.BREAKSTATEMENT: BreakStatement,
                cls.CONTINUESTATEMENT: ContinueStatement,
                cls.CONSTANT: Constant,
                cls.IDENTIFIER: Identifier,
                cls.NAVIGATION: Navigation,
                cls.ASSIGNMENT: Assignment,
                cls.FUNCTIONCALL: FunctionCall,
                cls.ARGUMENT: Argument,
                cls.NOT: Not,
                cls.OR: Or,
                cls.AND: And,
                cls.EQUAL: Equal,
                cls.LESSTHAN: LessThan,
                cls.GREATERTHAN: GreaterThan,
                cls.IN: In,
                cls.PLUS: Plus,
                cls.MINUS: Minus,
                cls.MULTIPLICATION: Multiplication,
                cls.DIVISION: Division,
                cls.MODULO: Modulo}

    def _create_unknown(self, params):
        clog = MvKCreateLog()
        clog.set_status_code(CreateConstants.BAD_REQUEST_CODE)
        clog.set_status_message(StringValue('Unknown physical type.'))
        return clog

    def backup(self, filename=None):
        olog = MvKOperationLog(StringValue("backup"))
        if not filename:
            filename = StringValue('backup')
        assert isinstance(filename, mvk.interfaces.datavalue.StringValue)
        with open(str(filename), 'wb') as f:
            pickle.dump(self.root, f, protocol=pickle.HIGHEST_PROTOCOL)
        olog.set_result(StringValue("OK"))
        olog.set_status_code(LogConstants.SUCCESS_CODE)
        olog.set_status_message(StringValue("Backed up modelverse to file " + str(filename)))
        return olog

    def restore(self, filename=None):
        olog = MvKOperationLog(StringValue("restore"))
        if not filename:
            filename = StringValue('backup')
        assert isinstance(filename, mvk.interfaces.datavalue.StringValue)
        with open(str(filename), 'rb') as f:
            self.root = pickle.load(f)
        olog.set_result(StringValue("OK"))
        olog.set_status_code(LogConstants.SUCCESS_CODE)
        olog.set_status_message(StringValue("Restored modelverse from file " + str(filename)))
        return olog

    def get_root(self):
        return self.root
