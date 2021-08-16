'''
Created on 25-feb.-2014

@author: Simon
'''
import mvk.interfaces.datavalue


class MvKLog(mvk.interfaces.datavalue.MappingValue):
    def get_status_code(self):
        """
        Returns the status code of this log. Consult the documentation for
        an overview of possible status codes.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The status code of this log.
        """
        raise NotImplementedError()

    def is_success(self):
        """
        Returns whether or not the operation performed was a succes.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: Whether or not the operation performed was a succes.
        """
        raise NotImplementedError()

    def get_status_message(self):
        """
        Returns the status message associated with this log.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The status message associated with this log.
        """
        raise NotImplementedError()

    def get_operation_name(self):
        """
        Returns the name of the performed operation.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The name of the performed operation.
        """
        raise NotImplementedError()


class MvKOperationLog(MvKLog):
    def get_result(self):
        """
        Returns the result of the operation.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The result of the operation.
        """
        raise NotImplementedError()


class MvKCRUDLog(MvKLog):
    def get_location(self):
        """
        Returns the location of the element on which the operation was performed.
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: The location of the element on which the operation was performed.
        """
        raise NotImplementedError()

    def get_physical_type(self):
        """
        Returns the physical type of the element on which the operation was
        performed. Consult the documentation for an overview of the possible
        physical types, and their mapping onto integer values.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The physical type of the element on which the operation was performed.
        """
        raise NotImplementedError()


class MvKChangelog(MvKCRUDLog):
    def get_inverse(self):
        """
        Returns the inverse of this changelog. Used for undoing operations.
        @rtype: L{MvKChangelog}
        @return: The inverse of this changelog. Used for undoing operations.
        """
        raise NotImplementedError()


class MvKCreateLog(MvKChangelog):
    def get_name(self):
        """
        Returns the name of the created item.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The name of the created item.
        """
        raise NotImplementedError()


class MvKReadLog(MvKCRUDLog):
    def get_item(self):
        """
        Returns the item which was read.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The item which was created.
        """
        raise NotImplementedError()


class MvKUpdateLog(MvKChangelog):
    def get_changes(self):
        """
        Returns the performed changes.
        @rtype: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @return: The performed changes.
        """
        raise NotImplementedError()


class MvKDeleteLog(MvKChangelog):
    pass


class MvKCompositeLog(MvKChangelog):
    def get_logs(self):
        """
        Returns the logs composted by this log.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The logs composted by this log.
        """
        raise NotImplementedError()


class MvKCreateCompositeLog(MvKCompositeLog, MvKCreateLog):
    pass

class MvKDeleteCompositeLog(MvKCompositeLog, MvKCreateLog):
    pass
