from flask import jsonify, current_app

try:
    from google.protobuf.internal.containers import BaseContainer
    from google.protobuf.reflection import GeneratedProtocolMessageType
    from google.protobuf.message import Message as ProtocolMessage
except ImportError:
    pass


class SerializerBase:
    def serialize(self, response, outgoing):
        raise NotImplementedError()

    def deserialize(self, request, incoming):
        raise NotImplementedError()


class JsonSerializer(SerializerBase):
    def serialize(self, response, _):
        return jsonify(response)

    def deserialize(self, request, _):
        return request.get_json()


class ProtobufSerializer(SerializerBase):
    def serialize(self, response, outgoing):
        assert isinstance(outgoing, GeneratedProtocolMessageType) is True

        outgoing = _dict_to_protobuf(response, outgoing)

        return current_app.response_class(
            outgoing.SerializeToString(),
            mimetype=current_app.config.get('RESTLY_PROTOBUF_MIMETYPE')
        )

    def deserialize(self, request, incoming):
        assert isinstance(incoming, GeneratedProtocolMessageType) is True

        incoming = incoming()

        data = request.get_data().strip().decode('unicode-escape')

        incoming.ParseFromString(data.encode('utf-8'))

        return _protobuf_to_dict(incoming)


json = JsonSerializer()
protobuf = ProtobufSerializer()


def _dict_to_protobuf(value, message):
    def _parse_list(values, message):
        if len(values) > 0 and isinstance(values[0], dict):
            for v in values:
                cmd = message.add()
                _parse_dict(v, cmd)
        else:
            message.extend(values)

    def _parse_dict(values, message):
        for k, v in values.items():
            if isinstance(v, dict):
                _parse_dict(v, getattr(message, k))
            elif isinstance(v, list):
                _parse_list(v, getattr(message, k))
            else:
                setattr(message, k, v)

        return message

    return _parse_dict(value, message())


def _protobuf_to_dict(instance):
    result = dict()

    for descriptor, value in instance.ListFields():
        if isinstance(value, ProtocolMessage):
            result[descriptor.name] = _protobuf_to_dict(value)
        elif isinstance(value, BaseContainer):
            result[descriptor.name] = []
            for item in value:
                if isinstance(item, ProtocolMessage):
                    dict_item = _protobuf_to_dict(item)
                    result[descriptor.name].append(dict_item)
                else:
                    result[descriptor.name].append(item)
        else:
            result[descriptor.name] = value

    return result
