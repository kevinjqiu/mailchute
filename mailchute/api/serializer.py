class ResponseDTO(dict):
    def __init__(self, root_name, value):
        super(ResponseDTO, self).__init__({
            root_name: value
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
