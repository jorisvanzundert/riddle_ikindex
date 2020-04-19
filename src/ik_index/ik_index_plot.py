import pickle
import matplotlib.pyplot as pyplot
import pandas
import seaborn as seaborn
from sklearn.metrics import f1_score
import subprocess
import os

def plot_ik_index( ik_index_result_package, save_output=False ):
    ik_index_result_package_file_path = ik_index_result_package[ 'file_path' ]
    data_frame = ik_index_result_package[ 'data_frame' ]
    equation = ik_index_result_package[ 'equation' ]
    measurement_title = 'ik-index'
    if 'measurement_title' in ik_index_result_package.keys():
        measurement_title = ik_index_result_package[ 'measurement_title' ]
    data_frame[ 'actual' ] = data_frame[ 'perspective' ].apply( lambda x: 1 if x == '1E PERS' else 3 )
    f1_scores = []
    for index in data_frame[ 'ik-index' ]:
        data_frame[ 'predicted' ] = data_frame[ 'ik-index' ].apply( lambda x: 1 if x > index else 3 )
        f1_scores.append( f1_score( data_frame[ 'actual' ], data_frame[ 'predicted' ] )  )
    data_frame.insert( len( data_frame.columns ), 'F1', f1_scores )

    ik_index_F1max = data_frame.loc[ data_frame['F1'].idxmax() ][ 'ik-index' ]

    data_frame[ 'actual' ] = data_frame[ 'perspective' ].apply( lambda x: '1st' if x == '1E PERS' else '3rd' )
    data_frame[ 'predicted' ] = data_frame[ 'ik-index' ].apply( lambda x: '1st' if x > ik_index_F1max else '3rd' )

    confusion_matrix = pandas.crosstab( data_frame[ 'actual' ], data_frame[ 'predicted' ], rownames=['Actual'], colnames=['Predicted'])

    seaborn.set()

    # Plot F1 curve
    pyplot.figure(1)
    pyplot.scatter( data_frame[ 'ik-index' ], data_frame[ 'F1' ], cmap="YlGnBu", alpha=0.5 )
    ax = pyplot.figure(1).axes[0]
    ax.set_xlabel( measurement_title )
    ax.set_ylabel( 'F1' )
    ax.set_title( 'F1 is max {} at {} {}'.format( round( max( data_frame[ 'F1' ] ), 4 ), measurement_title, round( ik_index_F1max, 4 ) ), pad=20 )
    ax.axvline( ik_index_F1max, linestyle=':', linewidth=1 )

    # Plot confusion matrix
    pyplot.figure( 2, figsize=[2,2] )
    seaborn.set( font_scale=1.5 )
    seaborn.heatmap( confusion_matrix, annot=True, cmap="Blues", cbar=False, fmt='g' )
    seaborn.set( font_scale=1 )

    # Plot swarm plot
    grid = seaborn.catplot( x="actual", y="ik-index", data=data_frame, cmap="Blues", kind="swarm" )
    grid.axes[0,0].set_ylabel( measurement_title )
    grid.axes[0,0].set_title( equation, pad=20 )
    grid.axes[0,0].axhline( ik_index_F1max, linestyle=':', linewidth=1 )

    if save_output:
        pyplot.figure(1).savefig( 'TMP_02.png', dpi=300, bbox_inches='tight' )
        pyplot.figure(2).savefig( 'TMP_03.png', dpi=300, bbox_inches='tight' )
        grid.savefig( 'TMP_01.png', dpi=300, bbox_inches='tight' )
        # Finishing touches with imagemagick
        subprocess.run( [ 'mogrify -gravity east -splice 200x0 TMP_*.png' ], shell=True )
        subprocess.run( [ 'convert +append -gravity center TMP_*.png {}.png'.format( ik_index_result_package_file_path.split( '.' )[0] ) ], shell=True )
        for file in [ 'TMP_01.png', 'TMP_02.png', 'TMP_03.png' ]:
            os.remove( file )
    else:
        pyplot.show()
