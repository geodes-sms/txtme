"""
Created on 28-dec.-2013

@author: Simon
"""
import os

import cPickle as pickle
from impl.formalisms.ActionMapper import ActionMapper
from impl.formalisms.MultiMapper import MDMapper
from impl.formalisms.SCDMapper import SCDMapper
from impl.python.changelog import MvKOperationLog, MvKReadLog, MvKReadCompositeLog
from impl.python.constants import LogConstants, ReadConstants
from impl.python.datavalue import LocationValue, StringValue, SetValue, BooleanValue, IntegerValue, SequenceValue
import impl.python.exception
from impl.python.python_representer import PythonRepresenter
import interfaces.datavalue
from interfaces.exception import MvKException, MvKKeyError
from util.singleton import Singleton
from random import Random


class MvK(Singleton):
    """
    MvK is the main entry point for the modelverse. It exposes
    a CRUD interface, which allows models in the modelverse to be
    manipulated. It is a Singleton, as there is only one entry point
    by which all requests need to pass.

    The MvK is a class which wraps one or more Representers, which have
    the task of actually representing the created objects as physical
    objects in a store. As such, the MvK in its simplest form merely
    passes on requests to its sole Representer.

    The interface of the MvK only uses interface classes defined in the
    'interfaces' package. This is to allow Representers which are not
    programmed in Python (but which do implement the Representer Python
    interface and know about the interface classes in the MvK) to
    be easily programmed: no conversion from Python has to happen, because
    everything is handled through standardized interfaces.
    """
    __representer = PythonRepresenter()
    __mappers_hierarchy = {LocationValue('mvk'): {LocationValue(''): __representer},
                           LocationValue('protected'): {LocationValue('formalisms'): {LocationValue('SimpleClassDiagrams'): {LocationValue(''): SCDMapper()},
                                                                                      LocationValue('MultiDiagrams'): {LocationValue(''): MDMapper()},
                                                                                      LocationValue('ActionLanguage'): {LocationValue(''): ActionMapper()}}
                                                        }
                           }

    def __init__(self):
        super(MvK, self).__init__()
        self._randomGen = Random(0)
        self.clear()

    def __longest_prefix_item(self, location):
        splitted = location.split(LocationValue('.'))

        curr_map = self.__mappers_hierarchy
        for val in splitted:
            if val in curr_map:
                curr_map = curr_map[val]

        if LocationValue('') in curr_map:
            return curr_map[LocationValue('')]
        else:
            from impl.python.exception import MvKKeyError
            raise MvKKeyError(StringValue('No mapper found for %s.' %
                                          location))

    ''' == MvK Management Operations == '''
    def register_mapper(self, location, mapper):
        '''
        Registers a mapper for creating types found in a specific location.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location where the types to be created are found.
        @type mapper: L{PhysicalMapper<mvk.interfaces.physical_mapper.PhysicalMapper>}
        @param mapper: The physical mapper responsible for creating types in the specified location.
        '''
        assert (isinstance(location, interfaces.datavalue.LocationValue) and
                isinstance(location.typed_by(), interfaces.datatype.LocationType))
        assert isinstance(mapper, interfaces.physical_mapper.PhysicalMapper)
        splitted = location.split(LocationValue('.'))

        curr_map = self.__mappers_hierarchy
        for val in splitted:
            curr_map = curr_map.setdefault(val, {})
        curr_map[LocationValue('')] = mapper

    def unregister_mapper(self, location):
        '''
        UnRegisters a mapper for creating types found in a specific location.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location where the types to be created are found.
        '''
        assert (isinstance(location, interfaces.datavalue.LocationValue) and
                isinstance(location.typed_by(), interfaces.datatype.LocationType))
        splitted = location.split(LocationValue('.'))

        try:
            curr_map = self.__mappers_hierarchy
            for val in splitted:
                curr_map = curr_map[val]
            del curr_map[LocationValue('')]
        except KeyError:
            from impl.python.exception import MvKKeyError
            raise MvKKeyError(StringValue('Did not find mapper for location %s' % location))

    def get_physical_mapper(self, location):
        '''
        Returns the physical mapper associated with the type on location.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location where the types to be created are found.
        @rtype: L{PhysicalMapper<mvk.interfaces.physical_mapper.PhysicalMapper>}
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: If the physical mapper for the location was not found.
        '''
        return self.__longest_prefix_item(location)

    ''' == CRUD == '''
    def create(self, params):
        """
        Creates an element using the passed parameters.
        @type params: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @param params: A dictionary of values for the to-be-created element.
        @rtype: L{MvKCreateLog<mvk.interfaces.changelog.MvKCreateLog>} or
                L{MvKCompositeLog<mvk.interfaces.changelog.MvKCompositeLog>}
        @return: The changelog corresponding to the operation performed.
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: If the physical mapper for the location was not found.
        """
        ''' TODO: Here, already check for necessary conditions: params is
        a MappingValue, and it contains three keys: type, location, and
        attributes. '''
        return self.get_physical_mapper(params[StringValue('type')]).create(params)

    def read(self, location):
        """
        Reads the element on the specified location.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location of the element to be read.
        @rtype: L{MvKReadLog<mvk.interfaces.changelog.MvKReadLog>}
        @return: The changelog corresponding to the operation performed.
        """
        if isinstance(location, SequenceValue):
            log = MvKReadCompositeLog()
            for l in location:
                log.add_log(self.read(l))
            log.set_status_code(ReadConstants.SUCCESS_CODE)
            log.set_status_message(StringValue("Success"))
            return log
        else:
            try:
                val = MvK.read_cache[location]
                if val.get_item().get_location() != location:
                    # Force a refresh of this entry
                    raise KeyError("LOCATION ERROR")
                return val
            except KeyError:
                # Not in cache, so do a real lookup
                log = self.__representer.read(location)
                if log.is_success():
                    # And now cache it
                    MvK.read_cache[location] = log
                return log

    def update(self, params):
        """
        Updates an element in the modelverse.
        @type params: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @param params: A dictionary of values, specifying the changes
        to be performed.
        @rtype: L{MvKUpdateLog<mvk.interfaces.changelog.MvKUpdateLog>} or
                L{MvKCompositeLog<mvk.interfaces.changelog.MvKCompositeLog>}
        @return: The changelog corresponding to the operation performed.
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: If the physical mapper for the location was not found.
        """
        return self.get_physical_mapper(params[StringValue('type')]).update(params)

    def delete(self, location):
        """
        Deletes an element from the modelverse.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location of the element to be read.
        @rtype: L{MvKDeleteLog<mvk.interfaces.changelog.MvKDeleteLog>} or
                L{MvKCompositeLog<mvk.interfaces.changelog.MvKCompositeLog>}
        @return: The changelog corresponding to the operation performed.
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: If the physical mapper for the location was not found.
        """
        dl = self.__representer.delete(location)
        try:
            self.unregister_mapper(location)
        except (MvKKeyError, impl.python.exception.MvKKeyError):
            pass
        return dl

    def clear(self):
        """
        Clears the modelverse.
        """
        dirname = os.path.dirname(__file__)
        return self.restore(StringValue(dirname[:dirname.find('mvk') + 3] + '/' + 'protected'))

    def apply(self, params):
        """
        Applies an operation specified in the 'params' parameter. This is
        most often used when inverting a specific operation.
        @type params: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @param params: The parameters specifying the operation to be performed.
        @rtype: L{MvKChangeLog<mvk.interfaces.changelog.MvKChangeLog>}
        @return: The changelog corresponding to the operation performed.
        """
        return self.__representer.apply(params)

    def backup(self, filename=None):
        """
        Backs up the modelverse. Default file name: backup. If given a file name, it will save in <filename>.
        """
        log = MvKOperationLog(operation_name=StringValue("backup"))
        try:
            if not filename:
                filename = StringValue('backup')
            assert isinstance(filename, interfaces.datavalue.StringValue)
            import os
            str_filename = filename.get_value().replace('/', os.sep)
            if ".." in str_filename or str_filename.startswith(os.sep):
                log.set_result(SequenceValue())
                log.set_status_code(LogConstants.BAD_REQUEST_CODE)
                log.set_status_message(StringValue("Not allowed to read this folder"))
                return log
            if os.sep in str_filename and not os.path.exists(str_filename.rsplit(os.sep, 1)[0]):
                os.makedirs(str_filename.rsplit(os.sep, 1)[0])
            with open('%s' % str(filename), 'wb') as f:
                pickle.dump((self.__representer, self.__mappers_hierarchy), f, protocol=pickle.HIGHEST_PROTOCOL)
            log.set_result(filename)
            log.set_status_code(LogConstants.SUCCESS_CODE)
            log.set_status_message(StringValue("Success"))
        except:
            log.set_result(filename)
            log.set_status_code(LogConstants.INTERNAL_ERROR_CODE)
            log.set_status_message(StringValue("Backup failed"))
        return log

    def restore(self, filename=None):
        """
        Restores the modelverse from a previously made backup.
        """
        MvK.read_cache = {}
        log = MvKOperationLog(operation_name=StringValue("restore"))
        try:
            if not filename:
                filename = StringValue('backup')
            assert isinstance(filename, interfaces.datavalue.StringValue)
            str_filename = filename.get_value().replace('/', os.sep)
            with open('%s' % str(filename), 'rb') as f:
                self.__representer, self.__mappers_hierarchy = pickle.load(f)
            log.set_result(filename)
            log.set_status_code(LogConstants.SUCCESS_CODE)
            log.set_status_message(StringValue("Success"))
        except:
            log.set_result(filename)
            log.set_status_code(LogConstants.INTERNAL_ERROR_CODE)
            log.set_status_message(StringValue("Restore failed"))
        return log

    def run(self, op_name, **params):
        """
        Applies a specific operation in the representer and returns its result.
        @type op_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param op_name: The name of the operation to be performed.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The return value of the operation.
        """
        representer = self.__representer
        return eval('representer.%s(**params)' % op_name)

    def execute(self, location, *args):
        """
        Executes an element (usually a function, action, or constraint) in the
        Modelverse and returns its result.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location of the element to be executed.
        @rtype: L{MvKLog<mvk.interfaces.changelog.MvKLog>}
        @return: The return value of the operation.
        TODO: Implement.
        """
        if location == "protected.formalisms.MT.functions.packet_in":
            from plugins.transformation.algorithm import packet_in
            primitive = args[0]
            packet = args[1]
            log = MvKOperationLog(operation_name=StringValue("protected.formalisms.MT.functions.packet_in"))
            packet = packet_in(primitive,packet)
            log.set_result(packet)
            log.set_status_code(LogConstants.SUCCESS_CODE) 
            return log
        elif location == "protected.formalisms.MT.functions.next_in":
            from plugins.transformation.algorithm import next_in
            primitive = args[0]
            packet = args[1]
            log = MvKOperationLog(operation_name=StringValue("protected.formalisms.MT.functions.packet_in"))
            packet = next_in(primitive,packet)
            log.set_result(packet)
            log.set_status_code(LogConstants.SUCCESS_CODE)
            return log
        elif location == "protected.formalisms.MT.functions.ramify":
            from plugins.transformation.algorithm import ramify
            location = args[0]
            log = MvKOperationLog(operation_name=StringValue("protected.formalisms.MT.functions.ramify"))
            ramify(location)
            log.set_result(True)
            log.set_status_code(LogConstants.SUCCESS_CODE) 
            return log
        elif location == "print":
            print(args[0])
            log = MvKOperationLog(operation_name=StringValue("print"))
            log.set_result(True)
            log.set_status_code(LogConstants.SUCCESS_CODE) 
            return log
        elif location == "plot":
            #do not use unless you have all necessary dependencies installed.
            from util import draw
            draw.Draw.plot(LocationValue(args[0]), args[1])
            log = MvKOperationLog(operation_name=StringValue("plot"))
            log.set_result(True)
            log.set_status_code(LogConstants.SUCCESS_CODE) 
            return log
        else:
            log = MvKOperationLog(operation_name=StringValue("plot"))
            log.set_result(False)
            log.set_status_code(LogConstants.METHOD_NOT_ALLOWED_CODE) 
            return log
    
    def conforms_to(self, model_loc, type_model_loc):
        """
        Checks whether a model (linguistically) conforms to a type model.
        @type model_loc: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param model_loc: The location of the model.
        @type type_model_loc: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param type_model_loc: The location of the type model.
        """
        log = MvKOperationLog(operation_name=StringValue('conforms_to'))
        l = self.read(model_loc)
        if not l.is_success():
            log.set_status_code(l.get_status_code())
            log.set_status_message(l.get_status_message())
            return log
        m = l.get_item()
        if not isinstance(m, interfaces.object.Model):
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message('Given model is not a model!')
            return log
        l = self.read(type_model_loc)
        if not l.is_success():
            log.set_status_code(l.get_status_code())
            log.set_status_message(l.get_status_message())
            return log
        tm = l.get_item()
        if not isinstance(tm, interfaces.object.Model):
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message('Given type model is not a model!')
            return log
        res = BooleanValue(True)
        ''' 1. Check whether all types are present in the type model... '''
        type_map = {}
        types = {}
        elements = tm.get_elements()
        s_msg = StringValue('')

        for elem in elements:
            el = elements[elem]
            assert el.get_location() not in type_map

            type_map[el.get_location()] = []
            types[el.get_location()] = el

        elements = m.get_elements()
        FALSE = BooleanValue(False)

        ''' 2. Classify each element. '''
        for elem in elements:
            el = elements[elem]

            el_t = el.typed_by()
            t_loc = el_t.get_location()
            if not t_loc in type_map:
                res = FALSE
                s_msg = s_msg + StringValue('Could not find type %s of element %s' % (t_loc, el.get_name()))
            else:
                type_map[t_loc].append(el)
        ''' 3. Check multiplicities and attributes for each element, and out- and incoming cardinalities for associations. '''
        for t_loc in type_map:
            els = type_map[t_loc]
            t = types[t_loc]
            if IntegerValue(len(els)) < t.get_lower():
                res = FALSE
                s_msg = s_msg + StringValue('Minimal Cardinality (%i < %i) not satisfied for type %s\n' % (len(els), t.get_lower(), t_loc))
            elif IntegerValue(len(els)) > t.get_upper():
                res = FALSE
                s_msg = s_msg + StringValue('Maximal Cardinality (%i > %i) not satisfied for type %s\n' % (len(els), t.get_upper(), t_loc))
            for el in els:
                attrs = el.get_attributes()

                for attr in attrs:
                    if attr.get_potency() == IntegerValue(0):
                        try:
                            ''' check name '''
                            try:
                                attr_t = t.get_attribute(attr.get_name().substring(start=attr.get_name().find(StringValue('.')) + IntegerValue(1)))
                            except (MvKKeyError, impl.python.exception.MvKKeyError):
                                attr_t = t.get_attribute(attr.get_name())
                            ''' check value '''
                            if not attr_t.get_type().is_type_of(attr.get_value()):
                                res = FALSE
                                s_msg = s_msg + StringValue('Type of attribute %s (of element %s) does not match that of its type (%s != %s)\n' % (attr.get_name(), el.get_name(), attr.get_value().typed_by(), attr_t.get_type()))
                        except (MvKKeyError, impl.python.exception.MvKKeyError):
                            res = FALSE
                            s_msg = s_msg + StringValue('Could not find attribute definition for %s (of element %s)\n' % (attr.get_name(), el.get_name()))

                out_assocs = {}
                for a in el.get_all_out_associations():
                    if a.typed_by().get_location() in out_assocs:
                        out_assocs[a.typed_by().get_location()].append(a)
                    else:
                        out_assocs[a.typed_by().get_location()] = [a]

                for a in el.typed_by().get_all_out_associations():
                    if a.get_potency() > IntegerValue(0) and a.get_location() not in out_assocs:
                        out_assocs[a.get_location()] = []

                for a_t in out_assocs:
                    out_class = types[a_t].get_from_multiplicity().get_node()
                    if not (el.typed_by() == out_class or el.typed_by() in out_class.get_all_specialise_classes()):
                        s_msg = s_msg + StringValue('Invalid outgoing association %s from element %s\n' % (a_t, el.get_name()))
                        res = FALSE
                    min_out_c = types[a_t].get_to_multiplicity().get_lower()
                    max_out_c = types[a_t].get_to_multiplicity().get_upper()
                    if IntegerValue(len(out_assocs[a_t])) < min_out_c:
                        s_msg = s_msg + StringValue('Minimal Cardinality (%s < %s) not satisfied for outgoing association %s from element %s\n' % (len(out_assocs[a_t]), min_out_c, a_t, el.get_name()))
                        res = FALSE
                    elif IntegerValue(len(out_assocs[a_t])) > max_out_c:
                        s_msg = s_msg + StringValue('Maximal Cardinality (%s > %s) not satisfied for outgoing association %s from element %s\n' % (len(out_assocs[a_t]), max_out_c, a_t, el.get_name()))
                        res = FALSE

                in_assocs = {}
                for a in el.get_all_in_associations():
                    if a.typed_by().get_location() in in_assocs:
                        in_assocs[a.typed_by().get_location()].append(a)
                    else:
                        in_assocs[a.typed_by().get_location()] = [a]

                for a in el.typed_by().get_all_in_associations():
                    if a.get_potency() > IntegerValue(0) and a.get_location() not in in_assocs:
                        in_assocs[a.get_location()] = []

                for a_t in in_assocs:
                    in_class = types[a_t].get_to_multiplicity().get_node()
                    if not (el.typed_by() == in_class or el.typed_by() in in_class.get_all_specialise_classes()):
                        s_msg = s_msg + StringValue('Invalid incoming association %s from element %s\n' % (a_t, el.get_name()))
                        res = FALSE
                    min_out_c = types[a_t].get_from_multiplicity().get_lower()
                    max_out_c = types[a_t].get_from_multiplicity().get_upper()
                    if IntegerValue(len(in_assocs[a_t])) < min_out_c:
                        s_msg = s_msg + StringValue('Minimal Cardinality (%s < %s) not satisfied for incoming association %s to element %s\n' % (len(in_assocs[a_t]), min_out_c, a_t, el.get_name()))
                        res = FALSE
                    elif IntegerValue(len(in_assocs[a_t])) > max_out_c:
                        s_msg = s_msg + StringValue('Maximal Cardinality (%s > %s) not satisfied for incoming association %s to element %s\n' % (len(in_assocs[a_t]), max_out_c, a_t, el.get_name()))
                        res = FALSE
        log.set_result(res)
        log.set_status_code(LogConstants.SUCCESS_CODE)
        log.set_status_message(s_msg)
        return log

    ''' == OBJECT ACCESSOR METHODS == '''
    def __read_obj(self, loc, method_name):
        log = MvKOperationLog(operation_name=method_name)
        if not (isinstance(loc, interfaces.datavalue.LocationValue) and
                isinstance(loc.typed_by(), interfaces.datatype.LocationType)):
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message(StringValue('Location needs to be a LocationValue!'))
            return log
        rl = self.read(loc)
        if not rl.is_success():
            log.set_status_code(rl.get_status_code())
            log.set_status_message(rl.get_status_message())
            return log
        return rl

    def __obj_exec(self, loc, method_name, **params):
        l = self.__read_obj(loc, method_name)
        if not l.is_success():
            return l
        log = MvKOperationLog(operation_name=StringValue(method_name))
        item = l.get_item()
        try:
            res = getattr(item, method_name)(**params)
            log.set_result(res)
            log.set_status_code(LogConstants.SUCCESS_CODE)
            log.set_status_message(StringValue('Success!'))
        except MvKException, e:
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message(e.get_message())
        except AttributeError:
            log.set_status_code(LogConstants.METHOD_NOT_ALLOWED_CODE)
            log.set_status_message(StringValue('Could not execute method %s on element %s.' % (method_name, loc)))
        except Exception, e:
            log.set_status_code(LogConstants.INTERNAL_ERROR_CODE)
            log.set_status_message(StringValue(str(e)))
        return log

    def evaluate(self, method_name, *locs, **params):
        '''
        Evaluates a method on an object in the modelverse and returns the result, wrapped
        in an MvKOperationLog.
        @type method_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param method_name: The name of the method to execute (as it appears in the public interface of the element).
        @type locs: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param locs: A number of locations: the first one is used to look up the element on which to call the method. The rest are used
        as parameters: their order is preserved.
        @param params: A number of named parameters, which are passed to the method.
        @rtype: L{MvKOperationLog<mvk.interfaces.changelog.MvKOperationLog>}
        @return: The log holding the result (or the error message) of the method invocation.
        '''
        log = MvKOperationLog(operation_name=method_name)
        if not (isinstance(method_name, interfaces.datavalue.StringValue) and
                isinstance(method_name.typed_by(), interfaces.datatype.StringType)):
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message(StringValue('Method name needs to be a StringValue!'))
            return log
        if len(locs) == 0:
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message(StringValue('I need an object to execute the method on!'))
            return log
        read_objs = []
        for loc in locs:
            rl = self.__read_obj(loc, method_name)
            if not rl.is_success():
                return rl
            read_objs.append(rl.get_item())
        try:
            res = getattr(read_objs[0], str(method_name))(*read_objs[1:], **params)
            log.set_result(res)
            log.set_status_code(LogConstants.SUCCESS_CODE)
            log.set_status_message(StringValue('Success!'))
        except MvKException, e:
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message(e.get_message())
        except AttributeError:
            log.set_status_code(LogConstants.METHOD_NOT_ALLOWED_CODE)
            log.set_status_message(StringValue('Could not execute method %s on element %s.' % (method_name, loc)))
        except Exception, e:
            log.set_status_code(LogConstants.INTERNAL_ERROR_CODE)
            log.set_status_message(StringValue(str(e)))
        return log

    def get_files(self, foldername):
        log = MvKOperationLog(operation_name=StringValue("get_files"))
        foldername = foldername.get_value().replace("/", os.sep)
        if ".." in foldername or foldername.startswith(os.sep):
            log.set_result(SequenceValue())
            log.set_status_code(LogConstants.BAD_REQUEST_CODE)
            log.set_status_message(StringValue("Not allowed to read this folder"))
            return log
        if os.path.exists(foldername):
            log.set_result(SequenceValue([StringValue(f) for f in sorted(os.listdir(foldername))]))
        else:
            log.set_result(SequenceValue())
        log.set_status_code(LogConstants.SUCCESS_CODE)
        log.set_status_message(StringValue("Success"))
        return log
