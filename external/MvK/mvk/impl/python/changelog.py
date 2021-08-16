'''
Created on 25-feb.-2014

@author: Simon
'''
from mvk.impl.python.constants import LogConstants, CRUDConstants, \
    CreateConstants, UpdateConstants, ReadConstants, ChangelogConstants, DeleteConstants
from mvk.impl.python.datatype import StringType, LocationType
from mvk.impl.python.datavalue import StringValue, MappingValue, \
    SequenceValue, ImmutableSequenceValue, BooleanValue, \
    LocationValue, VoidValue, IntegerValue
import mvk.interfaces.changelog

class MvKLog(MappingValue, mvk.interfaces.changelog.MvKLog):
    """ === CONSTRUCTOR === """
    def __init__(self, operation_name, **kwargs):
        assert (isinstance(operation_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(operation_name.typed_by(), mvk.interfaces.datatype.StringType))
        kwargs.setdefault("value", {})
        super(MvKLog, self).__init__(**kwargs)
        self[LogConstants.OPERATION_NAME_KEY] = operation_name

    """ === PUBLIC INTERFACE === """
    def get_status_code(self):
        return self[LogConstants.STATUS_CODE_KEY]

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            LogConstants.succes_codes())

    def get_status_message(self):
        return self[LogConstants.STATUS_MESSAGE_KEY]

    def get_operation_name(self):
        return self[LogConstants.OPERATION_NAME_KEY]

    """ === PYTHON SPECIFIC === """
    def set_status_code(self, status_code):
        assert (isinstance(status_code, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(status_code.typed_by(), mvk.interfaces.datatype.IntegerType))
        self[LogConstants.STATUS_CODE_KEY] = status_code

    def set_status_message(self, status_message):
        assert (isinstance(status_message, mvk.interfaces.datavalue.StringValue) and
                isinstance(status_message.typed_by(), mvk.interfaces.datatype.StringType))
        self[LogConstants.STATUS_MESSAGE_KEY] = status_message


class MvKOperationLog(MvKLog,
                      mvk.interfaces.changelog.MvKOperationLog):
    """ === CONSTRUCTOR === """
    def __init__(self, operation_name, **kwargs):
        super(MvKOperationLog, self).__init__(operation_name=operation_name,
                                              **kwargs)

    """ === PUBLIC INTERFACE === """
    def get_result(self):
        return self[StringValue("result")]

    """ === PYTHON SPECIFIC === """
    def set_result(self, result):
        self[StringValue("result")] = result


class MvKCRUDLog(MvKLog, mvk.interfaces.changelog.MvKCRUDLog):
    """ === PUBLIC INTERFACE === """
    def get_location(self):
        return self[CRUDConstants.LOCATION_KEY]

    def get_type(self):
        return self[CRUDConstants.TYPE_KEY]

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            CRUDConstants.succes_codes())

    """ === PYTHON SPECIFIC === """
    def set_location(self, location):
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))
        self[CRUDConstants.LOCATION_KEY] = location

    def set_type(self, the_type):
        self[CRUDConstants.TYPE_KEY] = the_type


class MvKChangelog(MvKCRUDLog, mvk.interfaces.changelog.MvKChangelog):
    """ === PUBLIC INTERFACE === """
    def get_inverse(self):
        raise NotImplementedError()

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            ChangelogConstants.succes_codes())


class MvKCreateLog(MvKChangelog, mvk.interfaces.changelog.MvKCreateLog):
    """ === CONSTRUCTOR === """
    def __init__(self, **kwargs):
        super(MvKCreateLog, self).__init__(operation_name=CRUDConstants.CREATE_OPERATION,
                                           **kwargs)
        if not CreateConstants.ATTRS_KEY in self:
            self[CreateConstants.ATTRS_KEY] = SequenceValue()

    """ === PUBLIC INTERFACE === """
    def get_changes(self):
        return ImmutableSequenceValue(self[CreateConstants.ATTRS_KEY])

    def get_name(self):
        return self[CreateConstants.NAME_KEY]

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            CreateConstants.succes_codes())

    """ === PYTHON SPECIFIC === """
    def add_attr_change(self, attr_name, val):
        assert (isinstance(attr_name, StringValue) and
                isinstance(attr_name.typed_by(), StringType))
        self[CreateConstants.ATTRS_KEY].append(MappingValue({CreateConstants.NAME_KEY: attr_name,
                                                             CreateConstants.VALUE_KEY: val})
                                               )

    def set_name(self, name):
        assert (isinstance(name, StringValue) and
                isinstance(name.typed_by(), StringType))
        self[CreateConstants.NAME_KEY] = name


    def get_inverse(self):
        # We need to issue a delete of the location we just created
        if self.is_success():
            baseloc = self[CreateConstants.LOCATION_KEY]
            if baseloc.len().get_value() > 0:
                return [("delete", baseloc + LocationValue(".") + self.get_name())]
            else:
                return [("delete", LocationValue(self.get_name().get_value()))]
        else:
            return []

