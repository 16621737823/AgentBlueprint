# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: APMFactory.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x41PMFactory.proto\x12\x05proto\"\x8b\x01\n\rNodeConnector\x12\x37\n\ninput_data\x18\x01 \x03(\x0b\x32#.proto.NodeConnector.InputDataEntry\x1a\x41\n\x0eInputDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0f.proto.DataNode:\x02\x38\x01\"\x90\x01\n\x08TaskNode\x12\x0f\n\x07node_id\x18\x01 \x01(\x04\x12,\n\x0enode_structure\x18\x02 \x01(\x0b\x32\x14.proto.NodeConnector\x12-\n\x0e\x66unction_param\x18\x03 \x01(\x0b\x32\x15.proto.FunctionParams\x12\x16\n\x0eoutput_data_id\x18\x04 \x01(\x04\"r\n\x08\x44\x61taNode\x12\x0f\n\x07\x64\x61ta_id\x18\x01 \x01(\x04\x12\x11\n\tsource_id\x18\x02 \x01(\r\x12\x14\n\x0cpackage_uuid\x18\x03 \x01(\t\x12,\n\x0enode_structure\x18\x04 \x01(\x0b\x32\x14.proto.NodeConnector\")\n\x07\x61pmFile\x12\x1e\n\x05nodes\x18\x01 \x03(\x0b\x32\x0f.proto.TaskNode\"<\n\x0e\x46unctionParams\x12\x13\n\x0buser_prompt\x18\x01 \x01(\t\x12\x15\n\rsystem_prompt\x18\x02 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'APMFactory_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NODECONNECTOR_INPUTDATAENTRY']._loaded_options = None
  _globals['_NODECONNECTOR_INPUTDATAENTRY']._serialized_options = b'8\001'
  _globals['_NODECONNECTOR']._serialized_start=28
  _globals['_NODECONNECTOR']._serialized_end=167
  _globals['_NODECONNECTOR_INPUTDATAENTRY']._serialized_start=102
  _globals['_NODECONNECTOR_INPUTDATAENTRY']._serialized_end=167
  _globals['_TASKNODE']._serialized_start=170
  _globals['_TASKNODE']._serialized_end=314
  _globals['_DATANODE']._serialized_start=316
  _globals['_DATANODE']._serialized_end=430
  _globals['_APMFILE']._serialized_start=432
  _globals['_APMFILE']._serialized_end=473
  _globals['_FUNCTIONPARAMS']._serialized_start=475
  _globals['_FUNCTIONPARAMS']._serialized_end=535
# @@protoc_insertion_point(module_scope)
