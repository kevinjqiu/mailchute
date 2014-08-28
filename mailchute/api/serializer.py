import functools


def response(root_key, dto_class):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            if not isinstance(result, (list, tuple)):
                result = [result]

            return ResponseDTO(
                root_key, list(map(dto_class, result)))
        return wrapper
    return decorator


class ResponseDTO(dict):
    def __init__(self, root_key, value):
        super(ResponseDTO, self).__init__({
            root_key: value
        })


class IncomingEmailDTO(dict):
    def __init__(self, model):
        super(IncomingEmailDTO, self).__init__(
            id=model.id,
            created_at=model.created_at.isoformat(),
            sender=model.sender,
            recipient=model.recipient,
            raw_message_id=model.raw_message_id,
            # TODO: add link to raw_message
        )


class RawMessageDTO(dict):
    def __init__(self, model):
        super(RawMessageDTO, self).__init__(
            id=model.raw_message_id,
            message=model.message,
        )