class MvKReadLog(MvKCRUDLog, mvk.interfaces.changelog.MvKReadLog):
    """ === CONSTRUCTOR === """
    def __init__(self, **kwargs):
        super(MvKReadLog, self).__init__(operation_name=CRUDConstants.READ_OPERATION,
                                         **kwargs)

    """ === PUBLIC INTERFACE === """
    def get_item(self):
        return self[ReadConstants.ITEM_KEY]

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            ReadConstants.succes_codes())

    """ === PYTHON SPECIFIC === """
    def set_item(self, item):
        assert isinstance(item, mvk.interfaces.element.Element)
        self[ReadConstants.ITEM_KEY] = item


class MvKUpdateLog(MvKChangelog, mvk.interfaces.changelog.MvKUpdateLog):
    """ === CONSTRUCTOR === """
    def __init__(self, **kwargs):
        super(MvKUpdateLog, self).__init__(operation_name=CRUDConstants.UPDATE_OPERATION,
                                           **kwargs)
        if not UpdateConstants.ATTRS_KEY in self:
            self[UpdateConstants.ATTRS_KEY] = SequenceValue()

    """ === PUBLIC INTERFACE === """
    def get_changes(self):
        return ImmutableSequenceValue(self[UpdateConstants.ATTRS_KEY])

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            UpdateConstants.succes_codes())

    """ === PYTHON SPECIFIC === """
    def add_attr_change(self, attr_name, old_val, new_val):
        assert (isinstance(attr_name, StringValue) and
                isinstance(attr_name.typed_by(), StringType))
        self[UpdateConstants.ATTRS_KEY].append(MappingValue({UpdateConstants.NAME_KEY: attr_name,
                                                             UpdateConstants.OLD_VAL_KEY: old_val,
                                                             UpdateConstants.NEW_VAL_KEY: new_val})
                                               )

    def get_inverse(self):
        # Update in the other direction
        if not self.is_success():
            return []
        attrs = {}
        for m in self[UpdateConstants.ATTRS_KEY]:
            attr = m[UpdateConstants.NAME_KEY]
            old = m[UpdateConstants.OLD_VAL_KEY]
            attrs[attr] = old
            
        return [("update", MappingValue({UpdateConstants.LOCATION_KEY: self[UpdateConstants.LOCATION_KEY],
                                         UpdateConstants.TYPE_KEY: self[UpdateConstants.TYPE_KEY],
                                         UpdateConstants.ATTRS_KEY: MappingValue(attrs)}))]


class MvKDeleteLog(MvKChangelog, mvk.interfaces.changelog.MvKDeleteLog):
    """ === CONSTRUCTOR === """
    def __init__(self, **kwargs):
        super(MvKDeleteLog, self).__init__(operation_name=CRUDConstants.DELETE_OPERATION,
                                           **kwargs)
        self[StringValue('attributes')] = SequenceValue()

    """ === PUBLIC INTERFACE === """
    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            DeleteConstants.succes_codes())

    def set_item(self, item):
        self[DeleteConstants.ITEM_KEY] = item
        
    def add_attr(self, attr_name, val):
        assert (isinstance(attr_name, StringValue) and
                isinstance(attr_name.typed_by(), StringType))
        self[StringValue('attributes')].append(MappingValue({CreateConstants.NAME_KEY: attr_name,
                                                             CreateConstants.VALUE_KEY: val})
                                               )
    def get_inverse(self):
        if not self.is_success():
            return []
        location = self[DeleteConstants.LOCATION_KEY]
        item = self[DeleteConstants.ITEM_KEY]
        from mvk.impl.client.object import Package
        if isinstance(item, Package):
            # Packages cannot be reconstructed by undo'ing
            # However, the user currently cannot do this himself, so we assume that the next operations
            # will automatically create the required packages.
            return []

        l = location.get_value().rsplit('.', 1)
        # Strip of the name of the location
        #TODO fix this, doesn't work for attributes with a name containing a dot
        if len(l) == 1:
            # At root level
            location = LocationValue('')
        else:
            location = LocationValue(l[0])
        attrs = {}
        if isinstance(item, mvk.impl.client.object.Association):
            to = item.to_multiplicity
            fr = item.from_multiplicity
            attrs[StringValue("to_multiplicity")] = MappingValue({StringValue("port_name"): to.port_name,
                                                                  StringValue("node"): to.node,
                                                                  StringValue("ordered"): to.ordered,
                                                                  StringValue("lower"): to.lower,
                                                                  StringValue("upper"): to.upper})
            attrs[StringValue("from_multiplicity")] = MappingValue({StringValue("port_name"): fr.port_name,
                                                                  StringValue("node"): fr.node,
                                                                  StringValue("ordered"): fr.ordered,
                                                                  StringValue("lower"): fr.lower,
                                                                  StringValue("upper"): fr.upper})
        for attr in item.attributes:
            # Only add if we have a value
            if attr.potency == IntegerValue(0):
                attrs[attr.name] = attr.value

        params = {CreateConstants.TYPE_KEY: item.linguistic_type,
                  CreateConstants.LOCATION_KEY: location,
                  CreateConstants.ATTRS_KEY: MappingValue(attrs)}
        return [("create", MappingValue(params))]

