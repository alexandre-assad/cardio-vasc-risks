from dataclasses import dataclass, field
from typing import Callable, Tuple, TypeAlias
from numpy import array, dot, log, mean, ndarray, exp, sum, zeros

class CustomLogisticRegression:

    def __init__(self, threshold = 0.5) -> None:
        self.threshold: float = threshold
        self.__weight: ndarray = field(default_factory=lambda: zeros((1, 1)))
        self.__bias: float = 0.0
        self.__losses: list = []

    
    def _sigmoid_transform(self, values: ndarray) -> ndarray:
        """
        To return a hypotesis (self._hypothesis) between 0 & 1, logistic regressor need to apply a sigmoid_transformation to squished value in this range. It will apply
        the sigmoid transformation to all the values of the array

        Input :
            value, ndarray : the matrix of value which will be "squished"
        Output :
            ndarray, the matrix of squished value
        Mathematic expression :
            f(x) = 1 / (1 + e^-x)
        """
        return 1 / (1 + exp(-values))

    def _hypotesis(self, weight: ndarray, bias: float, dataframe: ndarray) -> ndarray:
        """
        the hypothesis are the probability between 0 and 1. In a binary classification context, it is the probability to be classified as 1.
        It will be the sigmoid transformation of the dataset dot the weight with the bias add at the end.

        Input :
            dataframe : ndarray, the matrix of values of the dataframe
            weight : ndarray, the matrix of weight to be apply to the dataframe
            bias: float, the bias to be added at the dot calc
        Output :
            ndarray, the values of the sigmoid transformations of the inputs
        Mathematic expression :
            f(x) = s((X . w) + b)
        """
        return self._sigmoid_transform(dot(dataframe, weight) + bias)

    def _lost_function(self, target_values: ndarray, hypothesis: ndarray) -> float:
        """
        In the logistic regressor, the lost function or cost function is a mesure of how much the predictions differs from the labels.
        We use the binary cross entropy for this lost function.

        Input:
            target_values, ndarray: the matrix of the labels
            hypothesis, ndarray : the matrix of the predicted values
        Output:
            float : the mesure of how much the predictions differs from the labels
        Mathematic expression : - 1/m * S(m, i)[(yi * log(ŷi) + (1 - yi) * log(1 - ŷi))]
        """
        return float(
            -mean(
                target_values * (log(hypothesis))
                - (1 - target_values) * log(1 - hypothesis)
            )
        )

    def _gradient_calc(
        self, dataframe: ndarray, target_value: ndarray, hypothesis: ndarray
    ) -> Tuple[float, float]:
        """
        In a gradient descent context, to find the optimal weight and bias, we need for each gradient to calculate two partial derivatives (for weight & bias).

        Input :
            dataframe, ndarray : the matrix of the values of the dataframe
            target_values, ndarray : the matrix of the labels
            hypothesis, ndarray : the matrix of the predicted values
        Output :
            Tuple[float, float] : the partial derivate of weight, partial derivate of bias
        Mathematic expression :
            dw = (1 / m) * (X.T . (ŷ - y))
            db = (1 / m) * (s(ŷ - y))
        """
        number_observations = dataframe.shape[0]

        lost_partial_derivative_weight = (1 / number_observations) * dot(
            dataframe.T, (hypothesis - target_value)
        )
        lost_partial_derivative_bias = (1 / number_observations) * sum(
            hypothesis - target_value
        )

        return lost_partial_derivative_weight, float(lost_partial_derivative_bias)

    def _normalize_dataframe(self, dataframe: ndarray) -> ndarray:
        """
        To get acceptable lost function values, we need to normalize our dataset.
        Input :
            dataframe, ndarray : the matrix of the values of the dataframe
        Output :
            ndarray : the matrix of the normalized values of the dataframe
        Mathematic expression :
            for each feature n : X(n) = X(n) - mean(X(n)) / standart deviation(X(n))
        """
        _, number_features = dataframe.shape

        for _ in range(number_features):
            dataframe = dataframe - dataframe.mean(axis=0) / dataframe.std(axis=0)

        return dataframe

    def fit(
        self,
        dataframe: ndarray,
        target_values: ndarray,
        batch_size: int = 100,
        epochs: int = 1000,
        learning_rate: float = 0.01,
    ) -> None:
        """
        Method to fit the logistic regressor to the dataset. It will enables to find the optimal weight & bias for the classification.
        By iteratin epochs & batch, it will calculate the hypothesis and use gradient descent to optimize weight & bias.

        Input :
            dataframe, ndarray : the matrix of value of the dataset
            target_values, ndarray : the matrix of the labels
            batch_size (default 100), int: the size of the batch to divide the dataframe
            epochs (default 1000), int : the number of iterations of the entire dataframe
            learning_rate (default 0.01), float : the rate of gradient descent iteration
        Output : None
        """

        number_observations, number_features = dataframe.shape

        self.__weight = zeros((number_features, 1))
        self.__bias = 0.0
        self.__losses = []

        target_values = target_values.reshape(number_observations, 1)
        dataframe = self._normalize_dataframe(dataframe)

        for _ in range(epochs):
            for batch in range((number_observations - 1) // batch_size + 1):

                start_of_batch = batch * batch_size
                end_of_batch = start_of_batch + batch_size
                dataframe_by_batch = dataframe[start_of_batch:end_of_batch]
                target_values_by_batch = target_values[start_of_batch:end_of_batch]

                hypothesis = self._hypotesis(
                    self.__weight, self.__bias, dataframe_by_batch
                )
                partial_derivative_weight, partial_derivative_bias = (
                    self._gradient_calc(
                        dataframe_by_batch, target_values_by_batch, hypothesis
                    )
                )

                self.__weight -= learning_rate * partial_derivative_weight
                self.__bias -= learning_rate * partial_derivative_bias

            self.__losses.append(
                self._lost_function(
                    target_values, self._hypotesis(self.__weight, self.__bias, dataframe)
                )
            )

    def predict(self, dataframe: ndarray) -> ndarray:
        """
        Binary classification from a dataframe. It will calculate the hypothesis, and classify values if they are inferior or superior to the threshold.
        
        Input : 
            dataframe, ndarray : the matrix of the values from the dataframe
        Output :
            ndarray : the matrix of the predicted labels
        """
        dataframe = self._normalize_dataframe(dataframe)
        predictions = self._hypotesis(self.__weight, self.__bias, dataframe)

        predictions_classified = [
            1 if prediction > self.threshold else 0 for prediction in predictions
        ]

        return array(predictions_classified)
    

    def predict_proba(self, dataframe: ndarray) -> ndarray:
        """
        Probability from 0 to 1 to each observations of a dataframe to be classified as the label.

        Input :
            dataframe, ndarrar : the matrix of the values from the dataframe
        Output :
            ndarray : the matrix of probability to be labelized.
        """
        dataframe = self._normalize_dataframe(dataframe)
        return  array(self._hypotesis(self.__weight, self.__bias, dataframe))