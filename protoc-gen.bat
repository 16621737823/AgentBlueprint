set py_out_path=core/message
set proto_path=proto_message
set src_path=proto_message
python -m grpc_tools.protoc -I%proto_path% --python_out=%py_out_path% --pyi_out=%py_out_path%  %src_path%/*.proto