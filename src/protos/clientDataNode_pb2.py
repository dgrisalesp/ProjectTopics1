# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: clientDataNode.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'clientDataNode.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x63lientDataNode.proto\x12\x0e\x63lientDataNode\"R\n\ruploadRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0f\n\x07node_id\x18\x04 \x01(\t\"1\n\x0euploadResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t\"\x1e\n\ngetRequest\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\"<\n\x0bgetResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x10\n\x08response\x18\x03 \x01(\t\"E\n\x12sendReplicaRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x0f\n\x07node_id\x18\x03 \x01(\t\"6\n\x13sendReplicaResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t2\xf9\x01\n\x0e\x43lientDataNode\x12K\n\nuploadFile\x12\x1d.clientDataNode.uploadRequest\x1a\x1e.clientDataNode.uploadResponse\x12\x42\n\x07getFile\x12\x1a.clientDataNode.getRequest\x1a\x1b.clientDataNode.getResponse\x12V\n\x0bsendReplica\x12\".clientDataNode.sendReplicaRequest\x1a#.clientDataNode.sendReplicaResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'clientDataNode_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_UPLOADREQUEST']._serialized_start=40
  _globals['_UPLOADREQUEST']._serialized_end=122
  _globals['_UPLOADRESPONSE']._serialized_start=124
  _globals['_UPLOADRESPONSE']._serialized_end=173
  _globals['_GETREQUEST']._serialized_start=175
  _globals['_GETREQUEST']._serialized_end=205
  _globals['_GETRESPONSE']._serialized_start=207
  _globals['_GETRESPONSE']._serialized_end=267
  _globals['_SENDREPLICAREQUEST']._serialized_start=269
  _globals['_SENDREPLICAREQUEST']._serialized_end=338
  _globals['_SENDREPLICARESPONSE']._serialized_start=340
  _globals['_SENDREPLICARESPONSE']._serialized_end=394
  _globals['_CLIENTDATANODE']._serialized_start=397
  _globals['_CLIENTDATANODE']._serialized_end=646
# @@protoc_insertion_point(module_scope)
