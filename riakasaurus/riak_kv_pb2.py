# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='riak_kv.proto',
  package='',
  serialized_pb='\n\rriak_kv.proto\x1a\nriak.proto\"\'\n\x12RpbGetClientIdResp\x12\x11\n\tclient_id\x18\x01 \x02(\x0c\"&\n\x11RpbSetClientIdReq\x12\x11\n\tclient_id\x18\x01 \x02(\x0c\"\xa4\x01\n\tRpbGetReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\t\n\x01r\x18\x03 \x01(\r\x12\n\n\x02pr\x18\x04 \x01(\r\x12\x14\n\x0c\x62\x61sic_quorum\x18\x05 \x01(\x08\x12\x13\n\x0bnotfound_ok\x18\x06 \x01(\x08\x12\x13\n\x0bif_modified\x18\x07 \x01(\x0c\x12\x0c\n\x04head\x18\x08 \x01(\x08\x12\x15\n\rdeletedvclock\x18\t \x01(\x08\"M\n\nRpbGetResp\x12\x1c\n\x07\x63ontent\x18\x01 \x03(\x0b\x32\x0b.RpbContent\x12\x0e\n\x06vclock\x18\x02 \x01(\x0c\x12\x11\n\tunchanged\x18\x03 \x01(\x08\"\xd3\x01\n\tRpbPutReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x0e\n\x06vclock\x18\x03 \x01(\x0c\x12\x1c\n\x07\x63ontent\x18\x04 \x02(\x0b\x32\x0b.RpbContent\x12\t\n\x01w\x18\x05 \x01(\r\x12\n\n\x02\x64w\x18\x06 \x01(\r\x12\x13\n\x0breturn_body\x18\x07 \x01(\x08\x12\n\n\x02pw\x18\x08 \x01(\r\x12\x17\n\x0fif_not_modified\x18\t \x01(\x08\x12\x15\n\rif_none_match\x18\n \x01(\x08\x12\x13\n\x0breturn_head\x18\x0b \x01(\x08\"G\n\nRpbPutResp\x12\x1c\n\x07\x63ontent\x18\x01 \x03(\x0b\x32\x0b.RpbContent\x12\x0e\n\x06vclock\x18\x02 \x01(\x0c\x12\x0b\n\x03key\x18\x03 \x01(\x0c\"~\n\tRpbDelReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\n\n\x02rw\x18\x03 \x01(\r\x12\x0e\n\x06vclock\x18\x04 \x01(\x0c\x12\t\n\x01r\x18\x05 \x01(\r\x12\t\n\x01w\x18\x06 \x01(\r\x12\n\n\x02pr\x18\x07 \x01(\r\x12\n\n\x02pw\x18\x08 \x01(\r\x12\n\n\x02\x64w\x18\t \x01(\r\"%\n\x12RpbListBucketsResp\x12\x0f\n\x07\x62uckets\x18\x01 \x03(\x0c\" \n\x0eRpbListKeysReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\"-\n\x0fRpbListKeysResp\x12\x0c\n\x04keys\x18\x01 \x03(\x0c\x12\x0c\n\x04\x64one\x18\x02 \x01(\x08\"!\n\x0fRpbGetBucketReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\"2\n\x10RpbGetBucketResp\x12\x1e\n\x05props\x18\x01 \x02(\x0b\x32\x0f.RpbBucketProps\"A\n\x0fRpbSetBucketReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\x12\x1e\n\x05props\x18\x02 \x02(\x0b\x32\x0f.RpbBucketProps\"5\n\x0cRpbMapRedReq\x12\x0f\n\x07request\x18\x01 \x02(\x0c\x12\x14\n\x0c\x63ontent_type\x18\x02 \x02(\x0c\">\n\rRpbMapRedResp\x12\r\n\x05phase\x18\x01 \x01(\r\x12\x10\n\x08response\x18\x02 \x01(\x0c\x12\x0c\n\x04\x64one\x18\x03 \x01(\x08\"\xb0\x01\n\x0bRpbIndexReq\x12\x0e\n\x06\x62ucket\x18\x01 \x02(\x0c\x12\r\n\x05index\x18\x02 \x02(\x0c\x12*\n\x05qtype\x18\x03 \x02(\x0e\x32\x1b.RpbIndexReq.IndexQueryType\x12\x0b\n\x03key\x18\x04 \x01(\x0c\x12\x11\n\trange_min\x18\x05 \x01(\x0c\x12\x11\n\trange_max\x18\x06 \x01(\x0c\"#\n\x0eIndexQueryType\x12\x06\n\x02\x65q\x10\x00\x12\t\n\x05range\x10\x01\"\x1c\n\x0cRpbIndexResp\x12\x0c\n\x04keys\x18\x01 \x03(\x0c\"\xf5\x01\n\nRpbContent\x12\r\n\x05value\x18\x01 \x02(\x0c\x12\x14\n\x0c\x63ontent_type\x18\x02 \x01(\x0c\x12\x0f\n\x07\x63harset\x18\x03 \x01(\x0c\x12\x18\n\x10\x63ontent_encoding\x18\x04 \x01(\x0c\x12\x0c\n\x04vtag\x18\x05 \x01(\x0c\x12\x17\n\x05links\x18\x06 \x03(\x0b\x32\x08.RpbLink\x12\x10\n\x08last_mod\x18\x07 \x01(\r\x12\x16\n\x0elast_mod_usecs\x18\x08 \x01(\r\x12\x1a\n\x08usermeta\x18\t \x03(\x0b\x32\x08.RpbPair\x12\x19\n\x07indexes\x18\n \x03(\x0b\x32\x08.RpbPair\x12\x0f\n\x07\x64\x65leted\x18\x0b \x01(\x08\"3\n\x07RpbLink\x12\x0e\n\x06\x62ucket\x18\x01 \x01(\x0c\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x0b\n\x03tag\x18\x03 \x01(\x0c\"3\n\x0eRpbBucketProps\x12\r\n\x05n_val\x18\x01 \x01(\r\x12\x12\n\nallow_mult\x18\x02 \x01(\x08\x42#\n\x17\x63om.basho.riak.protobufB\x08RiakKvPB')



