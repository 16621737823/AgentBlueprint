#!/bin/bash

cp -r ./DataConfig\[EDIT\ ME\]/*.yaml ./golang-client/config/
cp -r ./DataConfig\[EDIT\ ME\]/*.yaml ./python-server/config/

py_out_path=python-server
go_module=golang-client/message
go_out_path=golang-client/message/proto
proto_path=proto_message
src_path=proto_message/message/proto

protoc -I$proto_path --experimental_allow_proto3_optional --go_out=$go_out_path --go_opt=module=$go_module --go-grpc_out=$go_out_path --go-grpc_opt=module=$go_module $src_path/*.proto
python -m grpc_tools.protoc -I$proto_path --experimental_allow_proto3_optional --python_out=$py_out_path --pyi_out=$py_out_path --grpc_python_out=$py_out_path $src_path/*.proto

