# Mini AlphaGo

**Mini AlphaGo** is a simple implementation of deep learning for playing some board games such as Go and Tic-Tac-Toe. This was created for educational purposes and used in some classes at KAIST from 2016 to 2019. This software is provided as is. Only the value network is implemented and the greedy policy is used while playing. Although we do not use any policy network, the performance can be improved as we go through training iterations. This is similar to the policy improvement mechanism in AlphaGo Zero. As in AlphaGo Zero, we start from a pure random policy without using any game records. Some simplifications to the rules of Go are also made.

Tensorflow >= 1.12.0 and python >=3.5 were assumed in the code. If you use tensorflow 2.x, then you need the following in all *.py codes:
```python
import tensorflow.compat.v1 as tf  # this replaces "import tensorflow as tf"
tf.disable_v2_behavior()
```

## Files
* boardgame.py: game environments (Go, Tic-Tac-Toe, Othello, and Omok) and GUI for playing games interactively
* go_train.py: trains value networks for Go and tests them
* go_interactive.py: plays Go between a human and a neural network
* go_test_players.py: plays games between two neural networks
* tictactoe_train.py: trains value networks to play tic-tac-toe and tests them.
* tictactoe_interactive.py: plays tic-tac-toe between a human and a neural network

## Training and Testing
For training, run go_train.py. This will train two value networks in two iterations. They will be stored as ./go_gen0.ckpt and ./go_gen1.ckpt. The second one should perform better.

To play interactive games between a human and a trained value network, do the following:

```bash
python3 go_interactive.py ./go_gen1.ckpt
```

To play games between two neural networks ./go_gen0.ckpt and ./go_gen1.ckpt, do the following:

```bash
python3 go_test_players.py
```

It will play the following four games and show result for each game.
* ./go_gen0.ckpt (black) vs. ./go_gen0.ckpt (white)
* ./go_gen0.ckpt (black) vs. ./go_gen1.ckpt (white)
* ./go_gen1.ckpt (black) vs. ./go_gen1.ckpt (white)
* ./go_gen1.ckpt (black) vs. ./go_gen0.ckpt (white)
