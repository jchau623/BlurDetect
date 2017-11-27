from sklearn import svm
import numpy as np

lin_clf = svm.LinearSVC()
DS_X = np.load("../training_np_arrays/X.npy")
DS_Y = np.load("../training_np_arrays/Y.npy")
print(DS_X)
print(DS_Y)
lin_clf.fit(DS_X, DS_Y)