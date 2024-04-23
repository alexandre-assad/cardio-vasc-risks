from dataclasses import dataclass, field
from typing import Tuple
from numpy import array, dot, floating, log, mean, ndarray, exp, sum, zeros
from sklearn.datasets import make_moons


@dataclass
class CustomLogisticRegression:
    _threshold: float = 0.5
    _weight: ndarray = field(default_factory=lambda: zeros((1, 1)))
    _bias: float = 0.0
    _losses: list = field(default_factory=list)

    def _sigmoid_transform(self, value: float) -> float:
        """
        To return a hypotesis (self._hypothesis) between 0 & 1, logistic regressor need to apply a sigmoid_transformation to squished value in this range

        Input : value, int : the value which will be "squished"
        Output : int, the squished value
        Mathematic expression : f(x) = 1 / (1 + e^-x)
        """
        return 1 / (1 + exp(-value))

    def _hypotesis(self, weight: ndarray, bias: float, dataframe: ndarray) -> float:
        """
        
        """
        return self._sigmoid_transform(dot(dataframe, weight) + bias)

    def _lost_function(self, target_values: ndarray, hypothesis: float) -> float:
        return -mean(
            target_values * (log(hypothesis))
            - (1 - target_values) * log(1 - hypothesis)
        )

    def _gradient_calc(
        self, dataframe: ndarray, target_value: ndarray, hypothesis: float
    ) -> Tuple[float, float]:

        number_observations = dataframe.shape[0]

        lost_partial_derivative_weight = (1 / number_observations) * dot(
            dataframe.T, (hypothesis - target_value)
        )
        lost_partial_derivative_bias = (1 / number_observations) * sum(
            hypothesis - target_value
        )

        return lost_partial_derivative_weight, float(lost_partial_derivative_bias)

    def _normalize_dataframe(self, dataframe: ndarray) -> ndarray:

        _, number_features = dataframe.shape

        for _ in range(number_features):
            dataframe = dataframe - dataframe.mean(axis=0) / dataframe.std(axis=0)

        return dataframe

    def fit(
        self,
        dataframe: ndarray,
        target_values: ndarray,
        batch_size: int = 0,
        epochs: int = 0,
        learning_rate: float = 0,
    ) -> None:

        number_observations, number_features = dataframe.shape

        self._weight = zeros((number_features, 1))
        self._bias = 0.0
        self._losses = []

        target_values = target_values.reshape(number_observations, 1)
        dataframe = self._normalize_dataframe(dataframe)

        for _ in range(epochs):  # TODO really appropriate this part & naming
            for batch in range((number_observations - 1) // batch_size + 1):

                start_of_batch = batch * batch_size
                end_of_batch = start_of_batch + batch_size
                dataframe_by_batch = dataframe[start_of_batch:end_of_batch]
                target_values_by_batch = target_values[start_of_batch:end_of_batch]

                hypothesis = self._hypotesis(
                    self._weight, self._bias, dataframe_by_batch
                )
                partial_derivative_weight, partial_derivative_bias = (
                    self._gradient_calc(
                        dataframe_by_batch, target_values_by_batch, hypothesis
                    )
                )

                self._weight -= learning_rate * partial_derivative_weight
                self._bias -= learning_rate * partial_derivative_bias

            self._losses.append(
                self._lost_function(
                    target_values, self._hypotesis(self._weight, self._bias, dataframe)
                )
            )

    def predict(self, dataframe: ndarray) -> ndarray:

        dataframe = self._normalize_dataframe(dataframe)
        predictions = self._hypotesis(self._weight, self._bias, dataframe)

        predictions_classified = [
            1 if prediction > self._threshold else 0 for prediction in predictions
        ]

        return array(predictions_classified)


def accuracy(y, y_hat):
    accuracy = sum(y == y_hat) / len(y)
    return accuracy


X, y = make_moons(n_samples=100, noise=0.24)
logistic_regressor = CustomLogisticRegression()
logistic_regressor.fit(X, y, batch_size=100, epochs=1000, learning_rate=0.01)
print(accuracy(y, logistic_regressor.predict(X)))
