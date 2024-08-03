from google.protobuf import descriptor_pb2, descriptor_pool, message_factory, any_pb2
from google.protobuf.json_format import ParseDict
import json

class GenericProtobuf:
    def __init__(self):
        self.pool = descriptor_pool.Default()
        self.factory = message_factory.MessageFactory()

    def create_message_type(self, type_url, fields):
        # Create a DescriptorProto for the message type
        type_name = type_url.split('.')[-1]

        # Check if the type is already existing in the pool
        try:
            self.pool.FindMessageTypeByName(type_name)
        except KeyError:
            pass
        else:
            return

        descriptor_proto = descriptor_pb2.DescriptorProto()
        descriptor_proto.name = type_name

        # Add key - value pairs as fields to the Descriptor
        for idx, (field_name, field_value) in enumerate(fields.items(), start=1):
            field_descriptor = descriptor_proto.field.add()
            field_descriptor.name = field_name
            field_descriptor.number = idx

            if isinstance(field_value, int):
                field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_INT32
            elif isinstance(field_value, float):
                field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT
            elif isinstance(field_value, bool):
                field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_BOOL
            elif isinstance(field_value, list):
                nested_type_name = f"{type_name}_{field_name}"
                self.create_message_type(nested_type_name, field_value[0])
                field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
                field_descriptor.type_name = f"{nested_type_name}"
                field_descriptor.label = descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
            elif isinstance(field_value, dict):
                nested_type_name = f"{type_name}_{field_name}"
                self.create_message_type(nested_type_name, field_value[0])
                field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
                field_descriptor.type_name = f"{nested_type_name}"

            else:
                field_descriptor.type = descriptor_pb2.FieldDescriptorProto.TYPE_STRING

        # Create a FileDescriptorProto for the new descriptor
        file_descriptor_proto = descriptor_pb2.FileDescriptorProto()
        file_descriptor_proto.name = f'{type_name}.proto'
        file_descriptor_proto.message_type.add().MergeFrom(descriptor_proto)

        # Add the file descriptor
        self.pool.Add(file_descriptor_proto)

    def get_message_class(self, type_name):
        message_descriptor = self.pool.FindMessageTypeByName(type_name.split('.')[-1])
        return self.factory.GetPrototype(message_descriptor)

    def create_any_message(self, msg_dict, type_url):
        type_name = type_url.split('/')[-1]

        self.create_message_type(type_name, msg_dict)

        message_class = self.get_message_class(type_name)

        message_instance = message_class()
        ParseDict(msg_dict, message_instance)

        msg_any = any_pb2.Any()
        msg_any.Pack(message_instance)
        msg_any.type_url = type_url

        return msg_any
