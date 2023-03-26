from scriptengine import *

#system Ui funcs
ui = system.ui                                                        # type: ScriptUI

# Primary project (project user is working in)
Project = projects.primary                                            # type: ScriptProject     

# ALL object containted in the primary object
ObjectsAll = Project.get_children(True)                               # type: list[ScriptObject]