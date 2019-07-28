from Game import *


if __name__ == '__main__':
    G = Game()
    NN = NeuralNetwork()
    data = G.generate_population(None)
    dummy_model = NN.create_dummy_model(data)
    train_model = NN.train_model(data, dummy_model)
    G.eval(train_model)
