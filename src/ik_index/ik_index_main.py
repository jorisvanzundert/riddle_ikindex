import os
import pickle
import pandas
from datetime import datetime
import config
from ik_index import ik_index
from ik_index_plot import plot_ik_index

def timestamp():
    now = datetime.now()
    return ( now, now.strftime("%Y%m%d_%H%M" ) )

def write_pickle( ik_index_result_package, save=False ):
    file_path = os.path.join( config.PATH_TO_RESULT, '{}_{}.pickle'.format( config.RESULT_FILE_PREFIX, timestamp()[1] ) )
    ik_index_result_package[ 'file_path' ] = file_path
    if save:
        with open( file_path, 'wb' ) as pickle_file:
             pickle.dump( ik_index_result_package, pickle_file )
    return ik_index_result_package

def infer_ik_index( index_meta, measurement_title='ik-index', save_as_file=False ):
    data_frame, equation_latex = ik_index( config.PATH_TO_TEXTS, index_meta )
    ik_index_result_package = { 'data_frame': data_frame, 'equation': equation_latex, 'measurement_title': measurement_title }
    ik_index_result_package = write_pickle( ik_index_result_package, save=save_as_file )
    return ik_index_result_package

# MAIN
index_meta = {
    'enumerator': [ 'ik' ],
    'denominator': [ 'ik', 'hij', 'zij', 'ze', 'wij', 'we' ]
}
# ik_index_result = infer_ik_index( index_meta, save_as_file=True )

# pandas.set_option( 'display.max_rows', None )
# print( ik_index_result[ 'data_frame' ] )
# print( ik_index_result[ 'equation' ] )

index_meta = {
    'enumerator': [ 'ik', 'wij', 'we' ],
    'denominator': [ 'ik', 'wij', 'we', 'hij', 'zij', 'ze' ]
}
# ik_index_result = infer_ik_index( index_meta, save_as_file=True )

index_meta = {
    'enumerator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze' ],
    'denominator': [ 'ik', 'wij', 'we', 'me', 'mij[n]', 'ons', 'onze', 'hij', 'zij', 'ze', 'je', 'jou[w]', 'haar', 'zijn', 'jullie' ]
}
ik_index_result_package = infer_ik_index( index_meta, measurement_title='I-index', save_as_file=False )
plot_ik_index( ik_index_result_package, save_output=True )
