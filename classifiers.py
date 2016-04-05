import csv
import numpy
from sklearn import tree

counter = 0
group = 0
sitting_values = {}
running_values = {}
stairs_values = {}
car_values = {}
walking_values = {}

for line in csv.reader(open("sitting.csv")):
	if group < 30 and "Time since start in ms" not in line[6]:
		if counter < 100:
			counter = counter + 1
			if group in sitting_values:
				# running_values[group].append(float(line[1].strip()))
				sitting_values[group].append(float(line[0].strip()))
			else:
				# running_values[group] = [float(line[1].strip())]
				sitting_values[group] = [float(line[0].strip())]
		else: 
			group = group + 1
			counter = 0

counter = 0
group = 0
for line in csv.reader(open("running.csv")):
	if group < 30 and "Time since start in ms" not in line[6]:
		if counter < 100:
			counter = counter + 1
			if group in running_values:
				running_values[group].append(float(line[0].strip()))
				# sitting_values[group].append(float(line[0].strip()))
			else:
				running_values[group] = [float(line[0].strip())]
				# sitting_values[group] = [float(line[0].strip())]
		else: 
			group = group + 1
			counter = 0

counter = 0
group = 0
for line in csv.reader(open("walking.csv")):
	if group < 30 and "Time since start in ms" not in line[6]:
		if counter < 100:
			counter = counter + 1
			if group in walking_values:
				walking_values[group].append(float(line[0].strip()))
			else:
				walking_values[group] = [float(line[0].strip())]
		else: 
			group = group + 1
			counter = 0

counter = 0
group = 0
for line in csv.reader(open("car.csv")):
	if group < 30 and "Time since start in ms" not in line[6]:
		if counter < 100:
			counter = counter + 1
			if group in car_values:
				car_values[group].append(float(line[0].strip()))
			else:
				car_values[group] = [float(line[0].strip())]
		else: 
			group = group + 1
			counter = 0

counter = 0
group = 0
for line in csv.reader(open("stairs.csv")):
	if group < 30 and "Time since start in ms" not in line[6]:
		if counter < 100:
			counter = counter + 1
			if group in stairs_values:
				stairs_values[group].append(float(line[0].strip()))
			else:
				stairs_values[group] = [float(line[0].strip())]
		else: 
			group = group + 1
			counter = 0

sitting_averages = {}
running_averages = {}
walking_averages = {}
car_averages = {}
stairs_averages = {}

sitting_stdevs = {}
running_stdevs = {}
walking_stdevs = {}
car_stdevs = {}
stairs_stdevs = {}

for group in sitting_values:
	sitting_averages[group] = numpy.mean(sitting_values[group])
	sitting_stdevs[group] = numpy.std(sitting_values[group])
	
	running_stdevs[group] = numpy.std(running_values[group])
	running_averages[group] = numpy.mean(running_values[group])

	walking_stdevs[group] = numpy.std(walking_stdevs[group])
	walking_averages[group] = numpy.mean(walking_averages[group])

	car_stdevs[group] = numpy.std(car_stdevs[group])
	car_averages[group] = numpy.mean(car_averages[group])

	stairs_stdevs[group] = numpy.std(stairs_stdevs[group])
	stairs_averages[group] = numpy.mean(stairs_averages[group])

training_labels = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

training_sitting = []
training_running = []
training_stairs = []
training_walking = []
training_car = []

for i in range(0,24):
	training_sitting.append([1, sitting_averages[i]])
	training_running.append([1, running_averages[i]])
	training_stairs.append([1, stairs_averages[i]])
	training_walking.append([1, walking_averages[i]])
	training_car.append([1, car_averages[i]])

test_sitting = []
test_running = []
test_stairs = []
test_walking = []
test_car = []

for i in range(24, 30):
	test_running.append([1, running_averages[i]])
	test_sitting.append([1, sitting_averages[i]])
	test_stairs.append([1, stairs_averages[i]])
	test_walking.append([1, walking_averages[i]])
	test_car.append([1, car_averages[i]])

all_test = test_sitting + test_running + test_car + test_walking + test_stairs

all_training = training_sitting + training_running + training_car + training_walking + training_stairs

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