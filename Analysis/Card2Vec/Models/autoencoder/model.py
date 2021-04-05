from keras.layers import Dense, Input, LSTM, RepeatVector
from keras.models import Model
from keras.wrappers import scikit_learn
from sklearn.pipeline import Pipeline

# TODO
# def build_model(timesteps, input_dim, latent_dim):
#     inputs = Input(shape=(timesteps, input_dim))
#     encoded = LSTM(latent_dim)(inputs)
#
#     decoded = RepeatVector(timesteps)(encoded)
#     decoded = LSTM(input_dim, return_sequences=True)(decoded)
#
#     sequence_autoencoder = Model(inputs, decoded)
#     encoder = Model(inputs, encoded)
#
#
#
# LSTM(units=100, activation='relu')
#
#
# encoder_pipeline = Pipeline(steps=[
#
# ])
#
# decoder_pipeline = Pipeline(steps=[
#
# ])