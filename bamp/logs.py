import logging


class DebugFilter(logging.Filter):
    def __init__(self, debug=None):
        self.debug = debug

    def filter(self, record):
        if self.debug:
            return True
        return False


LOGGING = {
    'version': 1,
    'filters': {
        'exc_filter': {
            '()': DebugFilter,
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
