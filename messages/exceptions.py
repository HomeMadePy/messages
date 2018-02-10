"""Custom Exceptions Module."""

import messages


class MessageInputError(ValueError):
    """Exception for invalid inputs in message classes."""

    def __init__(self, msg_type, attr, input_type):
        self.err = 'Invalid input for specified message class: ' + msg_type
        self.err += '\n\t* argument: "{}"'.format(attr)
        self.err += '\n\t* input type must be: {}'.format(input_type)

        super(MessageInputError, self).__init__(self.err)


class MessageTypeError(TypeError):
    """Exception for declaring unsupported message types."""

    def __init__(self, msg_type):
        self.err = 'Invalid message type: ' + msg_type
        self.err += '\n\t* Support Message Types: '
        self.err += str(messages.MESSAGES)

        super(MessageTypeError, self).__init__(self.err)
