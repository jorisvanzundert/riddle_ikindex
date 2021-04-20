# daTA_FRAME perspectvie, ik-index, predicted, actual
import pandas
import regex
import pickle
import os
from ik_index_plot import plot_ik_index

file_path = 'results/ik-ml-1001_20210421_0029.txt'

with open( file_path ) as result_file:
    lines = result_file.readlines()[1:]

results = {}
for result in lines:
    result = regex.findall( r'(?:.*?\s\s+)|.*$', result )
    if result[1].strip() == '1.0':
        perspective = '1E PERS'
    else:
        perspective = '3E PERS'
    results[ result[0].strip() ] = [ perspective, float( result[2] ) ]
    data_frame = pandas.DataFrame.from_dict( results, orient="index", columns=[ 'perspective', 'ik-index' ] )

meta_package = { 'data_frame': data_frame, 'equation': 'ML', 'measurement_title': 'ml prediction' }
file_path = '{}.pickle'.format( os.path.splitext( file_path )[0] )
meta_package[ 'file_path' ] = file_path
with open( file_path, 'wb' ) as pickle_file:
     pickle.dump( meta_package, pickle_file )
plot_ik_index( meta_package, True )
