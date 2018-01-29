"""Custom Exceptions Module."""


class MessageInputError(ValueError, Exception):
    """Exeption for invalid inputs in message classes."""

    def __init__(self, msg_type, attr, input_type):
        self.err = 'Invalid input for specified message class: ' + msg_type
        self.err += '\n\targument: "{}"'.format(attr)
        self.err += '\n\tinput type must be: {}'.format(input_type)

        super(MessageInputError, self).__init__(self.err)
