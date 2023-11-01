import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        PerModel = PerceptronModel.run(self, x)
        if nn.as_scalar(PerModel) < 0:
            return -1
        return 1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        loop = 1
        while loop:
            loop = 0
            batchSize = 1
            for x, y in dataset.iterate_once(batchSize):
                if self.get_prediction(x) != nn.as_scalar(y):
                    loop = 1
                    self.w.update(x,nn.as_scalar(y))       

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        self.batchSize = 200
        self.learningRate = -0.05
        
        # Weight Parameters
        self.w1 = nn.Parameter(1, 128)
        self.w2 = nn.Parameter(128, 32)
        self.w3 = nn.Parameter(32, 1)
        
        # Bias Parameters
        self.b1 = nn.Parameter(1, 128)
        self.b2 = nn.Parameter(1, 32)
        self.b3 = nn.Parameter(1, 1)
        
        # All Parameters
        self.all_params = [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3]
        
    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batchSize x 1)
        Returns:
            A node with shape (batchSize x 1) containing predicted y-values
        """
        layerone = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        layertwo = nn.ReLU(nn.AddBias(nn.Linear(layerone, self.w2), self.b2))
        return nn.AddBias(nn.Linear(layertwo, self.w3), self.b3)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batchSize x 1)
            y: a node with shape (batchSize x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        loss = float('inf')
        while loss > 0.02:
            for x, y in dataset.iterate_once(self.batchSize):
                loss = nn.as_scalar(self.get_loss(x, y))
                for i in range(len(self.all_params)):
                    self.all_params[i].update(nn.gradients(self.get_loss(x, y), self.all_params)[i], self.learningRate)
                        
class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
 
        self.batch_size = 100
        self.learning_rate = -0.5
        
        # # Weight Parameters
        self.weight1 = nn.Parameter(784, 49)
        self.weight2 = nn.Parameter(49, 98)
        self.weight3 = nn.Parameter(98, 10)
        
        # # Bias Parameters
        self.bias1 = nn.Parameter(1, 49)
        self.bias2 = nn.Parameter(1, 98)
        self.bias3 = nn.Parameter(1, 10)
        
        #self.all_params = [self.weight1, self.bias1, self.weight2,  self.bias2, self.weight3, self.bias3]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batchSize x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batchSize x 784)
        Output:
            A node with shape (batchSize x 10) containing predicted scores
                (also called logits)
        """
        layerone = nn.ReLU(nn.AddBias(nn.Linear(x, self.weight1), self.bias1))
        layertwo = nn.ReLU(nn.AddBias(nn.Linear(layerone, self.weight2), self.bias2))
        return nn.AddBias(nn.Linear(layertwo, self.weight3), self.bias3)


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batchSize x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batchSize x 784)
            y: a node with shape (batchSize x 10)
        Returns: a loss node
        """
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        while dataset.get_validation_accuracy() < 0.97:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients(loss, [self.weight1, self.weight2, self.weight3, self.bias1, self.bias2, self.bias3])
                self.weight1.update(gradients[0], self.learning_rate)
                self.weight2.update(gradients[1], self.learning_rate)
                self.weight3.update(gradients[2], self.learning_rate)
                self.bias1.update(gradients[3], self.learning_rate)
                self.bias2.update(gradients[4], self.learning_rate)
                self.bias3.update(gradients[5], self.learning_rate)

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        self.batchSize = 10
        self.learning_rate = -0.1
        
        # Weight Parameters 
        self.weight1 = nn.Parameter(self.num_chars, 256)
        self.weight2 = nn.Parameter(256, 256)
        self.weight3 = nn.Parameter(256, 5)
        
        # Bias Parameters 
        self.bias1 = nn.Parameter(1, 256)
        self.bias2 = nn.Parameter(1, 256)
        self.bias3 = nn.Parameter(1, 5)
        
        # All Parameters 
        self.all_params = [self.weight1, self.weight2, self.weight3, self.bias1, self.bias2, self.bias3]

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batchSize x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batchSize x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batchSize x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batchSize x self.num_chars)
        Returns:
            A node with shape (batchSize x 5) containing predicted scoress
                (also called logits)
        """
        onehotvector = nn.Linear(nn.DataNode(xs[0].data), self.weight1)
        for x in xs:
            onehotvector = nn.ReLU(nn.AddBias(nn.Linear(nn.Add(nn.Linear(x, self.weight1), onehotvector), self.weight2), self.bias2))
        return nn.AddBias(nn.Linear(onehotvector, self.weight3), self.bias3)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batchSize x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batchSize x self.num_chars)
            y: a node with shape (batchSize x 5)
        Returns: a loss node
        """
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        batch_size = 100
        while dataset.get_validation_accuracy() < 0.85:
            for x, y in dataset.iterate_once(batch_size):
                gradients = nn.gradients(self.get_loss(x, y), self.all_params)
                for i in range(len(self.all_params)):
                    self.all_params[i].update(gradients[i], self.learning_rate)
