import message.APMFactory_pb2 as apm

def write_test_apm():
    with open("test_apm.apm", "wb") as file:
        apm_file = apm.apmFile()
        test_data_1 = apm.DataNode(
            data_id=1110020001
        )
        test_data_2 = apm.DataNode(
            data_id=1110010000
        )
        test_data_3 = apm.DataNode(
            data_id=1210030000,
            node_structure=apm.NodeConnector(
                input_data={
                    1: test_data_1,
                    2: test_data_1,
                }
            )
        )
        task_node = apm.TaskNode(
            node_id=1,
            function_param=apm.FunctionParams(
                user_prompt="testing testing testing testing testing {1} testing testing testing testing testing {2} testing testing testing ",
                system_prompt="testing testing testing {4}testing testing testing testing {5} testing testing testing "
            ),
            node_structure=apm.NodeConnector(
                input_data={
                    1: test_data_1,
                    2: test_data_3,
                    3: test_data_2,
                    4: test_data_3,
                    5: test_data_2,
                }
            )
        )