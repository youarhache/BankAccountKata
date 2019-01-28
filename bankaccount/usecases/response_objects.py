class ResponseSuccess:
    SUCCESS = 'Success'
    
    def __init__(self, value = None):
        self.value = value
        self.type = self.SUCCESS

    def __bool__(self):
        return True


class ResponseFailure:
    def __init__(self, resp_type, resp_msg):
        self.type = resp_type
        self.message = self._format_msg(resp_msg)
        self.value = {'type': self.type, 'message': self.message}
    
    def _format_msg(self, msg):
        if isinstance(msg, Exception):
            return f"{msg.__class__.__name__} : {msg}"
        return msg

    # @property
    # def value(self):
    #     return {'type': self.type, 'message': self.message}

    #error types enum
    PARAMETERS_ERROR = 'ParametersError'
    RESOURCE_ERROR = 'ResourceError'
    SYSTEM_ERROR = 'SystemError'

    @classmethod
    def build_resource_error(cls, message=None):
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message=None):
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message=None):
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def from_invalid_request(cls, invalid_request):
        msg = '\n'.join([f"{e['parameter']} : {e['message']}" for e in invalid_request.errors])
        return cls.build_parameters_error(msg)

    def __bool__(self):
        return False