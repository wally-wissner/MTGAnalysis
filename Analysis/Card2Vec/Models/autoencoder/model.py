from keras.layers import Dense, Input, LSTM, RepeatVector
from keras.models import Sequential
from keras.wrappers import scikit_learn
from sklearn.pipeline import Pipeline


def build_encoder(timesteps, input_dim, latent_dim):
    m = Sequential()
    m.add(LSTM(units=latent_dim, return_sequences=True))

    return m

def build_decoder():
    m = Sequential()
    m.add(LSTM(, return_sequences=True))
    return m


LSTM(units=100, activation='relu')


encoder_pipeline = Pipeline(steps=[

])

decoder_pipeline = Pipeline(steps=[

])