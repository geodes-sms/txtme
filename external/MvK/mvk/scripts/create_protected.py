'''
Created on 4-apr.-2014

@author: Simon
'''
from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import StringType, BooleanType, TypeType, AnyType, IntegerType, TypeFactory, LocationType, MappingType,SequenceType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, IntegerValue, BooleanValue, AnyValue, InfiniteValue,SequenceValue
import mvk.interfaces.object
from mvk.mvk import MvK


def debug(defname, var):
    print(('\t' + defname + ': is_success() = True' if var.is_success() else '\t' + defname + ': is_success() = False'))

if __name__ == '__main__':
    mvkinst = MvK()

    ''' Action type model '''

    ## an action type model has a name attribute (as any other models)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms'),
                                      CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ActionLanguage'),
                                                                               StringValue('potency'): IntegerValue(1),
                                                                               StringValue('type_model'): LocationValue('mvk.object')})
                                      })
                        )
    debug('action type', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage'))
    debug('action type', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                      CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                               StringValue('type'): StringType(),
                                                                               StringValue('default'): StringValue(''),
                                                                               StringValue('potency'): IntegerValue(1),
                                                                               StringValue('lower'): IntegerValue(1),
                                                                               StringValue('upper'): IntegerValue(1),
                                                                               StringValue('class'): LocationValue('mvk.object.Attribute')})
                                      })
                        )
    debug('ActionLanguage.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.name'))
    debug('ActionLanguage.name', rl)

    ## Function related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Function'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Function', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Function'))
    debug('Function', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Function'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Function.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Function.name'))
    debug('Function.name', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Function'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('type'),
                                                                                StringValue('type'): TypeType(),
                                                                                StringValue('default'): AnyType(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Function.type', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Function.type'))
    debug('Function.type', rl)

    ## Body related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Body'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Body', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Body'))
    debug('Body', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Body'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Body.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Body.name'))
    debug('Body.name', rl)

    ## Parameter related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Parameter'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Parameter', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Parameter'))
    debug('Parameter', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Parameter.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Parameter.name'))
    debug('Parameter.name', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('type'),
                                                                                StringValue('type'): TypeType(),
                                                                                StringValue('default'): AnyType(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Parameter.type', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Parameter.type'))
    debug('Parameter.type', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('parameter_type'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue('in'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Parameter.parameter_type', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Parameter.parameter_type'))
    debug('Parameter.parameter_type', rl)

    ## Statement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Statement'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))

    debug('Statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Statement'))
    debug('Statement', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Statement'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Statement.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Statement.name'))
    debug('Statement.name', rl)

    ## ExpressionStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ExpressionStatement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('ExpressionStatement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement'))
    debug('ExpressionStatement', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('expressionstatement_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('expressionstatement_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.expressionstatement_i_statement'))
    debug('expressionstatement_i_statement', rl)

    ## ReturnStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ReturnStatement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('ReturnStatement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'))
    debug('ReturnStatement', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('returnstatement_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ReturnStatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('returnstatement_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.returnstatement_i_statement'))
    debug('returnstatement_i_statement', rl)

    ## DeclarationStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('DeclarationStatement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('DeclarationStatement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'))
    debug('DeclarationStatement', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('declarationstatement_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('declarationstatement_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.declarationstatement_i_statement'))
    debug('declarationstatement_i_statement', rl)

    ## WhileLoop related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('WhileLoop'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('WhileLoop', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.WhileLoop'))
    debug('WhileLoop', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('whileloop_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.WhileLoop')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('whileloop_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.whileloop_i_statement'))
    debug('whileloop_i_statement', rl)

    ## IfStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('IfStatement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('IfStatement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.IfStatement'))
    debug('IfStatement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstatement_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.IfStatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('ifstatement_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ifstatement_i_statement'))
    debug('ifstatement_i_statement', rl)

    ## BreakStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('BreakStatement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('BreakStatement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.BreakStatement'))
    debug('BreakStatement', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('breakstatement_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.BreakStatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('breakstatement_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.breakstatement_i_statement'))
    debug('breakstatement_i_statement', rl)

    ## ContinueStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ContinueStatement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('ContinueStatement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ContinueStatement'))
    debug('ContinueStatement', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('continuestatement_i_statement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ContinueStatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement')})
                                                                                })
                                       })
                         )
    debug('continuestatement_i_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.continuestatement_i_statement'))
    debug('continuestatement_i_statement', rl)

    ## Expression related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Expression'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Expression'))
    debug('Expression', rl)
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Expression.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Expression.name'))
    debug('Expression.name', rl)

    ## Constant related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Constant'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Constant', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Constant'))
    debug('Constant', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('constant_i_expression'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Constant')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression')})
                                                                                })
                                       })
                         )
    debug('constant_i_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.constant_i_expression'))
    debug('constant_i_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('type'),
                                                                                StringValue('type'): TypeType(),
                                                                                StringValue('default'): AnyType(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Constant.type', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Constant.type'))
    debug('Constant.type', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('value'),
                                                                                StringValue('type'): AnyType(),
                                                                                StringValue('default'): AnyValue(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Constant.value', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Constant.value'))
    debug('Constant.value', rl)

    ## Identifier related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Identifier'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Identifier', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Identifier'))
    debug('Identifier', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('identifier_i_expression'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Identifier')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression')})
                                                                                })
                                       })
                         )
    debug('identifier_i_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.identifier_i_expression'))
    debug('identifier_i_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Identifier'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('type'),
                                                                                StringValue('type'): TypeType(),
                                                                                StringValue('default'): AnyType(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Identifier.type', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Identifier.type'))
    debug('Identifier.type', rl)

    ## Navigation related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Navigation'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Navigation', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Navigation'))
    debug('Navigation', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('navigation_i_expression'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Navigation')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression')})
                                                                                })
                                       })
                         )
    debug('navigation_i_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.navigation_i_expression'))
    debug('navigation_i_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('path'),
                                                                                StringValue('type'): LocationType(),
                                                                                StringValue('default'): LocationValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Navigation.path', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Navigation.path'))
    debug('Navigation.path', rl)

    ## Assignment related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Assignment'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Assignment', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Assignment'))
    debug('Assignment', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('assignment_i_expression'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Assignment')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression')})
                                                                                })
                                       })
                         )
    debug('assignment_i_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.assignment_i_expression'))
    debug('assignment_i_expression', rl)

    ## FunctionCall related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('FunctionCall'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('FunctionCall', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.FunctionCall'))
    debug('FunctionCall', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('functioncall_i_expression'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.FunctionCall')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression')})
                                                                                })
                                       })
                         )
    debug('functioncall_i_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.functioncall_i_expression'))
    debug('functioncall_i_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.FunctionCall'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('function_name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('FunctionCall.function_name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.FunctionCall.function_name'))
    debug('FunctionCall.function_name', rl)

    ## Argument related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Argument'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Argument', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Argument'))
    debug('Argument', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Argument'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('key'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Argument.key', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Argument.key'))
    debug('Argument.key', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.Argument'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('Argument.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Argument.name'))
    debug('Argument.name', rl)

    ## Operator related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Operator'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Operator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Operator'))
    debug('Operator', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('operator_i_expression'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Operator')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression')})
                                                                                })
                                       })
                         )
    debug('operator_i_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.operator_i_expression'))
    debug('operator_i_expression', rl)

    ## UnaryOperator related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('UnaryOperator'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('UnaryOperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.UnaryOperator'))
    debug('UnaryOperator', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('unaryoperator_i_operator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.UnaryOperator')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Operator')})
                                                                                })
                                       })
                         )
    debug('unaryoperator_i_operator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.unaryoperator_i_operator'))
    debug('unaryoperator_i_operator', rl)

    ## Not related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Not'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Not', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Not'))
    debug('Not', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('not_i_unaryoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Not')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.UnaryOperator')})
                                                                                })
                                       })
                         )
    debug('not_i_unaryoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.not_i_unaryoperator'))
    debug('not_i_unaryoperator', rl)

    ## BinaryOperator related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('BinaryOperator'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('BinaryOperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.BinaryOperator'))
    debug('BinaryOperator', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('binaryoperator_i_operator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.BinaryOperator')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Operator')})
                                                                                })
                                       })
                         )
    debug('binaryoperator_i_operator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.binaryoperator_i_operator'))
    debug('binaryoperator_i_operator', rl)

    ## Or related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Or'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Or', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Or'))
    debug('Or', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('or_i_binaryoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Or')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.BinaryOperator')})
                                                                                })
                                       })
                         )
    debug('or_i_binaryoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.or_i_binaryoperator'))
    debug('or_i_binaryoperator', rl)

    ## And related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('And'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('And', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.And'))
    debug('And', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('and_i_binaryoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.And')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.BinaryOperator')})
                                                                                })
                                       })
                         )
    debug('and_i_binaryoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.and_i_binaryoperator'))
    debug('and_i_binaryoperator', rl)

    ## ComparisonOperator related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ComparisonOperator'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('ComparisonOperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ComparisonOperator'))
    debug('ComparisonOperator', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('comparisonoperator_i_binaryoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ComparisonOperator')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.BinaryOperator')})
                                                                                })
                                       })
                         )
    debug('comparisonoperator_i_binaryoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.comparisonoperator_i_binaryoperator'))
    debug('comparisonoperator_i_binaryoperator', rl)

    ## Equal related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Equal'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Equal', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Equal'))
    debug('Equal', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('equal_i_comparisonoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Equal')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ComparisonOperator')})
                                                                                })
                                       })
                         )
    debug('equal_i_comparisonoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.equal_i_comparisonoperator'))
    debug('equal_i_comparisonoperator', rl)

    ## LessThan related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('LessThan'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('LessThan', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.LessThan'))
    debug('LessThan', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('lessthan_i_comparisonoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.LessThan')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ComparisonOperator')})
                                                                                })
                                       })
                         )
    debug('lessthan_i_comparisonoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.lessthan_i_comparisonoperator'))
    debug('lessthan_i_comparisonoperator', rl)

    ## GreaterThan related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('GreaterThan'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('GreaterThan', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.GreaterThan'))
    debug('GreaterThan', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('greaterthan_i_comparisonoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.GreaterThan')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ComparisonOperator')})
                                                                                })
                                       })
                         )
    debug('greaterthan_i_comparisonoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.greaterthan_i_comparisonoperator'))
    debug('greaterthan_i_comparisonoperator', rl)

    ## ArithmeticOperator related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ArithmeticOperator'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('ArithmeticOperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator'))
    debug('ArithmeticOperator', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('arithmeticoperator_i_binaryoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.BinaryOperator')})
                                                                                })
                                       })
                         )
    debug('arithmeticoperator_i_binaryoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.arithmeticoperator_i_binaryoperator'))
    debug('arithmeticoperator_i_binaryoperator', rl)

    ## Plus related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Plus'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Plus', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Plus'))
    debug('Plus', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('plus_i_arithmeticoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Plus')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator')})
                                                                                })
                                       })
                         )
    debug('plus_i_arithmeticoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.plus_i_arithmeticoperator'))
    debug('plus_i_arithmeticoperator', rl)

    ## Minus related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Minus'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Minus', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Minus'))
    debug('Minus', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('minus_i_arithmeticoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Minus')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator')})
                                                                                })
                                       })
                         )
    debug('minus_i_arithmeticoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.minus_i_arithmeticoperator'))
    debug('minus_i_arithmeticoperator', rl)

    ## Multiplication related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Multiplication'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Multiplication', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Multiplication'))
    debug('Multiplication', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('multiplication_i_arithmeticoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Multiplication')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator')})
                                                                                })
                                       })
                         )
    debug('multiplication_i_arithmeticoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.multiplication_i_arithmeticoperator'))
    debug('multiplication_i_arithmeticoperator', rl)

    ## Division related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Division'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Division', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Division'))
    debug('Division', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('division_i_arithmeticoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Division')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator')})
                                                                                })
                                       })
                         )
    debug('division_i_arithmeticoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.division_i_arithmeticoperator'))
    debug('division_i_arithmeticoperator', rl)

    ## Modulo related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Modulo'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    debug('Modulo', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.Modulo'))
    debug('Modulo', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('modulo_i_arithmeticoperator'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Modulo')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ArithmeticOperator')})
                                                                                })
                                       })
                         )
    debug('modulo_i_arithmeticoperator', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.modulo_i_arithmeticoperator'))
    debug('modulo_i_arithmeticoperator', rl)

    ####### associations of the action metamodel bellow..

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('NamedElement'),
                                                                                StringValue('abstract'): BooleanValue(True),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})
                                       })
                         )
    debug('NamedElement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.NamedElement'))
    debug('NamedElement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage.NamedElement'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    debug('NamedElement.name', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.NamedElement.name'))
    debug('NamedElement.name', rl)

    # Function related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('function_body'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Function'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_function')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Body'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_body')})
                                                                                })
                                       })
                         )
    debug('function_body', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.function_body'))
    debug('function_body', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('function_body_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.function_body')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('function_body_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.function_body_i_namedelement'))
    debug('function_body_i_namedelement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('function_parameters'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Function'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_function')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_parameter')})
                                                                                })
                                       })
                         )
    debug('function_parameters', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.function_parameters'))
    debug('function_parameters', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('function_parameters_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.function_parameters')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('function_parameters_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.function_parameters_i_namedelement'))
    debug('function_parameters_i_namedelement', rl)

    # Body related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('body_statement'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Body'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_body')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Statement'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_statement')})
                                                                                })
                                       })
                         )
    debug('body_statement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.body_statement'))
    debug('body_statement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('body_statement_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.body_statement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('body_statement_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.body_statement_i_namedelement'))
    debug('body_statement_i_namedelement', rl)

    # ExpressionStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('expressionstatement_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_expressionstatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('expressionstatement_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.expressionstatement_expression'))
    debug('expressionstatement_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('expressionstatement_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.expressionstatement_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('expressionstatement_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.expressionstatement_expression_i_namedelement'))
    debug('expressionstatement_expression_i_namedelement', rl)

    # DeclarationStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('declarationstatement_identifier'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_declarationstatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Identifier'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_identifier')})
                                                                                })
                                       })
                         )
    debug('declarationstatement_identifier', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.declarationstatement_identifier'))
    debug('declarationstatement_identifier', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('declarationstatement_identifier_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.declarationstatement_identifier')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('declarationstatement_identifier_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.declarationstatement_identifier_i_namedelement'))
    debug('declarationstatement_identifier_i_namedelement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('declarationstatement_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_declarationstatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('declarationstatement_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.declarationstatement_expression'))
    debug('declarationstatement_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('declarationstatement_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.declarationstatement_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('declarationstatement_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.declarationstatement_expression_i_namedelement'))
    debug('declarationstatement_expression_i_namedelement', rl)

    # WhileLoop related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('whileloop_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.WhileLoop'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_whileloop')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('whileloop_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.whileloop_expression'))
    debug('whileloop_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('whileloop_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.whileloop_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('whileloop_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.whileloop_expression_i_namedelement'))
    debug('whileloop_expression_i_namedelement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('whileloop_body'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.WhileLoop'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_whileloop')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Body'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_body')})
                                                                                })
                                       })
                         )
    debug('whileloop_body', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.whileloop_body'))
    debug('whileloop_body', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('whileloop_body_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.whileloop_body')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('whileloop_body_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.whileloop_body_i_namedelement'))
    debug('whileloop_body_i_namedelement', rl)

    # IfStatement related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstatement_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.IfStatement'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_ifstatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('ifstatement_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ifstatement_expression'))
    debug('ifstatement_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstatement_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ifstatement_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('ifstatement_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ifstatement_expression_i_namedelement'))
    debug('ifstatement_expression_i_namedelement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstatement_body'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.IfStatement'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_ifstatement')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Body'),
                                                                                                                              StringValue('lower'): IntegerValue(2),
                                                                                                                              StringValue('upper'): IntegerValue(2),
                                                                                                                              StringValue('port_name'): StringValue('to_body')})
                                                                                })
                                       })
                         )
    debug('ifstatement_body', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ifstatement_body'))
    debug('ifstatement_body', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstatement_body_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.ifstatement_body')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('ifstatement_body_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.ifstatement_body_i_namedelement'))
    debug('ifstatement_body_i_namedelement', rl)

    # Assignment related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('assignment_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Assignment'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_assignment')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('assignment_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.assignment_expression'))
    debug('assignment_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('assignment_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.assignment_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('assignment_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.assignment_expression_i_namedelement'))
    debug('assignment_expression_i_namedelement', rl)

    # FunctionCall related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('functioncall_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.FunctionCall'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_functioncall')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('functioncall_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.functioncall_expression'))
    debug('functioncall_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('functioncall_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.functioncall_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('functioncall_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.functioncall_expression_i_namedelement'))
    debug('functioncall_expression_i_namedelement', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('functioncall_argument'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.FunctionCall'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_functioncall')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Argument'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_argument')})
                                                                                })
                                       })
                         )
    debug('functioncall_argument', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.functioncall_argument'))
    debug('functioncall_argument', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('functioncall_argument_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.functioncall_argument')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('functioncall_argument_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.functioncall_argument_i_namedelement'))
    debug('functioncall_argument_i_namedelement', rl)

    # Argument related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('argument_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Argument'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_argument')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(1),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('argument_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.argument_expression'))
    debug('argument_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('argument_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.argument_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('argument_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.argument_expression_i_namedelement'))
    debug('argument_expression_i_namedelement', rl)

    # Operator related
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('operator_expression'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Operator'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_operator')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.Expression'),
                                                                                                                              StringValue('lower'): IntegerValue(1),
                                                                                                                              StringValue('upper'): IntegerValue(2),
                                                                                                                              StringValue('port_name'): StringValue('to_expression')})
                                                                                })
                                       })
                         )
    debug('operator_expression', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.operator_expression'))
    debug('operator_expression', rl)

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('operator_expression_i_namedelement'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.operator_expression')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.ActionLanguage.NamedElement')})
                                                                                })
                                       })
                         )
    debug('operator_expression_i_namedelement', cl)
    rl = mvkinst.read(LocationValue('protected.formalisms.ActionLanguage.operator_expression_i_namedelement'))
    debug('operator_expression_i_namedelement', rl)

    ''' SimpleClassDiagrams type model '''
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('SimpleClassDiagrams'),
                                                                           StringValue('potency'): IntegerValue(2),
                                                                           StringValue('type_model'): LocationValue('mvk.object')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.name'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Class'),
                                                                               StringValue('abstract'): BooleanValue(False),
                                                                               StringValue('potency'): IntegerValue(2),
                                                                               StringValue('class'): LocationValue('mvk.object.Clabject')})}))

    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Class'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Class.name'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('is_abstract'),
                                                                           StringValue('type'): BooleanType(),
                                                                           StringValue('default'): BooleanValue(False),
                                                                           StringValue('potency'): IntegerValue(1),
                                                                           StringValue('lower'): IntegerValue(1),
                                                                           StringValue('upper'): IntegerValue(1),
                                                                           StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Class.is_abstract'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('id_field'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(0),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Class.id_field'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Attribute'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute.name'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('type'),
                                                                                StringValue('type'): TypeType(),
                                                                                StringValue('default'): AnyType(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute.type'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('default'),
                                                                                StringValue('type'): AnyType(),
                                                                                StringValue('default'): AnyValue(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute.default'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Association'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(2),
                                                                                StringValue('class'): LocationValue('mvk.object.Association'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                                StringValue('lower'): IntegerValue(0),
                                                                                                                                StringValue('upper'): InfiniteValue('+'),
                                                                                                                                StringValue('port_name'): StringValue('from_class')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_class')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('from_min'),
                                                                                StringValue('type'): IntegerType(),
                                                                                StringValue('default'): IntegerValue(0),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association.from_min'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('from_max'),
                                                                                StringValue('type'): TypeFactory.get_type('UnionType(IntegerType, InfiniteType)'),
                                                                                StringValue('default'): InfiniteValue('+'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association.from_max'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('from_port'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association.from_port'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('to_min'),
                                                                                StringValue('type'): IntegerType(),
                                                                                StringValue('default'): IntegerValue(0),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute'),
                                                                                StringValue('class'): LocationValue('mvk.object.Association')})
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association.to_min'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('to_max'),
                                                                                StringValue('type'): TypeFactory.get_type('UnionType(IntegerType, InfiniteType)'),
                                                                                StringValue('default'): InfiniteValue('+'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association.to_max'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('to_port'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Association.to_port'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Composition'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(2),
                                                                                StringValue('class'): LocationValue('mvk.object.Association'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                                StringValue('lower'): IntegerValue(0),
                                                                                                                                StringValue('upper'): InfiniteValue('+'),
                                                                                                                                StringValue('port_name'): StringValue('from_class')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_class')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Composition'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('comp_i_a'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Composition')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Association')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.comp_i_a'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Aggregation'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(2),
                                                                                StringValue('class'): LocationValue('mvk.object.Association'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                                StringValue('lower'): IntegerValue(0),
                                                                                                                                StringValue('upper'): InfiniteValue('+'),
                                                                                                                                StringValue('port_name'): StringValue('from_class')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_class')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Aggregation'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('aggr_i_a'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Aggregation')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Association')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.aggr_i_a'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Inheritance'),
                                                                           StringValue('abstract'): BooleanValue(False),
                                                                           StringValue('potency'): IntegerValue(1),
                                                                           StringValue('class'): LocationValue('mvk.object.Association'),
                                                                           StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                           StringValue('lower'): IntegerValue(0),
                                                                                                                           StringValue('upper'): InfiniteValue('+'),
                                                                                                                           StringValue('port_name'): StringValue('from_class')}),
                                                                           StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                         StringValue('lower'): IntegerValue(0),
                                                                                                                         StringValue('upper'): InfiniteValue('+'),
                                                                                                                         StringValue('port_name'): StringValue('to_class')})
                                                                           })
                                  })
                    )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'))
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance.name'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('a_i_c'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Association')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.a_i_c'))

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('attributes'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Association'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_class')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_attr')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.attributes'))
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.attributes'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})
                                  })
                    )
    rl = mvkinst.read(LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance.name'))

    ''' transformation type model '''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Transformation')})
                                  })
                        )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Transformation'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Rule'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                StringValue('Class.id_field'): StringValue('Rule.id')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                StringValue('Attribute.type'): StringType(),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('rule_loc'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('LocationType'),
                                                                                StringValue('Attribute.default'): LocationValue('')})
                                       })
                         )

    ''' MultiDiagrams type model '''
    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('MultiDiagrams'),
                                                                           StringValue('potency'): IntegerValue(2),
                                                                           StringValue('type_model'): LocationValue('mvk.object')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.name'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('potency'),
                                                                                StringValue('type'): TypeFactory.get_type('UnionType(IntegerType, InfiniteType)'),
                                                                                StringValue('default'): InfiniteValue('+'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.potency'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                      CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Clabject'),
                                                                               StringValue('abstract'): BooleanValue(False),
                                                                               StringValue('potency'): IntegerValue(2),
                                                                               StringValue('class'): LocationValue('mvk.object.Clabject')})}))

    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Clabject'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Clabject.name'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('is_abstract'),
                                                                           StringValue('type'): BooleanType(),
                                                                           StringValue('default'): BooleanValue(False),
                                                                           StringValue('potency'): IntegerValue(1),
                                                                           StringValue('lower'): IntegerValue(1),
                                                                           StringValue('upper'): IntegerValue(1),
                                                                           StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Clabject.is_abstract'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('id_field'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(0),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Clabject.id_field'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('potency'),
                                                                                StringValue('type'): TypeFactory.get_type('UnionType(IntegerType, InfiniteType)'),
                                                                                StringValue('default'): InfiniteValue('+'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Clabject.potency'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Attribute'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Clabject')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Attribute'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Attribute.name'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('type'),
                                                                                StringValue('type'): TypeType(),
                                                                                StringValue('default'): AnyType(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Attribute.type'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('default'),
                                                                                StringValue('type'): AnyType(),
                                                                                StringValue('default'): AnyValue(),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Attribute.default'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Attribute'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('potency'),
                                                                                StringValue('type'): TypeFactory.get_type('IntegerType'),
                                                                                StringValue('default'): IntegerValue(1),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Attribute.potency'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Association'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(2),
                                                                                StringValue('class'): LocationValue('mvk.object.Association'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                                StringValue('lower'): IntegerValue(0),
                                                                                                                                StringValue('upper'): InfiniteValue('+'),
                                                                                                                                StringValue('port_name'): StringValue('from_class')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_class')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('from_min'),
                                                                                StringValue('type'): IntegerType(),
                                                                                StringValue('default'): IntegerValue(0),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association.from_min'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('from_max'),
                                                                                StringValue('type'): TypeFactory.get_type('UnionType(IntegerType, InfiniteType)'),
                                                                                StringValue('default'): InfiniteValue('+'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association.from_max'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('from_port'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association.from_port'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('to_min'),
                                                                                StringValue('type'): IntegerType(),
                                                                                StringValue('default'): IntegerValue(0),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute'),
                                                                                StringValue('class'): LocationValue('mvk.object.Association')})
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association.to_min'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('to_max'),
                                                                                StringValue('type'): TypeFactory.get_type('UnionType(IntegerType, InfiniteType)'),
                                                                                StringValue('default'): InfiniteValue('+'),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association.to_max'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Association'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('to_port'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Association.to_port'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Composition'),
                                                                           StringValue('abstract'): BooleanValue(False),
                                                                           StringValue('potency'): InfiniteValue('+'),
                                                                           StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                           StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                           StringValue('lower'): IntegerValue(0),
                                                                                                                           StringValue('upper'): InfiniteValue('+'),
                                                                                                                           StringValue('port_name'): StringValue('from_class')}),
                                                                           StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                         StringValue('lower'): IntegerValue(0),
                                                                                                                         StringValue('upper'): InfiniteValue('+'),
                                                                                                                         StringValue('port_name'): StringValue('to_class')})
                                                                           })
                                  })
                    )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Composition'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('c_i_a'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Composition')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Association')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.c_i_a'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Aggregation'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Aggregation'),
                                                                           StringValue('abstract'): BooleanValue(False),
                                                                           StringValue('potency'): InfiniteValue('+'),
                                                                           StringValue('class'): LocationValue('mvk.object.Aggregation'),
                                                                           StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                           StringValue('lower'): IntegerValue(0),
                                                                                                                           StringValue('upper'): InfiniteValue('+'),
                                                                                                                           StringValue('port_name'): StringValue('from_class')}),
                                                                           StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                         StringValue('lower'): IntegerValue(0),
                                                                                                                         StringValue('upper'): InfiniteValue('+'),
                                                                                                                         StringValue('port_name'): StringValue('to_class')})
                                                                           })
                                  })
                    )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Composition'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('a_i_a'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Aggregation')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Association')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.a_i_a'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                  CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Inheritance'),
                                                                           StringValue('abstract'): BooleanValue(False),
                                                                           StringValue('potency'): IntegerValue(1),
                                                                           StringValue('class'): LocationValue('mvk.object.Association'),
                                                                           StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                           StringValue('lower'): IntegerValue(0),
                                                                                                                           StringValue('upper'): InfiniteValue('+'),
                                                                                                                           StringValue('port_name'): StringValue('from_class')}),
                                                                           StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                         StringValue('lower'): IntegerValue(0),
                                                                                                                         StringValue('upper'): InfiniteValue('+'),
                                                                                                                         StringValue('port_name'): StringValue('to_class')})
                                                                           })
                                  })
                    )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Inheritance'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.Inheritance'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})}))
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.Inheritance.name'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('a_i_c'),
                                                                                StringValue('class'): LocationValue('mvk.object.Inherits'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Association')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.a_i_c'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('attributes'),
                                                                                StringValue('abstract'): BooleanValue(False),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Association'),
                                                                                StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Clabject'),
                                                                                                                                StringValue('lower'): IntegerValue(1),
                                                                                                                                StringValue('upper'): IntegerValue(1),
                                                                                                                                StringValue('port_name'): StringValue('from_class')}),
                                                                                StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('protected.formalisms.MultiDiagrams.Attribute'),
                                                                                                                              StringValue('lower'): IntegerValue(0),
                                                                                                                              StringValue('upper'): InfiniteValue('+'),
                                                                                                                              StringValue('port_name'): StringValue('to_attr')})
                                                                                })
                                       })
                         )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.attributes'))
    assert rl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MultiDiagrams.attributes'),
                                       CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('name'),
                                                                                StringValue('type'): StringType(),
                                                                                StringValue('default'): StringValue(''),
                                                                                StringValue('potency'): IntegerValue(1),
                                                                                StringValue('lower'): IntegerValue(1),
                                                                                StringValue('upper'): IntegerValue(1),
                                                                                StringValue('class'): LocationValue('mvk.object.Attribute')})
                                  })
                    )
    rl = mvkinst.read(LocationValue('protected.formalisms.MultiDiagrams.attributes.name'))
    assert rl.is_success()

    ''' Temporary TestComposition formalism. '''

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestComposition')})
                                       })
                         )
    assert cl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Parent'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                StringValue('Class.id_field'): StringValue('Parent.name')})
                                       })
                         )
    assert cl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition.Parent'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                StringValue('Attribute.type'): StringType(),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                      })
                         )
    assert cl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Child'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                StringValue('Class.id_field'): StringValue('Child.name')})
                                       })
                         )

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition.Child'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                StringValue('Attribute.type'): StringType(),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                      })
                         )
    assert cl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Composition'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('children'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('children.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(1),
                                                                               StringValue('Association.from_max'): IntegerValue(1),
                                                                               StringValue('Association.from_port'): StringValue('from_parent'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_child'),
                                                                               StringValue('from_class'): LocationValue('formalisms.TestComposition.Parent'),
                                                                               StringValue('to_class'): LocationValue('formalisms.TestComposition.Child')})
                                  })
                    )
    assert cl.is_success()

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition.children'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                StringValue('Attribute.type'): StringType(),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                      })
                         )
    assert cl.is_success()

    '''Tranf. step model. Similar to AtomPM at the moment. Maris'''

    '''MT container model or package'''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MT')})
                                       })
                         )
    '''End MT container model'''
    
    '''Abstract class Step'''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Step'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                StringValue('Class.id_field'): StringValue('Step.id')})
                                       })
                         )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Step'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                StringValue('Attribute.type'): StringType(),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                      })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Step'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                StringValue('Attribute.type'): StringType(),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                      })
                         )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Step'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('isStart'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('BooleanType'),
                                                                                StringValue('Attribute.default'): BooleanValue(False)})
                                      })
                         )
    
    '''End abstract class Step'''
    
    '''MTRule class'''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Rule'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True)})
                                       })
                         )


    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('location'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('LocationType'),
                                                                                StringValue('Attribute.default'): LocationValue('')})
                                       })
                         )

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('first_match'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('BooleanType'),
                                                                                StringValue('Attribute.default'): BooleanValue(True)})
                                       })
                         )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('rule_i_step'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.MT.Rule'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.MT.Step')})
                                      })
                        )
    
    '''ARule apply rewrite to one match'''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('ARule'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False)})
                                       })
                         )
    

    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('arule_i_rule'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.MT.ARule'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.MT.Rule')})
                                      })
                        )
    '''end arule'''
    
    '''End mtrule class'''
    
    '''MTTransf class'''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transformation'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False)})
                                       })
                         )
