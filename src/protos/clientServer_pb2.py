# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: clientServer.proto
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
    'clientServer.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63lientServer.proto\x12\x0c\x63lientServer\"1\n\x0fregisterRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"3\n\x10registerResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t\"3\n\x11unregisterRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"5\n\x12unregisterResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t\".\n\x0cloginRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"0\n\rloginResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t\"/\n\rlogoutRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"1\n\x0elogoutResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t\"+\n\x0bstayRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"/\n\x0cstayResponse\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x10\n\x08response\x18\x02 \x01(\t2\xf8\x02\n\x0c\x43lientServer\x12I\n\x08register\x12\x1d.clientServer.registerRequest\x1a\x1e.clientServer.registerResponse\x12O\n\nunregister\x12\x1f.clientServer.unregisterRequest\x1a .clientServer.unregisterResponse\x12@\n\x05login\x12\x1a.clientServer.loginRequest\x1a\x1b.clientServer.loginResponse\x12\x43\n\x06logout\x12\x1b.clientServer.logoutRequest\x1a\x1c.clientServer.logoutResponse\x12\x45\n\x0cstayingAlive\x12\x19.clientServer.stayRequest\x1a\x1a.clientServer.stayResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'clientServer_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERREQUEST']._serialized_start=36
  _globals['_REGISTERREQUEST']._serialized_end=85
  _globals['_REGISTERRESPONSE']._serialized_start=87
  _globals['_REGISTERRESPONSE']._serialized_end=138
  _globals['_UNREGISTERREQUEST']._serialized_start=140
  _globals['_UNREGISTERREQUEST']._serialized_end=191
  _globals['_UNREGISTERRESPONSE']._serialized_start=193
  _globals['_UNREGISTERRESPONSE']._serialized_end=246
  _globals['_LOGINREQUEST']._serialized_start=248
  _globals['_LOGINREQUEST']._serialized_end=294
  _globals['_LOGINRESPONSE']._serialized_start=296
  _globals['_LOGINRESPONSE']._serialized_end=344
  _globals['_LOGOUTREQUEST']._serialized_start=346
  _globals['_LOGOUTREQUEST']._serialized_end=393
  _globals['_LOGOUTRESPONSE']._serialized_start=395
  _globals['_LOGOUTRESPONSE']._serialized_end=444
  _globals['_STAYREQUEST']._serialized_start=446
  _globals['_STAYREQUEST']._serialized_end=489
  _globals['_STAYRESPONSE']._serialized_start=491
  _globals['_STAYRESPONSE']._serialized_end=538
  _globals['_CLIENTSERVER']._serialized_start=541
  _globals['_CLIENTSERVER']._serialized_end=917
# @@protoc_insertion_point(module_scope)
