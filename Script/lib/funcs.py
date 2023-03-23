#Codesys iron python / python 2.7
from __future__ import print_function
import os, subprocess
import dis
import inspect

def list_ExtractColumn(list = [], column = 0):
    # type: (list, int) -> list

    if not len(list) > 0:
        raise Exception('empty list given')
    
    return [item[column] for item in list]

def saveTxtFile(Path, name, str = "Auto generated text file", ext = ".txt"):
    # type: (str, str, str, str) -> str

    if Path == None or "":
        raise Exception("No path given")
    
    if not os.path.exists(Path):
        raise Exception("Given path doesn't exist")
    
    if name == None or "":
        raise Exception("No Name given")
    
    path = os.path.join(Path, name + ext)
    with open(path, 'w') as txt:
        txt.write(str)

    return path

def nameof(_):
    frame = inspect.currentframe().f_back
    return _nameof(frame.f_code, frame.f_lasti)


def _nameof(code, offset):
    instructions = list(dis.get_instructions(code))
    (current_instruction_index, current_instruction), = (
        (index, instruction)
        for index, instruction in enumerate(instructions)
        if instruction.offset == offset
    )
    assert current_instruction.opname in ("CALL_FUNCTION", "CALL_METHOD"), "Did you call nameof in a weird way?"
    name_instruction = instructions[current_instruction_index - 1]
    assert name_instruction.opname.startswith("LOAD_"), "Argument must be a variable or attribute"
    return name_instruction.argrepr