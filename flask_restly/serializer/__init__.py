from flask import jsonify, Flask

try:
    from google.protobuf.reflection import GeneratedProtocolMessageType
except ImportError:
    pass


def json(response, _):
    return jsonify(response)


def protobuf(response, outgoing):
    assert isinstance(outgoing, GeneratedProtocolMessageType) is True

    outgoing = _dict_to_protobuf(response, outgoing)

    return Flask.response_class(
        outgoing.SerializeToString(),
        mimetype="application/x-protobuf"
    )


def _dict_to_protobuf(dictionary, outgoing):
    assert outgoing is not None
    assert isinstance(dictionary, dict)

    instance = outgoing()

    for key, value in dictionary.items():
        if value is None:
            continue

        if isinstance(value, dict):
            attribute = getattr(instance, key)
            _dict_to_protobuf(attribute, value)

        elif hasattr(value, "__iter__"):
            attribute = getattr(instance, key)
            if len(value) == 0 or not isinstance(value[0], dict):
                attribute.extend(value)
            else:
                for item in value:
                    _dict_to_protobuf(attribute.add(), item)
        else:
            setattr(instance, key, value)

    return instance
