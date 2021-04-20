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

PATH_TO_DATA = 'data/undisclosed/AD_ZD'
PATH_TO_1001 = os.path.join( PATH_TO_DATA, "1001" )

def clean( text ):
    text = regex.sub( r'\d+|[\'"“”‘’\-–—.,!?]', ' ', text ).lower()
    return regex.sub( r'\s+', ' ', text )

def shortname( file_path ):
    return os.path.basename( file_path ).split( '.' )[0]

def get_text( file_path ):
    with open( file_path, "r" ) as text_file:
        return clean( text_file.read() )

first_person_file_paths = sorted( glob.glob( "{}/1E PERS*.txt".format( PATH_TO_1001 ) ) )
third_person_file_paths = sorted( glob.glob( "{}/3E PERS*.txt".format( PATH_TO_1001 ) ) )

all_file_paths = first_person_file_paths + third_person_file_paths
all_labels = [1] * len( first_person_file_paths ) + [0] * len( third_person_file_paths )

results = pandas.DataFrame( columns=[ 'label', 'predicted' ] )
print( all_labels )
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
    # Last time for plotting parsed the tmp file into a dataframe
    with open( 'results/ik-ml-1001_20210421_0029.txt', 'w' ) as result_file:
        result_file.write( results.to_string() )
