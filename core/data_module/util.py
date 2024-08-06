def parse_func_index(index: int):
    return int(str(index)[:1]), int(str(index)[1:9])
def parse_data_index(index: int):
    node_type = int(str(index)[:2])
    node_index = int(str(index)[2:6])
    node_desc = int(str(index)[6:8])
    node_prop = int(str(index)[8:10])
    return node_type, node_index, node_desc, node_prop