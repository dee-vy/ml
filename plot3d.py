import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

# All the scores mentioned below are for banana crop for now.

df_train = pd.read_csv("train_" + "Banana.csv")
df_test = pd.read_csv("test_" + "Banana.csv")
df_train = df_train.dropna()
df_test = df_test.dropna()
label = "Banana Crop"

X_train_original = df_train[['Temperature', 'Rainfall']]
y_train = df_train[['Produce']]

X_test_original = df_test[['Temperature', 'Rainfall']]
y_test = df_test[['Produce']]

X1_train = X_train_original.iloc[:, 0]
X2_train = X_train_original.iloc[:, 1]
X_train = np.column_stack((X1_train, X2_train))

X1_test = X_test_original.iloc[:, 0]
X2_test = X_test_original.iloc[:, 1]
X_test = np.column_stack((X1_test, X2_test))

# >>Original features with RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, y_train.values.ravel())
yPred = model.predict(X_test)  # Score: MSE: 29.79 RMSE: 5.46 r2: 0.87

# >>Polynomial features with RandomForestRegressor
# 1. Three features
# X3 = X1_train * X2_train
# X_train = np.column_stack((X1_train, X2_train, X3))
# X3_test = X1_test * X2_test
# X_test = np.column_stack((X1_test, X2_test, X3_test))  # Score: MSE: 29.89 RMSE: 5.47 r2: 0.87

# 2. Square
# X1_train = X1_train * X1_train
# X2_train = X2_train * X2_train
# X_train = np.column_stack((X1_train, X2_train))
# X1_test = X1_test * X1_test
# X2_test = X2_test * X2_test
# X_test = np.column_stack((X1_test, X2_test))  # Score: MSE: 29.95 RMSE: 5.47 r2: 0.87

# Model
# model = RandomForestRegressor()
# model.fit(X_train, y_train.values.ravel())
# yPred = model.predict(X_test)

# >>Original features with knn
# y_train = y_train.astype(int)
# model = KNeighborsClassifier(n_neighbors=20).fit(X_train, y_train.values.ravel())
# yPred = model.predict(X_test)  # Very Bad. Score: MSE: 200.32 RMSE: 14.15 r2: 0.11

# >>Polynomial features with knn
# X3 = X1_train * X2_train
# X_train = np.column_stack((X1_train, X2_train, X3))
# X3_test = X1_test * X2_test
# X_test = np.column_stack((X1_test, X2_test, X3_test))
# y_train = y_train.astype(int)
# model = KNeighborsClassifier(n_neighbors=20).fit(X_train, y_train.values.ravel())
# yPred = model.predict(X_test)  # Very Bad. Score: MSE: 313.43 RMSE: 17.70 r2: -0.39

# >>Original features with Lasso (Bad)
# model = Lasso(alpha=1 / (2 * 5))  # C=5 from lasso.py
# model.fit(X_train, y_train)
# yPred = model.predict(X_test)  # Score: MSE: 131.83 RMSE: 11.48 r2: 0.42

# >>Polynomial features with Lasso (Equally Bad)
# X3 = X1_train * X2_train
# X_train = np.column_stack((X1_train, X2_train, X3))
# X3_test = X1_test * X2_test
# X_test = np.column_stack((X1_test, X2_test, X3_test))
# model = Lasso(alpha=1 / (2 * 5))  # C=5
# model.fit(X_train, y_train)
# yPred = model.predict(X_test)  # Score: MSE: 131.53 RMSE: 11.47 r2: 0.42

# Plots
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title(label)
ax.scatter(X1_train, X2_train, y_train, color='black', label="Features")
ax.set_xlabel("Temperature")
ax.set_ylabel("Rainfall")
ax.set_zlabel("Produce")
predicted_val = ax.plot_trisurf(X_test[:, 0], X_test[:, 1], yPred, color='red', label="Predictions")
predicted_val._facecolors2d = predicted_val._facecolor3d
predicted_val._edgecolors2d = predicted_val._edgecolor3d
plt.legend(loc="best")
plt.show()

# Scores
# print(model.score(X_test, y_test))
print("Mean squared error: %.2f" % mean_squared_error(y_test, yPred))
print("Root mean squared error: %.2f" % sqrt(mean_squared_error(y_test, yPred)))
print("r2 square: %.2f" % r2_score(y_test, yPred))
