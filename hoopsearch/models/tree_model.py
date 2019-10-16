'''
    Created on Thur September  18 2019

    @author danie

    train a decision tree model to predict the most descriptive sentence of a
    given game article.  That sentence will be ultimately be presented to the
    user as a summary of the game.
'''

from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn import pipeline
import joblib
import pandas as pd
import numpy as np
import ast
from hoopsearch.common.constants import TREE_MODEL_PATH, Xy_DATA_PATH


if __name__ == "__main__":

    Xy_df = pd.read_csv(Xy_DATA_PATH, index_col=0)

    X_temp = Xy_df['0'].tolist()

    X = []

    for x in X_temp:
        X.append(ast.literal_eval(x))

    y = Xy_df['1'].tolist()

    X = np.array(X)

    tree = DecisionTreeClassifier()
    tree.fit(X,y) 

    joblib.dump(tree,TREE_MODEL_PATH)


