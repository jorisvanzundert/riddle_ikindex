import numpy
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense


class NoDeepLearningModelError( Exception ):
    def __str__( self ):
        return( "NoDeepLearningModelError" )

class TestingDimensionError( Exception ):
    def __str__( self ):
        return( "TestingDimensionError" )

class DeepLearningModel:

    def __init__( self ):
        self.model = None
        self.x_dim = 0

    def build( self, training_data, batch_size=20, epochs=5 ):
        x_tdm, y_narr = training_data
        # x_narr = numpy.array( x_tdm.toarray() )
        x_narr = x_tdm
        self.x_dim = x_narr.shape[1]
        # neurons in hidden layer: a rule of thumb is 2/3 * (input + output)
        neurons_hidden_layer = int( round( ( self.x_dim + 1 ) * 0.66 ) )
        # fix random seed for reproducibility
        seed = 7
        numpy.random.seed( seed )
        # create model
        self.model = Sequential()
        self.model.add( Dense( 12, input_dim=self.x_dim, activation='relu', name='primary_input', kernel_initializer='uniform' ) )
        self.model.add( Dense( neurons_hidden_layer, activation='relu', kernel_initializer='uniform' ) )
        self.model.add( Dense( 1, activation='sigmoid', kernel_initializer='uniform' ) )
        # Compile model
        self.model.compile( loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'] )
        # Fit the model
        verbosity = 1
        self.model.fit( x_narr, y_narr, batch_size, epochs, verbosity )
        # evaluate the model
        scores = self.model.evaluate( x_narr, y_narr )
        # print( self.model.metrics_names )
        # print( "%s: %.2f%%" % ( self.model.metrics_names[1], scores[1]*100 ) )
        accuracy = scores[1]*100
        return accuracy

    def predict( self, narr ):
        if self.model != None:
            if self.x_dim == narr.shape[1]:
                # this ignores words not seen before! (Given a large enough corpus this
                # shouldn't be a big problem.)
                predictions = self.model.predict( narr )
                return predictions
            else:
                raise TestingDimensionError
        else:
            raise NoDeepLearningModelError

    def save( self, path, name ):
        self.model.save( os.path.join( path, '{n}.h5'.format( n=name  ) ) )

    def load( self, path, name ):
        del self.model
        self.model = load_model( os.path.join( path, '{n}.h5'.format( n=name  ) ) )
        self.x_dim = self.model.get_layer( 'primary_input' ).input_shape[1]
