import bottle
import functools

from email.parser import Parser
from mailchute.api.exception import NotFound, BadRequest


CONTENT_TYPE = 'application/json'


def response(root_key, dto_class):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                bottle.response.content_type = CONTENT_TYPE
                result = fn(*args, **kwargs)
                if not isinstance(result, (list, tuple)):
                    result = [result]

                if dto_class is None:
                    return ''
                else:
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


class IncomingEmailDTO(dict):
    def __init__(self, model):
        super(IncomingEmailDTO, self).__init__(
            id=model.id,
            created_at=model.created_at.isoformat(),
            sender=model.sender,
            recipient=model.recipient,
            raw_message=model.raw_message_id,
            subject=model.subject,
        )


class RawMessageDTO(dict):
    def __init__(self, model):
        super(RawMessageDTO, self).__init__(
            id=model.raw_message_id,
            message=self.get_message_payload(model)
        )

    def get_message_payload(self, model):
        email = Parser().parsestr(model.message)
        if email.is_multipart():
            return email.get_payload()[0].get_payload()
        else:
            return email.get_payload()
