﻿# EE807 Special Topics in EE <Deep Reinforcement Learning and AlphaGo>, Fall 2019
# Information Theory & Machine Learning Lab, School of EE, KAIST
#
# Revision history
# Originally written in Matlab by Sae-Young Chung in Apr. 2016
#   for EE405C Electronics Design Lab <Network of Smart Systems>, Spring 2016
# Python & TensorFlow porting by Wonseok Jeon, Narae Ryu, Hwehee Chung in Dec. 2016
#   for EE488C Special Topics in EE <Deep Learning and AlphaGo>, Fall 2016
# Revised by Sae-Young Chung, 2017/12/07
#   for EE488B Special Topics in EE <Deep Learning and AlphaGo>, Fall 2017
# Revised by Sae-Young Chung, 2018/12/01
#   for EE807B Special Topics in EE <Deep Reinforcement Learning and AlphaGo>, Fall 2018


import tensorflow as tf
import numpy as np
from boardgame import game1, game2, game3, game4, data_augmentation

# Choose game Go
game = game1()

### NETWORK ARCHITECTURE ###
def network(state, nx, ny):
    # Set variable initializers
    init_weight = tf.random_normal_initializer(stddev = 0.1)
    init_bias = tf.constant_initializer(0.1)

    # Create variables "weights1" and "biases1".
    weights1 = tf.get_variable("weights1", [3, 3, 3, 30], initializer = init_weight)
    biases1 = tf.get_variable("biases1", [30], initializer = init_bias)

    # Create 1st layer
    conv1 = tf.nn.conv2d(state, weights1, strides = [1, 1, 1, 1], padding = 'SAME')
    out1 = tf.nn.relu(conv1 + biases1)

    # Create variables "weights2" and "biases2".
    weights2 = tf.get_variable("weights2", [3, 3, 30, 50], initializer = init_weight)
    biases2 = tf.get_variable("biases2", [50], initializer = init_bias)

    # Create 2nd layer
    conv2 = tf.nn.conv2d(out1, weights2, strides = [1, 1, 1, 1], padding ='SAME')
    out2 = tf.nn.relu(conv2 + biases2)

    # Create variables "weights3" and "biases3".
    weights3 = tf.get_variable("weights3", [3, 3, 50, 70], initializer = init_weight)
    biases3 = tf.get_variable("biases3", [70], initializer = init_bias)

    # Create 3rd layer
    conv3 = tf.nn.conv2d(out2, weights3, strides = [1, 1, 1, 1], padding ='SAME')
    out3 = tf.nn.relu(conv3 + biases3)

    # Create variables "weights1fc" and "biases1fc".
    weights1fc = tf.get_variable("weights1fc", [nx * ny * 70, 100], initializer = init_weight)
    biases1fc = tf.get_variable("biases1fc", [100], initializer = init_bias)

    # Create 1st fully connected layer
    fc1 = tf.reshape(out3, [-1, nx * ny * 70])
    out1fc = tf.nn.relu(tf.matmul(fc1, weights1fc) + biases1fc)

    # Create variables "weights2fc" and "biases2fc".
    weights2fc = tf.get_variable("weights2fc", [100, 3], initializer = init_weight)
    biases2fc = tf.get_variable("biases2fc", [3], initializer = init_bias)

    # Create 2nd fully connected layer
    return tf.matmul(out1fc, weights2fc) + biases2fc


# Input (common for all networks)
S = tf.placeholder(tf.float32, shape = [None, game.nx, game.ny, 3], name = "S")

# temporary network for loading from .ckpt
scope = "network"
with tf.variable_scope(scope):
    # Estimation for unnormalized log probability
    Y = network(S, game.nx, game.ny) 
    # Estimation for probability
    P = tf.nn.softmax(Y, name = "softmax")

# network0 for black
# network1 for white
for i in range(2):
    scope = "network" + str(i)
    with tf.variable_scope(scope):
        # Estimation for unnormalized log probability
        Y = network(S, game.nx, game.ny) 
        # Estimation for probability
        P = tf.nn.softmax(Y, name = "softmax")

N_variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope = "network/")
N0_variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope = "network0/")
N1_variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope = "network1/")

### SAVER ###
saver = tf.train.Saver(N_variables)

with tf.Session() as sess:
    ### DEFAULT SESSION ###
    sess.as_default()

    ### VARIABLE INITIALIZATION ###
    sess.run(tf.global_variables_initializer())
    n_test = 1
    r_none = np.zeros((n_test))
    saver.restore(sess, "./go_gen0.ckpt")
    for i in range(len(N_variables)):
        sess.run(tf.assign(N0_variables[i], N_variables[i]))
    saver.restore(sess, "./go_gen1.ckpt")
    for i in range(len(N_variables)):
        sess.run(tf.assign(N1_variables[i], N_variables[i]))
    N0 = tf.get_default_graph().get_tensor_by_name("network0/softmax:0")
    N1 = tf.get_default_graph().get_tensor_by_name("network1/softmax:0")
    s = game.play_games(N0, r_none, N0, r_none, n_test, nargout = 1)
    win=s[0][0]; loss=s[0][1]; tie=s[0][2]
    print('net1 (black) against net1 (white): win %d, loss %d, tie %d' % (win, loss, tie))
    s = game.play_games(N0, r_none, N1, r_none, n_test, nargout = 1)
    win=s[0][0]; loss=s[0][1]; tie=s[0][2]
    print('net1 (black) against net2 (white): win %d, loss %d, tie %d' % (win, loss, tie))
    s = game.play_games(N1, r_none, N1, r_none, n_test, nargout = 1)
    win=s[0][0]; loss=s[0][1]; tie=s[0][2]
    print('net2 (black) against net2 (white): win %d, loss %d, tie %d' % (win, loss, tie))
    s = game.play_games(N1, r_none, N0, r_none, n_test, nargout = 1)
    win=s[0][0]; loss=s[0][1]; tie=s[0][2]
    print('net2 (black) against net1 (white): win %d, loss %d, tie %d' % (win, loss, tie))

