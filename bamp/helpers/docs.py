from bamp.config import DEFAULT_CONFIG

FILES_OPTION_HELP = (
    'File where version can be found. '
    'Can be used multiple times.'
)
TAG_OPTION_METAVAR = 'TAG_MESSAGE'
TAG_OPTION_HELP = (
    'The name of the tag to create. If nothing is passed the default '
    'value of {0} is used. If omitted tag is not created.'.
    format(DEFAULT_CONFIG.get('tag'))
)
VERSION_OPTION_HELP = 'Current version of the program.'
VCS_OPTION_HELP = 'Specify VCS to use.'
MESSAGE_OPTION_HELP = 'Commit message to use.'
CONFIG_OPTION_HELP = 'Path to a config file.'
DEBUG_OPTION_HELP = 'Enable debug flag.'
