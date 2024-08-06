def parse_index(index: int):
    data_type = int(str(index)[:2])
    data_index = int(str(index)[2:6])
    data_desc = int(str(index)[6:8])
    data_prop = int(str(index)[8:10])
    return data_type, data_index, data_desc, data_prop