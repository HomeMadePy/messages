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

    def __init__(self, msg_type, msg_types=None):
        self.err = 'Invalid message type: ' + msg_type
        if msg_types:
            self.err += '\n\t* Supported message types: '
            self.err += str(msg_types)
        super(UnsupportedMessageTypeError, self).__init__(self.err)


class UnknownProfileError(KeyError):
    """Exception for unknown config.json profile names."""

    def __init__(self, profile):
        self.err = 'Unknown Profile name: ' + profile
        super(UnknownProfileError, self).__init__(self.err)
