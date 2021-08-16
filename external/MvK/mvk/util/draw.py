'''
@author: Maris Jukss
'''

from mvk.impl.python.datatype import TypeFactory, StringType, BooleanType, \
    TypeType, AnyType, IntegerType
from mvk.impl.python.changelog import MvKCompositeLog
from mvk.impl.python.constants import CreateConstants, CRUDConstants
from mvk.impl.python.datatype import StringType
from mvk.impl.python.datavalue import StringValue, IntegerValue, LocationValue, \
    MappingValue, SequenceValue, BooleanValue, InfiniteValue
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.datavalue
#import mvk as mvk
from mvk.mvk import MvK
import pydot
import cairo
import datetime
from unittest import TestCase
import os

class Draw(object):
    def __init__(self,name):
        pass
    
    '''Plot the model specified in location using pydot. nice to visualize what's inside MvK'''
    '''Not tested for the protected formalisms and metamodels. Works on instances.'''  
    @staticmethod
    def plot(location,id='',path='graphs'):
        model_class = MvK().read(LocationValue('protected.formalisms.SimpleClassDiagrams.Class')).get_item()
        association_class = MvK().read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association')).get_item()
        model = MvK().read(location).get_item()
        it = iter(model.get_elements())
        nodes_ = []
        edges_ = []
        while it.has_next():
            el = model.get_element(next(it))
            if isinstance(el, mvk.interfaces.object.Association):
                edges_.append(el)
            elif isinstance(el,mvk.interfaces.object.Clabject):
                nodes_.append(el)
        attrs=''
        nodes ={}
        dateTag = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
        graph = pydot.Dot(dateTag, graph_type='digraph')
        for node in nodes_:
            it = iter(node.get_attributes())
            name = str(node.name)
            while it.has_next():
                data = next(it)
                attrs += "%s->%s\n"%(data.get_name(),data.get_value())
            attrs = attrs.replace("-","\-")
            attrs = attrs.replace("\n","\\n")
            attrs = attrs.replace("[","\[")
            attrs = attrs.replace("]","\]")
            #NEED UNIQUE IDENTIFIER FROM NODES HERE. WHAT IF id_field is not set? and name, id attributes are not defined?
            nodes[name] = pydot.Node(attrs)  
            graph.add_node(nodes[name])
            attrs = ''
        for edge in edges_:
            it = iter(edge.get_attributes())
            while it.has_next():
                data = next(it)
                attrs += "%s->%s\n"%(data.get_name(),data.get_value())
            src = str(edge.get_from_multiplicity().get_node().name)
            trg = str(edge.get_to_multiplicity().get_node().name)
            attrs = attrs.replace("-","\-")
            attrs = attrs.replace("\n","\\n")
            attrs = attrs.replace("[","\[")
            attrs = attrs.replace("]","\]")
            if not src in nodes or not trg in nodes:
                attrs = ''
                continue
            graph.add_edge(pydot.Edge(nodes[src],nodes[trg],label=attrs))
            attrs = ''
            #layout = self.layout_kamada_kawai()
            #ig.plot(self, layout=layout, bbox = (1000, 1000), margin = 20)
            #print self.name.split('/')[len(self.name.split('/'))-1]
        if not id:
            id = str(location)
        file = '%s/%s%s.svg'%(path,id,dateTag)
        fn = os.path.join(os.path.dirname(__file__),file)
        graph.write_svg(fn)     


