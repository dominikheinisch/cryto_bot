from turtle import shape

import numpy as np
import pickle
import tensorflow as tf

from crypto_bot.utils.func import named_timer, ticker_to_path


def load(ticker):
    with open(ticker_to_path(ticker), 'rb') as pickle_file:
        return pickle.load(pickle_file)


def print_data(model, x, current_prices, to_predict):
    predictions = model(x).numpy()

    print('-------------------------------------------------------------------------')
    temp = np.zeros(shape=(predictions.shape[0], 6))
    # up = (predictions - y_prev) > 0
    temp[:, 0:2] = predictions
    temp[:, 2] = current_prices
    temp[:, 3] = to_predict
    temp[:, 4] = (to_predict - current_prices) * predictions[:, 0]
    temp[:, 5] = (current_prices - to_predict) * predictions[:, 1]
    print(temp)

    print('sum+ :', np.sum(temp[:, 4]))
    print('sum- :', np.sum(temp[:, 5]))

    print('min', np.min(predictions))
    print('max_val', np.max(predictions))
    print('weights', model.weights)

    # test_loss, test_acc = model.evaluate(x, y)
    model.summary()


def preprocess():
    data = load('ethpln')
    max_val = data['max_val']
    x = data['prices'] * max_val
    current_prices = x[:, 0].copy()
    to_predict = data['prices_to_predict'] * max_val

    def cut_data(x ,to_predict):
        cut_idx = 0
        return x[cut_idx:], current_prices[cut_idx:], to_predict[cut_idx:]

    x, current_prices, to_predict = cut_data(x, to_predict)
    # x /= np.max(x)
    print(x[:10])
    x = x * x
    print(x[:10])
    x /= x.sum(axis=1)[:, np.newaxis]
    # x = tf.nn.softmax(x, axis=1)
    print(x[:10])

    # print(x, current_prices, to_predict)

    # one_hot encoding
    y = np.zeros(shape=(to_predict.shape[0], 2))
    y[:, 0] = to_predict > current_prices
    y[:, 1] = 1 - y[:, 0]
    print('************************************************************')
    # print(y)
    print(x.shape, current_prices.shape, to_predict.shape)
    assert x.shape[0] == current_prices.shape[0] and x.shape[0] == to_predict.shape[0]
    return x, y, current_prices, to_predict


def split(arr):
    treshold = 0.7
    treshold_idx = int(treshold * arr.shape[0])
    return arr[:treshold_idx], arr[treshold_idx:]


def train():
    np.set_printoptions(precision=2, suppress=True, threshold=10000)
    x, y, current_prices, to_predict = preprocess()
    x_train, x_test = split(x)
    y_train, y_test = split(y)
    current_prices_train, current_prices_test = split(current_prices)
    to_predict_train, to_predict_test = split(to_predict)


    # print(x_train, y_train)
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(x_train.shape[1],)))
    model.add(tf.keras.layers.Dense(
        units=x_train.shape[1],
        activation=tf.keras.layers.Activation('relu'),
        # kernel_initializer=tf.keras.initializers.RandomUniform(minval=0.05, maxval=0.2)
        # kernel_constraint=tf.keras.constraints.min_max_norm(
        #     min_value=0.0, max_value=0.1, rate=1.0, axis=0
        # )
    ))
    # model.add(tf.keras.layers.Dense(
    #     units=5,
    #     activation=tf.keras.layers.Activation('relu'),
    # ))
    # model.add(tf.keras.layers.Dropout(0.1))
    model.add(tf.keras.layers.Dense(
        units=2,
        # kernel_constraint=tf.keras.constraints.MinMaxNorm(min_value=0.0, max_value=0.3),
        # kernel_constraint=tf.keras.constraints.NonNeg(),
        # activation=tf.keras.layers.Activation('softmax_cross_entropy_with_logits'),
        # activation=tf.keras.layers.Activation('softmax'),
        # kernel_initializer=tf.keras.initializers.RandomUniform(minval=0.03, maxval=0.1, seed=None),
    ))


    model.compile(
        # optimizer=tf.keras.optimizers.RMSprop(),  # Optimizer
        # Loss function to minimize
        loss=tf.keras.losses.BinaryCrossentropy(),
        # loss=tf.keras.losses.CategoricalCrossentropy(),
        # loss=tf.nn.softmax_cross_entropy_with_logits,
        # List of metrics to monitor
        # metrics=[tf.keras.metrics.BinaryCrossentropy()],
        # metrics=[tf.keras.metrics.CategoricalAccuracy()],

        # optimizer='adam',
        # loss=tf.keras.losses.MeanSquaredError(),
        # loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=['accuracy'],
    )
    # model.compile(
    #     # optimizer='adam',
    #     loss=tf.nn.softmax_cross_entropy_with_logits,
    #     metrics=['accuracy'],
    # )

    model.fit(
        x_train,
        y_train,
        batch_size=8,
        epochs=50,
    )


    print_data(model, x_train, current_prices_train, to_predict_train)
    # print('==========================================================================================================')
    # print_data(model, x_test, y_test, max_val)

    # aaa = np.asarray([[1, 2, 3, 4], [9, 5, 3, 1]], dtype=float)
    # print(tf.nn.softmax(aaa))
    # print(x / np.linalg.norm(x))

train()
