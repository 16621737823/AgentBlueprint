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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x41PMFactory.proto\x12\x05proto\"\x8e\x01\n\rNodeConnector\x12\x39\n\x0binput_nodes\x18\x01 \x03(\x0b\x32$.proto.NodeConnector.InputNodesEntry\x1a\x42\n\x0fInputNodesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0f.proto.NodeData:\x02\x38\x01\"\xa8\x01\n\x08NodeData\x12\x0f\n\x07node_id\x18\x01 \x01(\x04\x12\x32\n\x0e\x66unction_param\x18\x02 \x01(\x0b\x32\x15.proto.FunctionParamsH\x00\x88\x01\x01\x12\x31\n\x0enode_structure\x18\x03 \x01(\x0b\x32\x14.proto.NodeConnectorH\x01\x88\x01\x01\x42\x11\n\x0f_function_paramB\x11\n\x0f_node_structure\"U\n\x08\x46ileTree\x12\x11\n\ttree_type\x18\x01 \x01(\x05\x12\"\n\troot_node\x18\x02 \x01(\x0b\x32\x0f.proto.NodeData\x12\x12\n\nis_default\x18\x03 \x01(\x08\"O\n\x07\x61pmFile\x12\x1e\n\x05trees\x18\x01 \x03(\x0b\x32\x0f.proto.FileTree\x12\x0e\n\x06usr_id\x18\x02 \x01(\x05\x12\x14\n\x0c\x63haracter_id\x18\x03 \x01(\x05\"\xc8\x01\n\x0e\x46unctionParams\x12\x1c\n\x0f\x66unction_prompt\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x1b\n\x0einput_data_obj\x18\x02 \x01(\x0cH\x01\x88\x01\x01\x12\x17\n\ninput_text\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x1a\n\rsystem_prompt\x18\x04 \x01(\tH\x03\x88\x01\x01\x42\x12\n\x10_function_promptB\x11\n\x0f_input_data_objB\r\n\x0b_input_textB\x10\n\x0e_system_promptb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'APMFactory_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NODECONNECTOR_INPUTNODESENTRY']._loaded_options = None
  _globals['_NODECONNECTOR_INPUTNODESENTRY']._serialized_options = b'8\001'
  _globals['_NODECONNECTOR']._serialized_start=28
  _globals['_NODECONNECTOR']._serialized_end=170
  _globals['_NODECONNECTOR_INPUTNODESENTRY']._serialized_start=104
  _globals['_NODECONNECTOR_INPUTNODESENTRY']._serialized_end=170
  _globals['_NODEDATA']._serialized_start=173
  _globals['_NODEDATA']._serialized_end=341
  _globals['_FILETREE']._serialized_start=343
  _globals['_FILETREE']._serialized_end=428
  _globals['_APMFILE']._serialized_start=430
  _globals['_APMFILE']._serialized_end=509
  _globals['_FUNCTIONPARAMS']._serialized_start=512
  _globals['_FUNCTIONPARAMS']._serialized_end=712
# @@protoc_insertion_point(module_scope)