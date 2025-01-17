# USAGE
# python train.py

# import the necessary packages
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from pyimagesearch import config
import numpy as np
import pickle
import os

def load_data_split(splitPath):
	# initialize the data and labels
	data = []
	labels = []

	# loop over the rows in the data split file
	for row in open(splitPath):
		# extract the class label and features from the row
		row = row.strip().split(",")
		label = row[0]
		features = np.array(row[1:], dtype="float")

		# update the data and label lists
		data.append(features)
		labels.append(label)

	# convert the data and labels to NumPy arrays
	data = np.array(data)
	labels = np.array(labels)

	# return a tuple of the data and labels
	return (data, labels)

# derive the paths to the training and testing CSV files
trainingPath = os.path.sep.join([config.BASE_CSV_PATH,
	"{}.csv".format(config.TRAIN)])
testingPath = os.path.sep.join([config.BASE_CSV_PATH,
	"{}.csv".format(config.TEST)])

# load the data from disk
print("[INFO] loading data...")
(trainX, trainY) = load_data_split(trainingPath)
(testX, testY) = load_data_split(testingPath)

# load the label encoder from disk
le = pickle.loads(open(config.LE_PATH, "rb").read())

# train the model
print("[INFO] training LR model...")
model = LogisticRegression(solver="lbfgs", multi_class="auto", max_iter=1000)
model.fit(trainX, trainY)

# evaluate the model
print("[INFO] evaluating...")
preds = model.predict(testX)
print(classification_report(testY, preds, target_names=le.classes_, labels=np.unique(preds)))

# overall accuracy
print("Accuracy : {}\n".format(accuracy_score(testY, preds)))

# by definition a confusion matrix C is such that C_{i, j} is equal to the number of observations 
# known to be in group i but predicted to be in group j.
print(confusion_matrix(testY, preds))

# train the model
print("[INFO] training L.SVM model...")
model = LinearSVC(random_state=0, tol=1e-5)
model.fit(trainX, trainY)

# evaluate the model
print("[INFO] evaluating...")
preds = model.predict(testX)
print(classification_report(testY, preds, target_names=le.classes_, labels=np.unique(preds)))

# overall accuracy
print("Accuracy : {}\n".format(accuracy_score(testY, preds)))

# by definition a confusion matrix C is such that C_{i, j} is equal to the number of observations 
# known to be in group i but predicted to be in group j.
print(confusion_matrix(testY, preds))

# serialize the model to disk
print("[INFO] saving model...")
f = open(config.MODEL_PATH, "wb")
f.write(pickle.dumps(model))
f.close()