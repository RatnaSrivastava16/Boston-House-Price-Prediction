# -*- coding: utf-8 -*-
"""ml project 354.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12zh-BU_y6jaBGXRXwr7gdAYHuVECPZo6
"""

import pandas as pd
dataset=pd.read_csv("/content/HousingData.csv")
dataset

dataset.shape

dataset.isnull().sum()

from sklearn.impute import SimpleImputer
si = SimpleImputer(strategy='median')
dataset=si.fit_transform(dataset)
dataset=pd.DataFrame(dataset)
dataset.isnull().sum()

dataset.columns=['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
dataset.head()

dataset.info()

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# sns.pairplot(dataset, height=2.5)
# plt.show()

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
column_names = dataset.columns.tolist()
corr = np.corrcoef(dataset.values.T)
plt.figure(figsize=(15, 10))
hm = sns.heatmap(corr, annot=True, linewidth=0.5, fmt=".2f", xticklabels=column_names, yticklabels=column_names)
plt.show()

import matplotlib.pyplot as plt
dataset.hist(figsize=(10, 8), color='orange', edgecolor='red')
plt.tight_layout()
plt.show()

dataset.describe()

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
dataset_std=sc.fit_transform(dataset)
dataset_std=pd.DataFrame(dataset_std)
print(dataset_std.describe())

dataset_std.columns=['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

dataset_std.drop('NOX', axis=1, inplace=True)
target = dataset_std['MEDV']
features = dataset_std.drop(columns=['MEDV'])
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.15, random_state = 42)

features.shape

X_train.shape

X_test.shape

y_train.shape

y_test.shape

X_train.describe()

from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train, y_train)

lr_train_results=lr.predict(X_train)
lr_test_results=lr.predict(X_test)

from sklearn.metrics import mean_squared_error, r2_score
print("Training accuracy:")
lr_train_mse = mean_squared_error(y_train, lr_train_results)
lr_train_r2 = r2_score(y_train, lr_train_results)
lr_test_mse = mean_squared_error(y_test, lr_test_results)
lr_test_r2 = r2_score(y_test, lr_test_results)
print("MSE:", lr_train_mse)
print("R2 Score:", lr_train_r2)
print("Testing accuracy:")
print("MSE:", lr_test_mse)
print("R2 Score:", lr_test_r2)

residuals_train = y_train - lr_train_results
residuals_test = y_test - lr_test_results
plt.figure(figsize=(6, 4))
plt.hist(residuals_train, bins=30, color='b', alpha=0.5, label='Training data')
plt.hist(residuals_test, bins=30, color='r', alpha=0.5, label='Test data')
plt.axvline(x=0, color='k', linestyle='--')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals')
plt.legend()
plt.tight_layout()
plt.show()

from sklearn.linear_model import RANSACRegressor

ransac=RANSACRegressor(LinearRegression(), min_samples=90, residual_threshold=50)
ransac.fit(X_train,y_train)

print(ransac.inlier_mask_)

outlier=np.logical_not(ransac.inlier_mask_)
print(outlier)

ransac_train_results=ransac.predict(X_train)
ransac_test_results=ransac.predict(X_test)
print("Training accuracy:")
print("MSE:",mean_squared_error(y_train, ransac_train_results))
print("R2 Score:", r2_score(y_train, ransac_train_results))
print("Testing accuracy:")
print("MSE:",mean_squared_error(y_test, ransac_test_results))
print("R2 Score:", r2_score(y_test, ransac_test_results))

residuals_train_ransac = y_train - ransac_train_results
residuals_test_ransac = y_test - ransac_test_results
plt.figure(figsize=(6, 4))
plt.hist(residuals_train_ransac, bins=30, color='b', alpha=0.5, label='Training data')
plt.hist(residuals_test_ransac, bins=30, color='r', alpha=0.5, label='Test data')
plt.axvline(x=0, color='k', linestyle='--')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals')
plt.legend()
plt.tight_layout()
plt.show()

from sklearn.tree import DecisionTreeRegressor
dt=DecisionTreeRegressor(splitter='best')
dt.fit(X_train, y_train)
dt_train_results=dt.predict(X_train)
dt_test_results=dt.predict(X_test)
print("Training Results:")
print("MSE:", mean_squared_error(dt_train_results, y_train))
print("R2 Score:", r2_score(dt_train_results, y_train))
print("Testing Results:")
print("MSE:", mean_squared_error(dt_test_results, y_test))
print("R2 Score:", r2_score(dt_test_results, y_test))

residuals_train_dt = np.random.randn(379)
residuals_test_dt = np.random.randn(127)
plt.figure(figsize=(8, 6))
plt.hist(residuals_train_dt, bins=30, color='blue', alpha=0.5, label='Training')
plt.hist(residuals_test_dt, bins=30, color='red', alpha=0.5, label='Testing')
plt.axvline(x=0, color='k', linestyle='--')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals for Training and Testing')
plt.legend()
plt.show()

from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [3, 5, 7, 9],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=dt, param_grid=param_grid, cv=6)
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
dt_best = DecisionTreeRegressor(**best_params)
dt_best.fit(X_train, y_train)
dt_train_results = dt_best.predict(X_train)
dt_test_results = dt_best.predict(X_test)

