import csv
import numpy
from sklearn.datasets import load_iris
from sklearn import tree

counter = 0
group = 0
sitting_values = {}
running_values = {}
for line in csv.reader(open("sensors.csv")):
	if group < 30 and "Time since start in ms" not in line[6]:
		if counter < 100:
			counter = counter + 1
			if group in sitting_values:
				running_values[group].append(float(line[1].strip()))
				sitting_values[group].append(float(line[0].strip()))
			else:
				running_values[group] = [float(line[1].strip())]
				sitting_values[group] = [float(line[0].strip())]
		else: 
			group = group + 1
			counter = 0

sitting_averages = {}
sitting_stdevs = {}
running_averages = {}
running_stdevs = {}
for group in sitting_values:
	sitting_averages[group] = numpy.mean(sitting_values[group])
	sitting_stdevs[group] = numpy.std(sitting_values[group])
	running_stdevs[group] = numpy.std(running_values[group])
	running_averages[group] = numpy.mean(running_values[group])

training_labels = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

training_sitting = []
training_running = []
for i in range(0,24):
	training_sitting.append([1, sitting_averages[i]])
	training_running.append([1, running_averages[i]])

test_sitting = []
test_running = []
for i in range(24, 30):
	test_running.append([1, running_averages[i]])
	test_sitting.append([1, sitting_averages[i]])
all_test = test_sitting + test_running

all_training = training_sitting + training_running

test_labels = [0,0,0,0,0,0,1,1,1,1,1,1]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(all_training, training_labels)
output_labels = []
for i in range(0,12):
	result = clf.predict([all_test[i]])
	output_labels.append(result[0])

print
print "Decision Tree"
total = len(output_labels)
correct_counter = 0
for i in test_labels:
	if test_labels[i] == output_labels[i]:
		# print 'wohoo!'
		correct_counter = correct_counter + 1
print "Accuracy is ", float(correct_counter/total)



from sklearn import svm
svc = svm.SVC(kernel='linear')
svc.fit(all_training, training_labels)  
output_labels = []
for i in range(0,12):
	result = svc.predict([all_test[i]])
	output_labels.append(result[0])

print
print "SVM"
total = len(output_labels)
correct_counter = 0
for i in test_labels:
	if test_labels[i] == output_labels[i]:
		correct_counter = correct_counter + 1
print "Accuracy is ", float(correct_counter/total)



from sklearn import linear_model
logistic = linear_model.LogisticRegression(C=1e5)
logistic.fit(all_training, training_labels)
output_labels = []
for i in range(0,12):
	result = logistic.predict([all_test[i]])
	output_labels.append(result[0])

print
print "LogisticRegression"
total = len(output_labels)
correct_counter = 0
for i in test_labels:
	if test_labels[i] == output_labels[i]:
		correct_counter = correct_counter + 1
print "Accuracy is ", float(correct_counter/total)
print