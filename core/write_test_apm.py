import message.APMFactory_pb2 as apm
from util.test_util import get_version_uuid

package_uuid = get_version_uuid("test1")
def write_test_apm():
    with open("test_apm.apm", "wb") as file:
        apm_file = apm.apmFile()
        test_data_1 = apm.DataNode(
            data_id=1110010001,
            package_uuid=package_uuid
        )
        test_data_2 = apm.DataNode(
            data_id=1110010000,
            package_uuid=package_uuid
        )
        test_data_3 = apm.DataNode(
            data_id=1210030000,
            package_uuid=package_uuid,
            node_structure=apm.NodeConnector(
                input_data={
                    1: test_data_1,
                    2: test_data_1,
                }
            )
        )

        test_connect_data_1 = apm.DataNode(
            data_id=1110010200,
            package_uuid=package_uuid,
            source_id=1,
        )
        test_connect_data_2 = apm.DataNode(
            data_id=1210030200,
            package_uuid=package_uuid,
            source_id=2,
        )
        test_connect_data_3 = apm.DataNode(
            data_id=1210030000,
            package_uuid=package_uuid,
            node_structure=apm.NodeConnector(
                input_data={
                    1: test_connect_data_1,
                    2: test_connect_data_2,
                }
            )
        )
        task_node_1 = apm.TaskNode(
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
            ),
            output_data_id=1110010100,
            package_uuid=package_uuid,
        )
        task_node_2 = apm.TaskNode(
            node_id=2,
            function_param=apm.FunctionParams(
                user_prompt="testing testing testing testing testing {1} testing testing testing testing testing {2} testing testing testing ",
                system_prompt="testing testing testing {4}testing testing testing testing {5} testing testing testing "
            ),
            node_structure=apm.NodeConnector(
                input_data={
                    1: test_data_1,
                    2: test_connect_data_1,
                    3: test_data_2,
                    4: test_connect_data_1,
                    5: test_data_2,
                }
            ),
            output_data_id=1210030000,
            package_uuid=package_uuid,
        )
        task_node_3 = apm.TaskNode(
            node_id=3,
            function_param=apm.FunctionParams(
                user_prompt="testing testing testing testing testing {1} testing testing testing testing testing {2} testing testing testing ",
                system_prompt="testing testing testing {4}testing testing testing testing {5} testing testing testing "
            ),
            node_structure=apm.NodeConnector(
                input_data={
                    1: test_data_1,
                    2: test_connect_data_2,
                    3: test_data_2,
                    4: test_connect_data_3,
                    5: test_data_2,
                }
            ),
            output_data_id=1210030000,
            package_uuid=package_uuid,
        )
        apm_file.nodes.extend([task_node_1, task_node_2, task_node_3])
        file.write(apm_file.SerializeToString())


def read_test_apm():
    with open("test_apm.apm","rb") as file:
        data_read = file.read()
        apm_file = apm.apmFile()
        apm_file.ParseFromString(data_read)
    return apm_file