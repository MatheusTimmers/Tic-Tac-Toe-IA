import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import csv
from shared import *

X_train = []
y_train = [] 

with open('data/tic-tac-toe.data', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        row_data = parse_line(row)
        print(row_data)
        X_train.append(row_data[:-1])  
        y_train.append(row_data[-1])

k = 4  
knn = KNeighborsClassifier(n_neighbors=k)

# Train the classifier
knn.fit(X_train, y_train)


X_test = np.array([parse_line('xxxbbbbbb')]) 

# Predict the outcome for the test game state
prediction = knn.predict(X_test)

print(f"Predicted outcome: {parse_to_str(prediction[0])}")