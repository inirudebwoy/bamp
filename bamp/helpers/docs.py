from bamp.config import DEFAULT_CONFIG

TAG_OPTION_METAVAR = 'TAG_MESSAGE'
TAG_OPTION_HELP = (
    'The name of the tag to create. If nothing is passed the default '
    'value of {0} is used. If omitted tag is not created.'.
    format(DEFAULT_CONFIG.get('tag'))
)
