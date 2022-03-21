# This is the code that defines the Parameters, Inputs and Outputs of the Node. Most of the code should not be
# changed. The only parts that should be changed are the information in the lists of the properties of the Node and the
# name of the xxx_com variable under the if __name__ == "__main__": clause


# <editor-fold desc="The following 9 lines of code are required to allow Heron to be able to see the Operation without
# package installation. Do not change.">
import os
import sys
from os import path

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))

from Heron import general_utils as gu

Exec = os.path.realpath(__file__)
# </editor-fold>


# <editor-fold desc="The following code is called from the GUI process as part of the generation of the node.
# It is meant to create Node specific elements.
# This is where a new Node's individual elements should be defined">

"""
Properties of the generated Node
"""
BaseName = 'Snake PyGame'  # The base name can have spaces.

NodeAttributeNames = ['Parameters', 'Angle In']  # The names of all the inputs to the Node.
# If the Node has any parameters then the first name has to be Parameters. This is neither an input or an output but
# provides space on the Node to show parameter widgets.

NodeAttributeType = ['Static', 'Input']  # Whether the above names are outputs or inputs. A Sink can only have
# Inputs. Sinks allow multiple inputs. If the first attribute name is Parameters then the first attribute type must be
# Static (i.e. neither an Output nor and Input).

ParameterNames = ['Speed']  # If there are
# parameters then write their names here. If there are not make an empty list (i.e. ParameterNames = [])

ParameterTypes = ['float']  # The types of the parameters (in string form).
# types allowed are: 'bool', 'str', 'list', 'int' and 'float'. Again for no parameters make an empty list.

ParametersDefaultValues = [10.0]  # The default values of each parameter.  These are the values the Node will
# have when first created into the Node Editor. Parameter of 'list' type become drop down menus and the list of their
# default values becomes the drop down menu items. The Node by default uses the first item (so the order matters).

# The following line needs to exist with the correct name for the xxx_worker.py script
WorkerDefaultExecutable = os.path.join(os.path.dirname(Exec), 'snake_pygame_worker.py')
# </editor-fold>


# <editor-fold desc="The following code is called as its own process when the editor starts the graph.
#  You can refactor the name of the xxx_com variable but do not change anything else">
if __name__ == "__main__":
    #  In this case refactor the name sink_template_com to whatever_com
    snake_pygame_com = gu.start_the_sink_communications_process()
    gu.register_exit_signals(snake_pygame_com.on_kill)
    snake_pygame_com.start_ioloop()
# </editor-fold>