_RPBINDEXREQ_INDEXQUERYTYPE = descriptor.EnumDescriptor(
  name='IndexQueryType',
  full_name='RpbIndexReq.IndexQueryType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='eq', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='range', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1306,
  serialized_end=1341,
)


_RPBGETCLIENTIDRESP = descriptor.Descriptor(
  name='RpbGetClientIdResp',
  full_name='RpbGetClientIdResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='client_id', full_name='RpbGetClientIdResp.client_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=29,
  serialized_end=68,
)


_RPBSETCLIENTIDREQ = descriptor.Descriptor(
  name='RpbSetClientIdReq',
  full_name='RpbSetClientIdReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='client_id', full_name='RpbSetClientIdReq.client_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=70,
  serialized_end=108,
)


_RPBGETREQ = descriptor.Descriptor(
  name='RpbGetReq',
  full_name='RpbGetReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbGetReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='RpbGetReq.key', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='r', full_name='RpbGetReq.r', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pr', full_name='RpbGetReq.pr', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='basic_quorum', full_name='RpbGetReq.basic_quorum', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='notfound_ok', full_name='RpbGetReq.notfound_ok', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='if_modified', full_name='RpbGetReq.if_modified', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='head', full_name='RpbGetReq.head', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='deletedvclock', full_name='RpbGetReq.deletedvclock', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=111,
  serialized_end=275,
)


_RPBGETRESP = descriptor.Descriptor(
  name='RpbGetResp',
  full_name='RpbGetResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='content', full_name='RpbGetResp.content', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vclock', full_name='RpbGetResp.vclock', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='unchanged', full_name='RpbGetResp.unchanged', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=277,
  serialized_end=354,
)


_RPBPUTREQ = descriptor.Descriptor(
  name='RpbPutReq',
  full_name='RpbPutReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbPutReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='RpbPutReq.key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vclock', full_name='RpbPutReq.vclock', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content', full_name='RpbPutReq.content', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='w', full_name='RpbPutReq.w', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dw', full_name='RpbPutReq.dw', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='return_body', full_name='RpbPutReq.return_body', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pw', full_name='RpbPutReq.pw', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='if_not_modified', full_name='RpbPutReq.if_not_modified', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='if_none_match', full_name='RpbPutReq.if_none_match', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='return_head', full_name='RpbPutReq.return_head', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=357,
  serialized_end=568,
)


