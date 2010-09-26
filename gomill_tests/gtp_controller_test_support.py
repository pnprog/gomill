from cStringIO import StringIO

from gomill import gtp_controller

class Mock_gmp_channel(gtp_controller.Linebased_gtp_channel):
    """A Linebased_gtp_channel that simulates talking to a GMP engine."""
    def __init__(self):
        gtp_controller.Linebased_gtp_channel.__init__(self)
        self.closed = False
        self.bytes_sent = 0

    def send_command_line(self, command):
        pass

    def get_response_line(self):
        if self.closed:
            raise GtpTransportError("pipe is closed")
        raise StandardError("requested a full line; this will hang")

    def get_response_byte(self):
        if self.closed:
            raise GtpTransportError("pipe is closed")
        packet = "\x01\xa1\xa0\x80"
        result = packet[self.bytes_sent]
        self.bytes_sent += 1
        return result

    def close(self):
        self.closed = True

class Preprogrammed_gtp_channel(gtp_controller.Subprocess_gtp_channel):
    """A Linebased_gtp_channel with preprogrammed response stream.

    Instantiate with a string containing the complete response stream.

    This will send the contents of the response stream, irrespective of what
    commands are received.

    The command stream is available from get_command_stream().

    """
    def __init__(self, response):
        gtp_controller.Linebased_gtp_channel.__init__(self)
        self.command_pipe = StringIO()
        self.response_pipe = StringIO(response)
        #raise GtpChannelError(s)

    def close(self):
        self.command_pipe.close()
        self.response_pipe.close()
        #self.resource_usage = rusage
        #raise GtpTransportError("\n".join(errors))

    def get_command_stream(self):
        """Return the complete contents of the command stream sent so far."""
        return self.command_pipe.getvalue()


