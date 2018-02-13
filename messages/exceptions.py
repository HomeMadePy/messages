"""Custom Exceptions Module."""


class InvalidMessageInputError(ValueError):
    """Exception for invalid inputs in message classes."""

    def __init__(self, msg_type, attr, input_type):
        self.err = 'Invalid input for specified message class: ' + msg_type
        self.err += '\n\t* argument: "{}"'.format(attr)
        self.err += '\n\t* input type must be: {}'.format(input_type)
        super(InvalidMessageInputError, self).__init__(self.err)


class UnsupportedMessageTypeError(TypeError):
    """Exception for declaring unsupported message types."""

    def __init__(self, msg_type):
        self.err = 'Invalid message type: ' + msg_type
        super(UnsupportedMessageTypeError, self).__init__(self.err)