_RPBPUTRESP = descriptor.Descriptor(
  name='RpbPutResp',
  full_name='RpbPutResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='content', full_name='RpbPutResp.content', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vclock', full_name='RpbPutResp.vclock', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='RpbPutResp.key', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=570,
  serialized_end=641,
)


_RPBDELREQ = descriptor.Descriptor(
  name='RpbDelReq',
  full_name='RpbDelReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbDelReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='RpbDelReq.key', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rw', full_name='RpbDelReq.rw', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vclock', full_name='RpbDelReq.vclock', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='r', full_name='RpbDelReq.r', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='w', full_name='RpbDelReq.w', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pr', full_name='RpbDelReq.pr', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pw', full_name='RpbDelReq.pw', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dw', full_name='RpbDelReq.dw', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=643,
  serialized_end=769,
)


_RPBLISTBUCKETSRESP = descriptor.Descriptor(
  name='RpbListBucketsResp',
  full_name='RpbListBucketsResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='buckets', full_name='RpbListBucketsResp.buckets', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=771,
  serialized_end=808,
)


_RPBLISTKEYSREQ = descriptor.Descriptor(
  name='RpbListKeysReq',
  full_name='RpbListKeysReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbListKeysReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=810,
  serialized_end=842,
)


_RPBLISTKEYSRESP = descriptor.Descriptor(
  name='RpbListKeysResp',
  full_name='RpbListKeysResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='keys', full_name='RpbListKeysResp.keys', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='done', full_name='RpbListKeysResp.done', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=844,
  serialized_end=889,
)


_RPBGETBUCKETREQ = descriptor.Descriptor(
  name='RpbGetBucketReq',
  full_name='RpbGetBucketReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbGetBucketReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=891,
  serialized_end=924,
)


_RPBGETBUCKETRESP = descriptor.Descriptor(
  name='RpbGetBucketResp',
  full_name='RpbGetBucketResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='props', full_name='RpbGetBucketResp.props', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=926,
  serialized_end=976,
)


_RPBSETBUCKETREQ = descriptor.Descriptor(
  name='RpbSetBucketReq',
  full_name='RpbSetBucketReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbSetBucketReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='props', full_name='RpbSetBucketReq.props', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=978,
  serialized_end=1043,
)


_RPBMAPREDREQ = descriptor.Descriptor(
  name='RpbMapRedReq',
  full_name='RpbMapRedReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='request', full_name='RpbMapRedReq.request', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content_type', full_name='RpbMapRedReq.content_type', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1045,
  serialized_end=1098,
)


_RPBMAPREDRESP = descriptor.Descriptor(
  name='RpbMapRedResp',
  full_name='RpbMapRedResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='phase', full_name='RpbMapRedResp.phase', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='response', full_name='RpbMapRedResp.response', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='done', full_name='RpbMapRedResp.done', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1100,
  serialized_end=1162,
)


_RPBINDEXREQ = descriptor.Descriptor(
  name='RpbIndexReq',
  full_name='RpbIndexReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbIndexReq.bucket', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='index', full_name='RpbIndexReq.index', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='qtype', full_name='RpbIndexReq.qtype', index=2,
      number=3, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='RpbIndexReq.key', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='range_min', full_name='RpbIndexReq.range_min', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='range_max', full_name='RpbIndexReq.range_max', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RPBINDEXREQ_INDEXQUERYTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1165,
  serialized_end=1341,
)


_RPBINDEXRESP = descriptor.Descriptor(
  name='RpbIndexResp',
  full_name='RpbIndexResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='keys', full_name='RpbIndexResp.keys', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1343,
  serialized_end=1371,
)


_RPBCONTENT = descriptor.Descriptor(
  name='RpbContent',
  full_name='RpbContent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='RpbContent.value', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content_type', full_name='RpbContent.content_type', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='charset', full_name='RpbContent.charset', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content_encoding', full_name='RpbContent.content_encoding', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vtag', full_name='RpbContent.vtag', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='links', full_name='RpbContent.links', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='last_mod', full_name='RpbContent.last_mod', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='last_mod_usecs', full_name='RpbContent.last_mod_usecs', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='usermeta', full_name='RpbContent.usermeta', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='indexes', full_name='RpbContent.indexes', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='deleted', full_name='RpbContent.deleted', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1374,
  serialized_end=1619,
)


