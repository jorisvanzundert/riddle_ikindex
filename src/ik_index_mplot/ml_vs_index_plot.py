import pickle
import matplotlib.pyplot as pyplot
import pandas
# import seaborn as seaborn
# import os
import numpy
import seaborn
from sklearn.metrics import f1_score

def extract_meta_package( meta_package_file_path ):
    with open( meta_package_file_path, 'rb' ) as pickle_file:
        meta_package = pickle.load( pickle_file )
    return meta_package

def plot_adzd_predictions( meta_package_file_paths, save_output=True ):
    meta_package_a = extract_meta_package( meta_package_file_paths[0] )
    meta_package_b = extract_meta_package( meta_package_file_paths[1] )
    data_frame_a = meta_package_a[ 'data_frame' ].sort_index()
    data_frame_b = meta_package_b[ 'data_frame' ].sort_index()
    data_frame_b[ 'ml-prediction' ] = data_frame_a[ 'ik-index' ]
    data_frame_b = data_frame_b.sort_values( ['ml-prediction'], ascending=False )
    print(  data_frame_b.iloc[30:40] )
    print( '------------' )
    print(  data_frame_b.iloc[30:40].index.values )

    pandas.set_option('display.max_columns', 20)

    data_frame_b[ 'actual' ] = data_frame_b[ 'perspective' ].apply( lambda x: 1 if x == '1E PERS' else 3 )
    f1_scores = []
    for index in data_frame_b[ 'ik-index' ]:
        data_frame_b[ 'ik-index-prediction' ] = data_frame_b[ 'ik-index' ].apply( lambda x: 1 if x > index else 3 )
        f1_scores.append( f1_score( data_frame_b[ 'actual' ], data_frame_b[ 'ik-index-prediction' ] )  )
    data_frame_b.insert( len( data_frame_b.columns ), 'F1-ik-index', f1_scores )
    index_F1max = data_frame_b.loc[ data_frame_b[ 'F1-ik-index' ].idxmax() ][ 'ik-index' ]
    data_frame_b[ 'ik-index-prediction' ] = data_frame_b[ 'ik-index' ].apply( lambda x: 1 if x > index_F1max else 3 )

    data_frame_b = data_frame_b.rename( columns={ 'ml-prediction': 'ml-index' } )
    print('>>>>>>>', data_frame_b['ik-index'] )
    f1_scores = []
    for index in data_frame_b[ 'ml-index' ]:
        data_frame_b[ 'ml-index-prediction' ] = data_frame_b[ 'ml-index' ].apply( lambda x: 1 if x > index else 3 )
        f1_scores.append( f1_score( data_frame_b[ 'actual' ], data_frame_b[ 'ml-index-prediction' ] )  )
    data_frame_b.insert( len( data_frame_b.columns ), 'F1-ml-index', f1_scores )
    index_F1max = data_frame_b.loc[ data_frame_b[ 'F1-ml-index' ].idxmax() ][ 'ml-index' ]
    data_frame_b[ 'ml-index-prediction' ] = data_frame_b[ 'ml-index' ].apply( lambda x: 1 if x > index_F1max else 3 )

    data_frame_b[ 'ml-correct' ] = data_frame_b.apply( lambda row: 1 if row['ml-index-prediction']==row['actual'] else 0, axis=1 )
    data_frame_b[ 'ik-correct' ] = data_frame_b.apply( lambda row: 1 if row['ik-index-prediction']==row['actual'] else 0, axis=1 )

    data_frame_b[ 'ml-color' ] = data_frame_b.apply( lambda row: 'deepskyblue' if row['ml-index-prediction']==row['actual'] else 'maroon', axis=1 )
    data_frame_b[ 'ik-color' ] = data_frame_b.apply( lambda row: 'orange' if row['ik-index-prediction']==row['actual'] else 'maroon', axis=1 )

    seaborn.set()
    seaborn.set_palette( seaborn.color_palette( 'coolwarm' ) )

    X = data_frame_b.index.values
    figure = pyplot.figure( figsize=( 10, 500 ) )
    axes = figure.add_axes( [ 1, 1, 1, 1 ] ) # left, bottom, width, height in figure dimension fractions
    pyplot.barh( X, data_frame_b['ik-index'], color=data_frame_b['ik-color'], height=0.5 )
    pyplot.barh( X, -data_frame_b['ml-index'], color=data_frame_b['ml-color'], height=0.5 )
    axes.set_xlim( right=1.0 )
    axes.set_ylim( bottom=-1.0, top=1002 )
    ticks = axes.get_xticks()
    axes.set_xticklabels( [ abs( tick ) for tick in ticks ] )
    axes.axvline( 0, linewidth=1, color='darkorchid' )
    pyplot.figure(1).savefig( 'results/ml_vs_index_20200129_0127.png', dpi=95, bbox_inches='tight' )

# main

plot_adzd_predictions( [ 'results/ik-ml-1001_20200128_1304.pickle', 'results/ik-index-1001_20200128_1247.pickle' ], False )
