# remove ''""“”‘’
# replace !? --> ,
# tokenize op whitespace
# leave one out testing
import os
import glob
import regex
import numpy
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
import ml_model

PATH_TO_DATA = 'AD_ZD'
PATH_TO_DIALOGUE = os.path.join( PATH_TO_DATA, "Alleen dialoog (20)" )
PATH_TO_NON_DIALOGUE = os.path.join( PATH_TO_DATA, "Zonder dialoog (20)" )

def clean( text ):
    text = regex.sub( r'\d+|[\'"“”‘’\-–—.,!?]', ' ', text ).lower()
    return regex.sub( r'\s+', ' ', text )

def shortname( file_path ):
    return os.path.basename( file_path ).split( '.' )[0]

def get_text( file_path ):
    with open( file_path, "r" ) as text_file:
        return clean( text_file.read() )

dialogue_file_paths = sorted( glob.glob( "{}/*.txt".format( PATH_TO_DIALOGUE ) ) )
non_dialogue_file_paths = sorted( glob.glob( "{}/*.txt".format( PATH_TO_NON_DIALOGUE ) ) )
all_file_paths = dialogue_file_paths + non_dialogue_file_paths
all_labels = [1] * len( dialogue_file_paths ) + [0] * len( non_dialogue_file_paths )

results = pandas.DataFrame( columns=[ 'label', 'predicted' ] )
for idx, file_path in enumerate( all_file_paths ):
    training_texts = []
    for path in ( path for path in all_file_paths if( path != file_path ) ):
        training_texts.append( get_text( path ) )
    training_labels = all_labels.copy()
    test_label = training_labels.pop( idx )
    test_text = get_text( file_path )
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform( training_texts )
    # feature_names = vectorizer.get_feature_names()
    model = ml_model.DeepLearningModel()
    model.build( ( vectors, numpy.array( training_labels ) ) )
    test_vector = vectorizer.transform( [ test_text ] )
    predictions = list( model.predict( test_vector ) )
    for idx, prediction in enumerate( predictions ):
        results.loc[ shortname( file_path ) ] = [ test_label, prediction[0] ]
    # TODO: put to decent dataframe and pickle
    # Last time for plotting save print to txt
    # parsed the txt file(s) into a dataframe
    print( results )
