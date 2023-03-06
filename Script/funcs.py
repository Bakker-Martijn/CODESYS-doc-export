def list_ExtractColumn(list = [], column = 0):
    # type: (list, int) -> list

    if not len(list) > 0:
        raise Exception('empty list given')
    
    return [item[column] for item in list]