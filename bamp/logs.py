import logging


class ExceptionFilter(logging.Filter):
    def __init__(self, debug=None):
        self.debug = debug

    def filter(self, record):
        if self.debug:
            return True

        # clear exceptions when not in debug
        if record.levelname == 'ERROR' and record.exc_info:
            record.exc_info = None
        return True

LOGGING = {
    'version': 1,
    'filters': {
        'exc_filter': {
            '()': ExceptionFilter,
            'debug': False
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['exc_filter']
        }
    },
    'loggers': {
        'bamp': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
}
