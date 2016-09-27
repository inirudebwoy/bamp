from bamp.config import DEFAULT_CONFIG

FILES_OPTION_HELP = ('File where version can be found. '
                     'Can be used multiple times.')
TAG_NAME_OPTION_METAVAR = 'TAG_NAME'
TAG_NAME_OPTION_HELP = (
    'The name of the tag to create. If nothing is passed the default '
    'value of {0} is used. Used with --tag option.'.format(
        DEFAULT_CONFIG.get('tag')))
TAG_FLAG_OPTION_HELP = (
    'Toggle for creating tag with a commit. If passed tag will '
    'be created. --tag-name/-T specifies what will be the tag name')
VERSION_OPTION_HELP = 'Current version of the program.'
VCS_OPTION_HELP = 'Specify VCS to use.'
MESSAGE_OPTION_HELP = 'Commit message to use.'
COMMIT_FLAG_OPTION_HELP = (
    'Toggle for creating a commit. If passed commit '
    'will be created. --message/-m specifies what is the commit message.')
CONFIG_OPTION_HELP = 'Path to a config file.'
DEBUG_OPTION_HELP = 'Enable debug flag.'