#     '''name attribute'''
#     cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#                                        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Transformation'),
#                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
#                                                                                 StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
#                                                                                 StringValue('Attribute.default'): StringValue('')})
#                                       })
#                          )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Transformation'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('location'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('LocationType'),
                                                                                StringValue('Attribute.default'): LocationValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('transf_i_step'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.MT.Transformation'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.MT.Step')})
                                      })
                        )
    '''End mttrans class'''
    
    '''Control flow Associations'''
    
    '''@TODO cardinalities check''' 
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Flow'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(True),
                                                                               StringValue('Class.id_field'): StringValue('Flow.id'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_step'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_step'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.MT.Step'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.MT.Step')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Flow'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                      })
                         )
    '''Number of time transfrormation flow can follow this path. -1 inifinite, 0 none etc. Number will be decremented by transformation.'''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.Flow'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('exec_num'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                StringValue('Attribute.default'): IntegerValue(-1)})
                                      })
                         )
    '''Subclasses of control flow association'''
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('OnSuccess'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_step'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_step'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.MT.Step'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.MT.Step')})
                                  })
                    )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('OnFailure'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_step'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_step'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.MT.Step'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.MT.Step')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('OnNotApplicable'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_step'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_step'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.MT.Step'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.MT.Step')})
                                  })
                    )
    
    
