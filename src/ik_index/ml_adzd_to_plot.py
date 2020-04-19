# daTA_FRAME perspectvie, ik-index, predicted, actual
import pandas
import regex
import pickle
import os
from ml_adzd_plot import plot_adzd_predictions

file_path = 'results/azdz-ml_20200127_2330.txt'

with open( file_path ) as result_file:
    lines = result_file.readlines()[3:]

results = {}
for result in lines:
    result = regex.findall( r'(?:.*?\s\s+)|.*$', result )
    if result[1].strip() == '1.0':
        perspective = 'Dialoog'
    else:
        perspective = 'Vertel'
    results[ result[0].strip() ] = [ perspective, float( result[2] ) ]
    data_frame = pandas.DataFrame.from_dict( results, orient="index", columns=[ 'text-type', 'prediction' ] )
print( data_frame )
meta_package = { 'data_frame': data_frame, 'equation': 'ML' }
file_path = '{}.pickle'.format( os.path.splitext( file_path )[0] )
meta_package[ 'file_path' ] = file_path
with open( file_path, 'wb' ) as pickle_file:
     pickle.dump( meta_package, pickle_file )
plot_adzd_predictions( file_path, True )
