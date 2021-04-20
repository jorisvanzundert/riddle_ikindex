import pickle
import matplotlib.pyplot as pyplot
import seaborn
from matplotlib.path import Path
import matplotlib.patches as patches
from random import shuffle
from random import randrange
from matplotlib import gridspec
import pandas


def get_verts( origin, target, test=False ):
    origin = float( origin )
    target = float( target )
    if test:
        return  [
            ( 0.0, origin ), # MOVETO
            ( 0.3, origin ), # LINETO
            ( 0.4, origin ), # CURVE3
            ( 0.5, origin + (target-origin)/2 ), # MOVETO
            ( 0.6, target ), # CURVE3
            ( 0.7, target ), # LINETO
            ( 1.0, target )  # LINETO
        ]
    else:
        return  [
            ( 0.0, origin ), # MOVETO
            ( 0.1, origin ), # LINETO
            ( 0.2, origin ), # CURVE3
            ( 0.5, origin + (target-origin)/2 ), # MOVETO
            ( 0.8, target ), # CURVE3
            ( 0.9, target ), # LINETO
            ( 1.0, target )  # LINETO
        ]


def plot_ml_vs_idx( save_output=True, test=False ):

    with open( 'results/tmp-datafram-b.pickle', 'rb' ) as pickle_file:
         data_frame = pickle.load( pickle_file )

    # We want to create a graph that contains a comparison of predictions
    # by machine learning (ml) and ik-index. Two outer 'panes' will have
    # the same comparison of ml prediction vs ik-index but in different orders,
    # one sorted by ml prediction and one sorted by ik-index.
    # The middle pane will hold the text labels, twice in those different orders.
    # bezier curves will connect the labels with the same text names.

    # The actual labels, data, and colors for the left pane (0)
    # and the right pane (2) that we'll be working with
    data_frame[ 'bezier_index' ] = range( len( data_frame ) )
    data_frame2 = data_frame.sort_values( [ 'ik-index' ], ascending=False )
    X = data_frame.index.values
    Y_ik_index = data_frame[ 'ik-index' ]
    Y_ml_index = data_frame[ 'ml-index' ]
    ik_color = data_frame[ 'ik-color' ]
    ml_color = data_frame[ 'ml-color' ]
    X2 = data_frame2.index.values
    Y_ik_index2 = data_frame2[ 'ik-index' ]
    Y_ml_index2 = data_frame2[ 'ml-index' ]
    ik_color2 = data_frame2[ 'ik-color' ]
    ml_color2 = data_frame2[ 'ml-color' ]
    if test:
        X = X[300:330]
        Y_ik_index = Y_ik_index[300:330]
        Y_ml_index = Y_ml_index[300:330]
        ik_color = data_frame[ 'ik-color' ][300:330]
        ml_color = data_frame[ 'ml-color' ][300:330]
        X2 = X.copy()
        Y_ik_index2 = Y_ik_index.copy()
        Y_ml_index2 = Y_ml_index.copy()
        ik_color2 = ik_color.copy()
        ml_color2 = ml_color.copy()
        shuffle( Y_ik_index2 )
        shuffle( Y_ml_index2 )
        shuffle( ik_color2 )
        shuffle( ml_color2 )

    # Accept some pretty styling out of the box
    seaborn.set()
    seaborn.set_palette( seaborn.color_palette( 'coolwarm' ) )

    # Create the figure as a whole, set dimensions
    fig_height = 500
    fig_width = 100
    ratios = [ 0.2, 0.6, 0.2 ]
    if test:
        fig_height = 10
        fig_width = 40
        ratios = [ 0.3, 0.4, 0.3 ]
    figure = pyplot.figure( figsize=( fig_width, fig_height ) )

    # Set up a grid, we want a wider middle 'pane' to display the text labels
    # and the bezier connectors
    grid_spec = gridspec.GridSpec( 1, 3, width_ratios=ratios )

    # We don't need space between the subplots
    pyplot.subplots_adjust( wspace=0 )

    # # These are just temporary aids to see if suboplots align exactly
    # pyplot.rcParams["axes.edgecolor"] = '0.15'
    # pyplot.rcParams["axes.linewidth"] = 1.25

    # a1 is the middle pane with text labels and connectors
    a1 = pyplot.subplot( grid_spec[1] )
    # we hadrly need a gridded background or color for the middle pane,
    # but still a hint of color is nice, so…
    a1.patch.set_alpha( 0.4 )
    a1.barh( X, [0] * len( X ), color=data_frame['ik-color'], height=0.5 )
    a1.set_xlim( left=0.0, right=1.0 )
    if not test:
        a1.set_ylim( bottom=-1.0, top=1002 )
    # we need no ticks, major or minor, nor labels in the mid pane
    a1.tick_params( axis='x', which='both', bottom=False, labelbottom=False )

    # Add in Bezier magics
    origins = data_frame[ 'bezier_index' ].tolist()
    targets = data_frame2[ 'bezier_index' ].tolist()
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CURVE3,
        Path.MOVETO,
        Path.CURVE3,
        Path.LINETO,
        Path.LINETO
    ]
    if test:
        origins = list( range( 30 ) )
        targets = list( range( 30 ) )
        # a bit of shifting to create interesting beziers
        for i in range(10):
            targets.append( targets.pop( randrange(30) ) )
            beziers = list( zip( origins, targets ) )
        for bezier in beziers:
            path = Path( get_verts( bezier[0], bezier[1], test ), codes )
            patch = patches.PathPatch( path, facecolor='none', lw=14, edgecolor='midnightblue', alpha=0.1 )
            a1.add_patch( patch )
    else:
        for origin in origins:
            target = targets.index( origin )
            path = Path( get_verts( origin, target ), codes )
            patch = patches.PathPatch( path, facecolor='none', lw=2, edgecolor='midnightblue', alpha=0.2 )
            a1.add_patch( patch )


    # a0 is the left pane
    a0 = pyplot.subplot( grid_spec[0] )
    # make sure this thing is printed on top of the bezier connectors stuff
    a0.set_zorder( 100 )
    a0.barh( X, Y_ik_index, color=ik_color, height=0.5 )
    a0.barh( X, -Y_ml_index, color=ml_color, height=0.5 )
    # a0.tick_params( labelleft=False )
    # Make the x axis show ticks from 1.0 to 0.0 to 1.0
    # (for the mirrored hbar chart).
    a0.set_xlim( right=1.05, left=-1.05 )
    if not test:
        a0.set_ylim( bottom=-1.0, top=1002 )
    ticks = a0.get_xticks()
    a0.set_xticklabels( [ abs( tick ) for tick in ticks ] )
    # We have to mess around with labels here, as they need to be on the (non
    # default) right side..
    a0.yaxis.set_label_position( 'right' )
    a0.yaxis.tick_right()
    a0.tick_params( axis='y', which='both', right=False )
    a0.axvline( 0, linewidth=1, color='darkorchid' )

    # a2 is the right pane
    a2 = pyplot.subplot( grid_spec[2] )
    # make sure this thing is printed on top of the bezier connectors stuff
    a2.set_zorder( 101 )
    a2.barh( X2, -Y_ik_index2, color=ik_color2, height=0.5 )
    a2.barh( X2, Y_ml_index2, color=ml_color2, height=0.5 )
    # axes.set_ylim( bottom=-1.0, top=1002 )
    # Make the x axis show ticks from 1.0 to 0.0 to 1.0
    # (for th mirrored hbar chart).
    a2.set_xlim( right=1.05, left=-1.05 )
    if not test:
        a2.set_ylim( bottom=-1.0, top=1002 )
    ticks = a2.get_xticks()
    a2.set_xticklabels( [ abs( tick ) for tick in ticks ] )
    a2.axvline( 0, linewidth=1, color='darkorchid' )
    # We don't have to mess around with labels here, as it comes with the right
    # labels and positioning on the left out of the box (obviously).

    pyplot.figure(1).savefig( 'results/ml_vs_index_spike.png', dpi=95, bbox_inches='tight' )
    # pyplot.show()

# main

plot_ml_vs_idx( save_output=False, test=True )
