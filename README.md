# Architectural Synthesis for Machine Learning Models

This project has been developed for educational purposes during the course Advanced Computing Architectures at the University of Trento (MSc in Computer Science). 

The aim of the project was to perform architectural synthesis applied to a machine learning task. We selected convolutional neural networks as a target, since they are simply formed by summations and multiplications. We broke the problem in two different steps: construction of the computational graph and development of scheduling and binding algorithms (in a resource unconstrained and constrained scenario). We implemented two unconstrained scheduling algorithms: asap and alap, and one heuristic constrained resource scheduling algorithm: LIST_L. 

To verify that the algorithms were correct, we also implemented the construction of computational graphs from simple mathematical formulas, which are more understandable, and proposed examples of the execution of the algorithms.

Of course, a lot of improvements could be done. For instance, in the case of convolutional networks we reported the simplifying choice of creating a new node even when a value is sure to be reused. This causes the associated register to be set free and then to require another access to memory. Another thing that could be done given more time is more on the engineering part: a more user-friendly way to set the parameters instead of setting up the parameters in the code could be nice.

### Execution

One can run the simplified version of the software in which the computational graph is created by a simple mathematical formula by simply running:

```console
python run_simple_formula.py
```

And can run the convolutional neural network version by running:

```console
python run_convolution.py
```

### Parameters

The runnable files are easily customizable and changing the parameters (i.e., change the availability of the resources or change the input) is really easy.


### Dependancies

Just Numpy.

