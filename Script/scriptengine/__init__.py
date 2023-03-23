from .dotNETs import *
from .ScriptApplication import *
from .ScriptDeviceDescription import *
from .ScriptDeviceObject import *
from .ScriptDeviceParameters import *
from .ScriptDeviceRepository import *
from .ScriptDeviceUserManagement import *
from .ScriptDriverInfo import *
from .ScriptExplicitConnectorObjects import *
from .ScriptExternalFileObject import *
from .ScriptIecLanguageObjectContainer import *
from .ScriptLibManObject import *
from .ScriptLiveDeviceUserManagement import *
from .ScriptObject import *
from .ScriptOnline import *
from .ScriptProject import *
from .ScriptProjects import *
from .ScriptSystem import *
from .ScriptTaskConfigObject import *
from .ScriptTextualObject import *
from .ScriptTreeObject import *
from .ScriptUserManagement import *

## create instances for intellisense/code completion
device_repository = ScriptDeviceRepository()    # type: ScriptDeviceRepository
library_manager = LibManager()                  # type: LibManager
online = ScriptOnline()                         # type: ScriptOnline
projects = ScriptProjects()                     # type: ScriptProjects
system = System()                               # type: System


## Modules extending the ScriptEngine:


#
# Module ""CODESYS Visualization Support""
#
from .ScriptImagePoolObject import *
from .ScriptTextListObject import *


#
# Module ""CODESYS Application Composer""
#
from .ScriptApplicationComposer import *
modulerepository = ScriptModuleRepository()     # type: ScriptModuleRepository


#
# Module ""
#
from .ScriptApplicationComposer import *
modulerepository = ScriptModuleRepository()     # type: ScriptModuleRepository