class MvKCompositeLog(MvKChangelog, mvk.interfaces.changelog.MvKCompositeLog):
    """ === CONSTRUCTOR === """
    def __init__(self, logs=None, **kwargs):
        if logs is None:
            logs = SequenceValue([])
        self.logs = logs
        if not 'operation_name' in kwargs:
            super(MvKCompositeLog, self).__init__(operation_name=CRUDConstants.COMPOSITE_OPERATION,
                                                  **kwargs)
        else:
            super(MvKCompositeLog, self).__init__(**kwargs)

    """ === PUBLIC INTERFACE === """
    def get_logs(self):
        return ImmutableSequenceValue(self.logs)

    def is_success(self):
        for log in self.logs:
            if not log.is_success():
                return BooleanValue(False)
        return BooleanValue(True)

    """ === PYTHON SPECIFIC === """
    def add_log(self, log):
        assert isinstance(log, mvk.interfaces.changelog.MvKLog) and log.get_status_code()
        #if isinstance(log, MvKCompositeLog):
        if hasattr(log, "logs"):
            self.logs.extend(log.logs)
        else:
            self.logs.append(log)

    def __str__(self):
        return 'COMPOSITE(%s, %s)[%s]' % (self.get_status_code(),
                                          self.get_status_message(),
                                          ',\n'.join([str(l) for l in self.logs.get_value()]))

    def get_inverse(self):
        # Perform inverse operations in reverse order
        retval = []
        # Use the actual value inside, as reversed requires a __len__ method to be defined
        for log in reversed(self.logs.get_value()):
            retval.extend(log.get_inverse())
        return retval


class MvKCreateCompositeLog(MvKCompositeLog, mvk.interfaces.changelog.MvKCreateCompositeLog):
    """ === CONSTRUCTOR === """
    def __init__(self, **kwargs):
        super(MvKCreateCompositeLog, self).__init__(**kwargs)
        self[CreateConstants.ATTRS_KEY] = SequenceValue()

    """ === PUBLIC INTERFACE === """
    def get_changes(self):
        return ImmutableSequenceValue(self[CreateConstants.ATTRS_KEY])

    def get_name(self):
        return self[CreateConstants.NAME_KEY]

    def is_success(self):
        return BooleanValue(self.get_status_code() in
                            CreateConstants.succes_codes())

    """ === PYTHON SPECIFIC === """
    def add_attr_change(self, attr_name, val):
        assert (isinstance(attr_name, StringValue) and
                isinstance(attr_name.typed_by(), StringType))
        self[CreateConstants.ATTRS_KEY].append(MappingValue({CreateConstants.NAME_KEY: attr_name,
                                                             CreateConstants.VALUE_KEY: val})
                                               )

    def set_name(self, name):
        assert (isinstance(name, StringValue) and
                isinstance(name.typed_by(), StringType))
        self[CreateConstants.NAME_KEY] = name

    def get_inverse(self):
        # Only remove the packages that were created and ourself
        # A revertion will not be necessary for the others (lower) elements, as this happens automatically
        logs = self.logs.get_value()
        if len(logs) > 0:
            inverse = []
            if logs[0][CreateConstants.TYPE_KEY] == LocationValue("mvk.object.Package"):
                # We created a package for this create, so queue a deletion for this package
                inverse = logs[0].get_inverse()
            for log in logs:
                # First iterate over all the packages
                if log[CreateConstants.TYPE_KEY] == LocationValue("mvk.object.Package"):
                    continue

                # Next thing that was created will be the model itself, so invert that one too
                package_inverse, inverse = inverse, log.get_inverse()
                inverse.extend(package_inverse)

                # And we are done after that, as the rest was made automatically
                break
            return inverse
        else:
            return []

    def __str__(self):
        return "CREATE" + str(super(MvKCreateCompositeLog, self).__str__())

class MvKDeleteCompositeLog(MvKCompositeLog, mvk.interfaces.changelog.MvKDeleteCompositeLog):
    pass

class MvKReadCompositeLog(MvKCompositeLog, mvk.interfaces.changelog.MvKDeleteCompositeLog):
    def get_inverse(self):
        return []