#     cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
#                                        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
#                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('OnSuccess'),
#                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
#                                        })
#                          )
#     cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
#                                        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
#                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('OnFailure'),
#                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
#                                        })
#                          )
#     cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
#                                        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
#                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('OnNotApplicable'),
#                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
#                                        })
#                          )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('succ_i_flow'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.MT.OnSuccess'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.MT.Flow')})
                                      })
                        )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('fail_i_flow'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.MT.OnFailure'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.MT.Flow')})
                                      })
                        )
    
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('noappl_i_flow'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.MT.OnNotApplicable'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.MT.Flow')})
                                      })
                        )
    
    '''end control flow associations'''
    
    '''End Tranf. step model. Maris'''
    
    
    ''' rule type model '''
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Rule')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Pattern'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                StringValue('Class.id_field'): StringValue('MTpre_Pattern.pattern_name')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MTpre_Pattern'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('pattern_name'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MTpre_Pattern'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MT_constraint'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('True')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Pattern'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                StringValue('Class.id_field'): StringValue('MTpost_Pattern.pattern_name')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MTpost_Pattern'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('pattern_name'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MTpost_Pattern'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MT_action'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('pass')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MT_Element'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                StringValue('Class.id_field'): StringValue('MT_Element.id')}),
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MT_Element'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MT_label'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MT_Element'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Element'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True)})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('pre_i_el'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpre_Element'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MT_Element')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Element'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(True)})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('post_i_el'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpost_Element'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MT_Element')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MT_Association'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(True),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_el'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_el'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.Rule.MT_Element'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.Rule.MT_Element')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('assoc_i_el'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.MT_Association'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MT_Element')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Association'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(True),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_el'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_el'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpre_Element'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('pre_i_assoc'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpre_Association'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MT_Association')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Association'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(True),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_el'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_el'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpost_Element'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('post_i_assoc'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpost_Association'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MT_Association')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Contents'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('MTpre_Contents.id'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_pattern'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_el'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpre_Pattern'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                      CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Contents'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('MTpost_Contents.id'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_pattern'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_el'),
                                                                               StringValue('from_class'): LocationValue('protected.formalisms.Rule.MTpost_Pattern'),
                                                                               StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                  })
                    )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule.MTpost_Contents'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                StringValue('Attribute.default'): StringValue('')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('NAC'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False)})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('nac_i_pattern'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.NAC'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Pattern')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('LHS'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False)})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('lhs_i_pattern'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.LHS'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Pattern')})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('RHS'),
                                                                                StringValue('Class.is_abstract'): BooleanValue(False)})
                                       })
                         )
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                       CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.Rule'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('rhs_i_pattern'),
                                                                                StringValue('from_class'): LocationValue('protected.formalisms.Rule.RHS'),
                                                                                StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Pattern')})
                                       })
                         )
    
    
    ###########################
    cl = mvkinst.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
            CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT'),
            CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TCore')})
        }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Iter')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Iter'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('maxIterations'),
        StringValue('Attribute.type'): IntegerType(),
        StringValue('Attribute.default'): IntegerValue(1)})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Iter'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('Random'),
        StringValue('Attribute.type'): BooleanType(),
        StringValue('Attribute.default'): BooleanValue(False)})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Iter'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('rule'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue("")})
    }))
    
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('MatchSet'),
        StringValue('Class.id_field'): StringValue('Match.name')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.MatchSet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue('')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.MatchSet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('matches'),
        StringValue('Attribute.type'): MappingType(),
        StringValue('Attribute.default'): AnyValue()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.MatchSet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('match2rewrite'),
        StringValue('Attribute.type'): AnyType(),
        StringValue('Attribute.default'): AnyValue()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Packet')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('model'),
        StringValue('Attribute.type'): LocationType()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('msg'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue('')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('rule'),
        StringValue('Attribute.type'): LocationType()})
    }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Attribute.name'): StringValue('currentRule'),
