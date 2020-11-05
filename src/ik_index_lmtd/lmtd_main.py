import os
import pickle
import pandas
from datetime import datetime
import config
from ik_index.ik_index import ik_index
from ik_index.ik_index_plot import plot_ik_index

def timestamp():
    now = datetime.now()
    return ( now, now.strftime("%Y%m%d_%H%M" ) )

def write_pickle( ik_index_result_package, path_to_texts, save=False ):
    file_path = os.path.join( config.PATH_TO_RESULT, '{}_{}_{}.pickle'.format( config.RESULT_FILE_PREFIX, os.path.basename( path_to_texts ), timestamp()[1] ) )
    ik_index_result_package[ 'file_path' ] = file_path
    if save:
        with open( file_path, 'wb' ) as pickle_file:
             pickle.dump( ik_index_result_package, pickle_file )
    return ik_index_result_package

def infer_ik_index( index_meta, path_to_texts, save_as_file=False ):
    data_frame, equation_latex = ik_index( path_to_texts, index_meta )
    ik_index_result_package = { 'data_frame': data_frame, 'equation': equation_latex }
    ik_index_result_package = write_pickle( ik_index_result_package, path_to_texts, save=save_as_file )
    return ik_index_result_package

# MAIN
index_meta = {
    'enumerator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze' ],
    'denominator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze', 'hij', 'zij', 'ze', 'je', 'jou[w]', 'haar', 'zijn', 'jullie' ]
}
dfs = []
for path in [ config.PATH_TO_TEXTS, config.PATH_TO_TEXTS_NO_DIALOGUE, config.PATH_TO_TEXTS_DIALOGUE_ONLY ]:
    ik_index_result_package = infer_ik_index( index_meta, path, save_as_file=False )
    ik_index_result_package_file_path = ik_index_result_package[ 'file_path' ]
    data_frame = ik_index_result_package[ 'data_frame' ]
    print( data_frame )
    equation = ik_index_result_package[ 'equation' ]
    data_frame.sort_index( axis='index', inplace=True )
    data_frame.reset_index( inplace=True )
    data_frame.drop( axis=1, labels='perspective', inplace=True )
    label = os.path.basename( path )[0] + os.path.basename( path ).split( '_' )[1][0]
    data_frame.rename( columns={ 'index': 'index_{}'.format( label ), 'ik-index': 'ik-index_{}'.format( label ), 'token_count': 'token_count_{}'.format( label ) }, inplace=True )
    dfs.append( data_frame )
    # plot_ik_index( ik_index_result_package, save_output=False )

data_frame = pandas.concat( dfs, axis=1 )
data_frame[ 'ratio_dialogue_text' ] = data_frame[ 'token_count_do' ] / data_frame[ 'token_count_ft' ]
meta_data = pandas.read_csv( os.path.join( config.PATH_TO_METADATA, 'Data-Table 1.csv' ) )
meta_data[ 'NB' ] = meta_data[ 'NB' ].fillna( ' ' )
meta_data[ 'org_lang' ] = meta_data[ 'Translated' ] + meta_data[ 'NB' ]
map = { 'yes (Eng) ': 'en',
        'yes (non-Eng)Deens':'da',
        'yes (non-Eng)Zweeds':'se',
        'yes (non-Eng)Noors':'no',
        'yes (non-Eng)Frans':'fr',
        'yes (non-Eng)Duits':'de',
        'yes (non-Eng)Italiaans':'it',
        'yes (non-Eng)Spaans':'sp',
        'no ':'nl' }
meta_data[ 'org_lang' ] = meta_data[ 'org_lang' ].map( map ).fillna( meta_data[ 'org_lang' ] )
data_frame[ 'genre_riddle' ] = meta_data[ 'GenreRiddle' ]
data_frame[ 'mean_literary_rating' ] = meta_data[ 'MeanLitRating' ]
data_frame[ 'org_lang' ] = meta_data[ 'org_lang' ]
print( data_frame.columns )
pandas.set_option( 'display.max_columns', None )
# data_frame.to_csv( os.path.join( config.PATH_TO_METADATA, 'data_lmtd_002.csv' ) )
