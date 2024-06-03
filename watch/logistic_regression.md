# Logistic Regression

## Introduction

The logistic regression algorythm is the most popular supervised machine learning classifier model. The idea behind it is two fit the data with a linear modelisation.
This model could be either binary or multinomial.  

### How it works ?

The main goal is to set the data in a 2D plan, then to squish all the values between 0 & 1, to obtain then a probability.  
To predict values, the model will create linear function with the following format :  
y = wx + b, where w is the weight & b the bias  
When all the values are predicted, we squish them with a sigmoid function to keep a value between 0 & 1. If the value is superior or inferior to a threshold, it will be labelized either as 0 or 1.  
To optimized weight & bias, the model have inner méthods as the loss function to calculate as far are the predicted values to the real one.  

### The fit method

The ```fit``` method is the function that calculate self.weight & self.bias over a dataframe fit. They are optimized that way :
- Init the weight, bias & losses attributes
- Normalize the dataframe & reshape target values

Repeat the following code with some iterations & slices of the dataframe (batch) :
- Calculate the hypothesis (probabilities) of the batch
- Calculate the partial derivatives (with gradient batch) of the dataframe, target_values & the hypothesis
- Adjust the weight & bias with the partial derivatives
- Add the loss function in losses

After that, the weight & bias are optimally calculated.

### The predict method 

The ```predict``` method is simply the hypothesis of values with the model's bias & model's weight. If the predicted value is >= threshold than it's labelized at 1, otherwise it is labelized as 0.  
the ```predict_proba``` only return the hypothesis of values

### Why use Logistic Regression ?

The main pros are : 
- The interpretability : As a linear correlation, it is easy to understand the model with a specific feature.
- The sturdiness : Thanks to its simplicity, the logistic regression still works with poorly prepared data.
- Fast and inexpensive : As a simple function, logistic regression is very fast and inexpensive.

The main cons are :
- Sensible to outliers