_RPBLINK = descriptor.Descriptor(
  name='RpbLink',
  full_name='RpbLink',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='bucket', full_name='RpbLink.bucket', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='RpbLink.key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tag', full_name='RpbLink.tag', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1621,
  serialized_end=1672,
)


_RPBBUCKETPROPS = descriptor.Descriptor(
  name='RpbBucketProps',
  full_name='RpbBucketProps',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='n_val', full_name='RpbBucketProps.n_val', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='allow_mult', full_name='RpbBucketProps.allow_mult', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1674,
  serialized_end=1725,
)

import riak_pb2

_RPBGETRESP.fields_by_name['content'].message_type = _RPBCONTENT
_RPBPUTREQ.fields_by_name['content'].message_type = _RPBCONTENT
_RPBPUTRESP.fields_by_name['content'].message_type = _RPBCONTENT
_RPBGETBUCKETRESP.fields_by_name['props'].message_type = _RPBBUCKETPROPS
_RPBSETBUCKETREQ.fields_by_name['props'].message_type = _RPBBUCKETPROPS
_RPBINDEXREQ.fields_by_name['qtype'].enum_type = _RPBINDEXREQ_INDEXQUERYTYPE
_RPBINDEXREQ_INDEXQUERYTYPE.containing_type = _RPBINDEXREQ;
_RPBCONTENT.fields_by_name['links'].message_type = _RPBLINK
_RPBCONTENT.fields_by_name['usermeta'].message_type = riak_pb2._RPBPAIR
_RPBCONTENT.fields_by_name['indexes'].message_type = riak_pb2._RPBPAIR

class RpbGetClientIdResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBGETCLIENTIDRESP
  
  # @@protoc_insertion_point(class_scope:RpbGetClientIdResp)

class RpbSetClientIdReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBSETCLIENTIDREQ
  
  # @@protoc_insertion_point(class_scope:RpbSetClientIdReq)

class RpbGetReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBGETREQ
  
  # @@protoc_insertion_point(class_scope:RpbGetReq)

class RpbGetResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBGETRESP
  
  # @@protoc_insertion_point(class_scope:RpbGetResp)

class RpbPutReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBPUTREQ
  
  # @@protoc_insertion_point(class_scope:RpbPutReq)

class RpbPutResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBPUTRESP
  
  # @@protoc_insertion_point(class_scope:RpbPutResp)

class RpbDelReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBDELREQ
  
  # @@protoc_insertion_point(class_scope:RpbDelReq)

class RpbListBucketsResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBLISTBUCKETSRESP
  
  # @@protoc_insertion_point(class_scope:RpbListBucketsResp)

class RpbListKeysReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBLISTKEYSREQ
  
  # @@protoc_insertion_point(class_scope:RpbListKeysReq)

class RpbListKeysResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBLISTKEYSRESP
  
  # @@protoc_insertion_point(class_scope:RpbListKeysResp)

class RpbGetBucketReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBGETBUCKETREQ
  
  # @@protoc_insertion_point(class_scope:RpbGetBucketReq)

class RpbGetBucketResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBGETBUCKETRESP
  
  # @@protoc_insertion_point(class_scope:RpbGetBucketResp)

class RpbSetBucketReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBSETBUCKETREQ
  
  # @@protoc_insertion_point(class_scope:RpbSetBucketReq)

class RpbMapRedReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBMAPREDREQ
  
  # @@protoc_insertion_point(class_scope:RpbMapRedReq)

class RpbMapRedResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBMAPREDRESP
  
  # @@protoc_insertion_point(class_scope:RpbMapRedResp)

class RpbIndexReq(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBINDEXREQ
  
  # @@protoc_insertion_point(class_scope:RpbIndexReq)

class RpbIndexResp(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBINDEXRESP
  
  # @@protoc_insertion_point(class_scope:RpbIndexResp)

class RpbContent(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBCONTENT
  
  # @@protoc_insertion_point(class_scope:RpbContent)

class RpbLink(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBLINK
  
  # @@protoc_insertion_point(class_scope:RpbLink)

class RpbBucketProps(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RPBBUCKETPROPS
  
  # @@protoc_insertion_point(class_scope:RpbBucketProps)

# @@protoc_insertion_point(module_scope)