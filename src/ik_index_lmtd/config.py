import sys
from os.path import dirname, abspath, join
work_dir = dirname( dirname( abspath( __file__ ) ) )
sys.path.append( work_dir )

PATH_TO_TEXTS_DIALOGUE_ONLY = 'data/undisclosed/lmtd/dialogue_only'
PATH_TO_TEXTS_NO_DIALOGUE = 'data/undisclosed/lmtd/no_dialogue'
PATH_TO_TEXTS = 'data/undisclosed/lmtd/full_txt'
PATH_TO_METADATA = 'data/undisclosed/lmtd/metadata/'
PATH_TO_RESULT = 'results/lmtd'
RESULT_FILE_PREFIX = 'lmtd'
