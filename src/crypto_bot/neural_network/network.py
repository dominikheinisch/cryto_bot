from turtle import shape

import numpy as np
import pickle
import tensorflow as tf

from crypto_bot.utils.func import named_timer, ticker_to_path


def load(ticker):
    with open(ticker_to_path(ticker), 'rb') as pickle_file:
        return pickle.load(pickle_file)


def print_data(model, x, y, max_val):
    predictions = model(x).numpy()

    y_len = y.shape[0]
    predictions = predictions.reshape(y_len) * max_val
    y = y * max_val
    y_prev = np.zeros(shape=(y_len))
    y_prev[1:] = y[:y_len - 1]
    y_prev[0] = y_prev[1]

    print('---------------------')
    temp = np.zeros(shape=(y_len, 5))
    up = (predictions - y_prev) > 0
    temp[:, 0] = up * (y - y_prev)
    temp[:, 1] = y_prev
    temp[:, 2] = predictions
    temp[:, 3] = y
    temp[:, 4] = (up - 1) * (y - y_prev)

    np.set_printoptions(precision=2, suppress=True, threshold=10000)
    print(temp)
    print('sum+ :', np.sum(temp[:, 0]))
    print('sum- :', np.sum(temp[:, 4]))
    print('y_len', y_len)
    print('up', up.sum())

    print('min', np.min(predictions))
    print('max_val', max_val)
    print('weights', model.weights)

    # test_loss, test_acc = model.evaluate(x, y)
    # print(test_loss, test_acc)
    model.summary()


def train():
    data = load('btgpln')
    x = data['prices']
    y = data['prices_to_predict']
    max_val = data['max_val']

    x *= max_val
    y *= max_val
    x = x[100:]
    y = y[100:]
    max_val = np.amax(x)
    x /= max_val
    y /= max_val

    # print(x, y, max_val)
    print(np.size(x), np.size(y))
    print(x.shape, y.shape)
    assert x.shape[0] == y.shape[0]
    trin_multiply = 0.6
    train_size = int(trin_multiply * x.shape[0])
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # model = tf.keras.models.Sequential([
    #     tf.keras.layers.Dense(units=11, activation='relu'),
    #     # tf.keras.layers.Dropout(0.2),
    #     tf.keras.layers.Dense(units=1),
    # ])
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(x.shape[1],)))
    model.add(tf.keras.layers.Dense(
        units=8,
        activation=tf.keras.layers.Activation('relu'),
        kernel_initializer=tf.keras.initializers.RandomUniform(minval=0.05, maxval=0.1)
        # kernel_constraint=tf.keras.constraints.min_max_norm(
        #     min_value=0.0, max_value=0.1, rate=1.0, axis=0
        # )
    ))
    # model.add(tf.keras.layers.Dropout(0.1))
    model.add(tf.keras.layers.Dense(
        units=1,
        # kernel_constraint=tf.keras.constraints.MinMaxNorm(min_value=0.0, max_value=0.3),
        # kernel_constraint=tf.keras.constraints.NonNeg(),
        kernel_initializer=tf.keras.initializers.RandomUniform(minval=0.03, maxval=0.2, seed=None),
    ))


    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=['accuracy'],
    )
    model.fit(
        x_train,
        y_train,
        batch_size=16,
        epochs=50,
    )


    print_data(model, x_train, y_train, max_val)
    print('--------------------====================================------------------------')
    print_data(model, x_test, y_test, max_val)


train()
