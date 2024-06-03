# Cardio Vasc Risks

This project is a simple demonstration of how to use logistic regression to predict cardio vascular risks based on various features. The project is structured as follows:

- [`analysis/`](analysis/): Contains Jupyter notebooks for generating various charts. Data Treatment, and processing
- [`data/`](data/): Contains the raw data used in the project. With a slight attempt of applying DVC.
- [`logistic_regression/`](logistic_regression/): Contains Python scripts for running our logistic regression.
- [`models/`](models/): 

## How to Run

1. Install the required Python packages:

```sh
git clone https://github.com/alexandre-assad/cardio-vasc-risks.git
cd cardio-vasc-risk
poetry install
```

2. Run the Jupyter notebooks in the [`analysis/`](analysis/) directory:

```sh   
jupyter notebook analysis/cleaning.ipynb
jupyter notebook notebooks/cateorical_viz.ipynb
```

1. Run the Model in the [`logistic_regression/`](logistic_regression/) directory:

```sh
jupyter predict/prediction.ipynb
```

## 