import pickle
import matplotlib.pyplot as pyplot
import pandas
import seaborn as seaborn
from sklearn.metrics import f1_score
import subprocess
import os

def plot_adzd_predictions( meta_package_file_path, save_output=True ):
    with open( meta_package_file_path, 'rb' ) as pickle_file:
        meta_package = pickle.load( pickle_file )
        data_frame = meta_package[ 'data_frame' ]
        equation = meta_package[ 'equation' ]

    data_frame[ 'actual' ] = data_frame[ 'text-type' ].apply( lambda x: 1 if x == 'Dialoog' else 3 )
    f1_scores = []
    for index in data_frame[ 'prediction' ]:
        data_frame[ 'predicted' ] = data_frame[ 'prediction' ].apply( lambda x: 1 if x > index else 3 )
        f1_scores.append( f1_score( data_frame[ 'actual' ], data_frame[ 'predicted' ] )  )
    data_frame.insert( len( data_frame.columns ), 'F1', f1_scores )

    ik_index_F1max = data_frame.loc[ data_frame['F1'].idxmax() ][ 'prediction' ]

    data_frame[ 'actual' ] = data_frame[ 'text-type' ].apply( lambda x: 'D' if x == 'Dialoog' else 'V' )
    data_frame[ 'predicted' ] = data_frame[ 'prediction' ].apply( lambda x: 'D' if x > ik_index_F1max else 'V' )

    confusion_matrix = pandas.crosstab( data_frame[ 'actual' ], data_frame[ 'predicted' ], rownames=['Actual'], colnames=['Predicted'])

    seaborn.set()

    # Plot F1 curve
    pyplot.figure(1)
    pyplot.scatter( data_frame[ 'prediction' ], data_frame[ 'F1' ], cmap="YlGnBu", alpha=0.5 )
    ax = pyplot.figure(1).axes[0]
    ax.set_xlabel( 'prediction' )
    ax.set_ylabel( 'F1' )
    ax.set_title( 'F1 is max {} at prediction value {}'.format( round( max( data_frame[ 'F1' ] ), 4 ), round( ik_index_F1max, 4 ) ), pad=20 )
    ax.axvline( ik_index_F1max, linestyle=':', linewidth=1 )

    # Plot confusion matrix
    pyplot.figure( 2, figsize=[2,2] )
    seaborn.set( font_scale=1.5 )
    seaborn.heatmap( confusion_matrix, annot=True, cmap="Blues", cbar=False, fmt='g' )
    seaborn.set( font_scale=1 )

    # Plot swarm plot
    grid = seaborn.catplot( x="text-type", y="prediction", data=data_frame, cmap="Blues", kind="swarm" )
    grid.axes[0,0].set_title( equation, pad=20 )
    grid.axes[0,0].axhline( ik_index_F1max, linestyle=':', linewidth=1 )

    if save_output:
        pyplot.figure(1).savefig( 'TMP_02.png', dpi=300, bbox_inches='tight' )
        pyplot.figure(2).savefig( 'TMP_03.png', dpi=300, bbox_inches='tight' )
        grid.savefig( 'TMP_01.png', dpi=300, bbox_inches='tight' )
        # Finishing touches with imagemagick
        subprocess.run( [ 'mogrify -gravity east -splice 200x0 TMP_*.png' ], shell=True )
        subprocess.run( [ 'convert +append -gravity center TMP_*.png {}.png'.format( meta_package_file_path.split( '.' )[0] ) ], shell=True )
        for file in [ 'TMP_01.png', 'TMP_02.png', 'TMP_03.png' ]:
            os.remove( file )
    else:
        pyplot.show()