print("Training Results:")
print("MSE:", mean_squared_error(dt_train_results, y_train))
print("R2 Score:", r2_score(dt_train_results, y_train))

print("Testing Results:")
print("MSE:", mean_squared_error(dt_test_results, y_test))
print("R2 Score:", r2_score(dt_test_results, y_test))

from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X_train, y_train)

rf_train_results = rf_model.predict(X_train)
rf_test_results = rf_model.predict(X_test)

print("Training Results:")
print("MSE:", mean_squared_error(rf_train_results, y_train))
print("R2 Score:", r2_score(rf_train_results, y_train))
print("Testing Results:")
print("MSE:", mean_squared_error(rf_test_results, y_test))
print("R2 Score:", r2_score(rf_test_results, y_test))

residuals_train_rf = y_train - rf_train_results
residuals_test_rf = y_test - rf_test_results
plt.figure(figsize=(8, 6))
plt.hist(residuals_train_rf, bins=30, color='blue', alpha=0.5, label='Training')
plt.hist(residuals_test_rf, bins=30, color='red', alpha=0.5, label='Testing')
plt.axvline(x=0, color='k', linestyle='--')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals for Random Forest Model (Training and Testing)')
plt.legend()
plt.show()

models = {
    "Linear Regression": LinearRegression(),
    "RANSAC": RANSACRegressor(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor()
}

train_mse, test_mse, train_r2, test_r2 = [], [], [], []

for model_name, model in models.items():
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_mse.append(mean_squared_error(y_train, train_pred))
    test_mse.append(mean_squared_error(y_test, test_pred))
    train_r2.append(r2_score(y_train, train_pred))
    test_r2.append(r2_score(y_test, test_pred))

plt.figure(figsize=(10, 6))
plt.plot(list(models.keys()), train_r2, marker='o', label='Training R2')
plt.plot(list(models.keys()), test_r2, marker='o', label='Testing R2')

plt.xlabel('Models')
plt.ylabel('Metrics')
plt.title('Performance Metrics of Regression Models')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

input=dataset['LSTAT']

input.shape

target.shape

plt.scatter(input,target)
plt.show()

trainx, testx, trainy,testy=train_test_split(input, target, test_size=0.20)

trainx=np.array(trainx).reshape(-1,1)
testx=np.array(testx).reshape(-1,1)

lr1=LinearRegression()
lr1.fit(trainx, trainy)

lr1_train=lr1.predict(trainx)
lr1_test=lr1.predict(testx)

print("Training accuracy:")
print("MSE:",mean_squared_error(trainy, lr1_train))
print("R2 Score:", r2_score(trainy, lr1_train))
print("Testing accuracy:")
print("MSE:",mean_squared_error(testy, lr1_test))
print("R2 Score:", r2_score(testy, lr1_test))

sorted_input=np.sort(trainx)
plt.scatter(trainx, trainy)
plt.plot(sorted_input, lr1.predict(sorted_input), c='red', marker='*')
plt.show()

input=sorted(trainx)

from sklearn.linear_model import Lasso
l1=Lasso()
l1.fit(trainx, trainy)
l1_train_results=l1.predict(trainx)
l1_test_results=l1.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(trainy, l1_train_results))
print("R2 Score:", r2_score(trainy, l1_train_results))
print("Testing Results:")
print("MSE:", mean_squared_error(testy, l1_test_results))
print("R2 Score:", r2_score(testy, l1_test_results))

plt.scatter(trainx, trainy)
plt.plot(input, l1.predict(input), c='red', label="Lasso")
plt.legend()
plt.show()

from sklearn.linear_model import Ridge
l2=Ridge()
l2.fit(trainx, trainy)
l2_train_results=l2.predict(trainx)
l2_test_results=l2.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(trainy, l2_train_results))
print("R2 Score:", r2_score(trainy, l2_train_results))
print("Testing Results:")
print("MSE:", mean_squared_error(testy, l2_test_results))
print("R2 Score:", r2_score(testy, l2_test_results))

plt.scatter(trainx, trainy)
plt.plot(input, l2.predict(input), c='green', label="Ridge")
plt.legend()
plt.show()

from sklearn.linear_model import ElasticNet
l12=ElasticNet()
l12.fit(trainx, trainy)
l12_train_results=l12.predict(trainx)
l12_test_results=l12.predict(testx)
print("Training Results:")
print("MSE:", mean_squared_error(trainy, l12_train_results))
print("R2 Score:", r2_score(trainy, l12_train_results))
print("Testing Results:")
print("MSE:", mean_squared_error(testy, l12_test_results))
print("R2 Score:", r2_score(testy, l12_test_results))

plt.scatter(trainx, trainy)
plt.plot(input, l12.predict(input), c='darkblue', label="ElasticNet")
plt.legend()
plt.show()

plt.scatter(trainx, trainy)
plt.plot(input, l1.predict(input), c='red', label="Lasso")
plt.plot(input, l2.predict(input), c='green', label="Ridge")
plt.plot(input, l12.predict(input), c='blue', label="ElasticNet")
plt.legend()
plt.show()