#         StringValue('Attribute.type'): LocationType()})
#     }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('current'),
        StringValue('Attribute.type'): LocationType()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('isSuccess'),
        StringValue('Attribute.type'): BooleanType(),
        StringValue('Attribute.default'): BooleanValue(False)})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Packet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('matchsets'),
        StringValue('Attribute.type'): MappingType(),
        StringValue('Attribute.default'): AnyValue()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Rewriter')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Rewriter'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('rule'),
        StringValue('Attribute.type'): LocationType()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Match'),
        StringValue('Class.id_field'): StringValue('Match.name')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Match'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue('')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Match'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('mapping'),
        StringValue('Attribute.type'): MappingType(),
        StringValue('Attribute.default'): AnyValue()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(True),
        StringValue('Class.name'): StringValue('Primitive'),
        StringValue('Class.id_field'): StringValue('Primitive.name')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Primitive'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('isSuccess'),
        StringValue('Attribute.type'): BooleanType(),
        StringValue('Attribute.default'): BooleanValue(False)})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Primitive'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue('')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Matcher')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Matcher'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('max'),
        StringValue('Attribute.type'): IntegerType(),
        StringValue('Attribute.default'): IntegerValue(1)})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Matcher'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('rule'),
        StringValue('Attribute.type'): LocationType()})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(True),
        StringValue('Class.name'): StringValue('RulePrimitive')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(True),
        StringValue('Class.name'): StringValue('Message'),
        StringValue('Class.id_field'): StringValue('Message.name')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Message'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue('')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Inheritance.name'): StringValue('r_i_rp'),
        StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Rewriter'),
        StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.RulePrimitive')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Inheritance.name'): StringValue('p_i_rp'),
        StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.RulePrimitive'),
        StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.Primitive')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Inheritance.name'): StringValue('m_i_rp'),
        StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Matcher'),
        StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.RulePrimitive')})
    }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Inheritance.name'): StringValue('p_i_m'),
        StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Packet'),
        StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.Message')})
    }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Association.to_max'): InfiniteValue('+'),
