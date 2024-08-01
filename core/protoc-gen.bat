set py_out_path=message
set proto_path=message
set src_path=message/proto
python -m grpc_tools.protoc -I%proto_path% --python_out=%py_out_path% --pyi_out=%py_out_path%  %src_path%/*.proto