import bottle
import functools
from mailchute.api.exception import NotFound, BadRequest


def response(root_key, dto_class):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
                if not isinstance(result, (list, tuple)):
                    result = [result]

                return ResponseDTO(
                    root_key, list(map(dto_class, result)))
            except NotFound:
                bottle.response.status = 404
                return {'error': {'message': 'Resource Not Found'}}
            except BadRequest as e:
                bottle.response.status = 400
                return {'error': {'message': str(e)}}


        return wrapper
    return decorator


class ResponseDTO(dict):
    def __init__(self, root_key, value):
        super(ResponseDTO, self).__init__({
            root_key: value
        })


class InboxDTO(dict):
    def __init__(self, model):
        super(InboxDTO, self).__init__(
            id=model.name,
            name=model.name,
            num_of_emails=len(model.emails),
            emails=list(map(IncomingEmailDTO, model.emails)),
        )


class IncomingEmailDTO(dict):
    def __init__(self, model):
        super(IncomingEmailDTO, self).__init__(
            id=model.id,
            created_at=model.created_at.isoformat(),
            sender=model.sender,
            recipient=model.recipient,
            raw_message_id=model.raw_message_id,
            subject=model.subject,
            # TODO: add link to raw_message
        )


class RawMessageDTO(dict):
    def __init__(self, model):
        super(RawMessageDTO, self).__init__(
            id=model.raw_message_id,
            message=model.message,
        )