#         StringValue('Association.from_max'): IntegerValue(1),
#         StringValue('Association.from_port'): StringValue('from_packet'),
#         StringValue('Association.to_min'): IntegerValue(0),
#         StringValue('Class.name'): StringValue('Matchset'),
#         StringValue('Association.to_port'): StringValue('to_match'),
#         StringValue('Class.is_abstract'): BooleanValue(False),
#         StringValue('Association.from_min'): IntegerValue(0),
#         StringValue('Class.id_field'): StringValue('Matchset.name'),
#         StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Packet'),
#         StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.Match')})
#     }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Association.to_max'): IntegerValue(1),
#         StringValue('Association.from_max'): IntegerValue(1),
#         StringValue('Association.from_port'): StringValue('from_packet'),
#         StringValue('Association.to_min'): IntegerValue(0),
#         StringValue('Class.name'): StringValue('Match2Rewrite'),
#         StringValue('Association.to_port'): StringValue('to_match'),
#         StringValue('Class.is_abstract'): BooleanValue(False),
#         StringValue('Association.from_min'): IntegerValue(0),
#         StringValue('Class.id_field'): StringValue('Match2Rewrite.name'),
#         StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Packet'),
#         StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.Match')})
#     }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Matchset'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Attribute.name'): StringValue('rule'),
#         StringValue('Attribute.type'): LocationType(),
#         StringValue('Attribute.default'): LocationValue('')})
#     }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Matchset'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Attribute.name'): StringValue('name'),
#         StringValue('Attribute.type'): StringType(),
#         StringValue('Attribute.default'): StringValue('')})
#     }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Match2Rewrite'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Attribute.name'): StringValue('name'),
#         StringValue('Attribute.type'): StringType(),
#         StringValue('Attribute.default'): StringValue('')})
#     }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.Match2Rewrite'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Attribute.name'): StringValue('rule'),
#         StringValue('Attribute.type'): LocationType(),
#         StringValue('Attribute.default'): LocationValue('')})
#     }))
    cl = mvkinst.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
        CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Inheritance.name'): StringValue('i_i_rp'),
        StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Iter'),
        StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.RulePrimitive')})
    }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Association.to_max'): IntegerValue(1),
#         StringValue('Association.from_max'): IntegerValue(1),
#         StringValue('Association.from_port'): StringValue('from_match'),
#         StringValue('Association.to_min'): IntegerValue(0),
#         StringValue('Class.name'): StringValue('NextMatch'),
#         StringValue('Association.to_port'): StringValue('to_match'),
#         StringValue('Class.is_abstract'): BooleanValue(False),
#         StringValue('Association.from_min'): IntegerValue(0),
#         StringValue('Class.id_field'): StringValue('NextMatch.id'),
#         StringValue('from_class'): LocationValue('protected.formalisms.MT.TCore.Match'),
#         StringValue('to_class'): LocationValue('protected.formalisms.MT.TCore.Match')})
#     }))
#     cl = mvkinst.create(MappingValue({
#         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
#         CreateConstants.LOCATION_KEY: LocationValue('protected.formalisms.MT.TCore.NextMatch'),
#         CreateConstants.ATTRS_KEY: MappingValue({
#         StringValue('Attribute.name'): StringValue('id'),
#         StringValue('Attribute.type'): IntegerType()})
#     }))

    mvkinst.backup(StringValue("protected"))
