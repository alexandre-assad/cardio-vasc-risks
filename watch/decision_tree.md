# Decision tree

## Introduction

As easy to explain as understand, the decision tree algorythm is a very popular machine learning model that can easily be associated with human decision-making process.  
![exemple-decision-tree-looklike](./screenshots/decision_tree_shape.png)

## How it works 

### Basic function

The main ideas are : 
- to divide your data into serveral distinct regions.  
For exemple one region could be people taller than 170cm and with a weight superior at 80kgs, and another will be same weight with 180cm tall, etc...
- to predict the most common label for each region at the leaf of the tree  

### Our custom decision tree function

*(For a better understanding, do not hesitate to read the model's docstrings)*  
They are two main public methods in the model : 
- the ```fit``` method : to optimize class parameters according to the input supervised dataframe  
- the ```predict``` method : To predict labels from an unlabelized dataframe

Basiquely, the ```fit``` method will create a Tree, and the ```predict``` method will traverse the tree newly created to find the most probable label.  
*** 
#### Fit method
The main idea is the following one : "For enough feature with a maximum depth, it will create split of two that separe the best the feature with different label."