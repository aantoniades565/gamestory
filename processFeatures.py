import numpy as np
import os.path
import argparse
import operator
import csv
from sklearn import svm
from sklearn.preprocessing import normalize
from sklearn.metrics import accuracy_score, classification_report
from collections import OrderedDict
import datetime
import matplotlib.pyplot as plt
import fnmatch

def process_file(file_dict):
    sorted_data = sorted(file_dict.items(), key = operator.itemgetter(0))
    return ([x[1] for x in sorted_data])

def process_metadata(file_path, timestamps):
    metadata_dict = dict(zip(timestamps, np.zeros(len(timestamps))))
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time_object = datetime.datetime.strptime(row['UTC_timestamp'], "%Y-%m-%d %H:%M:%S")
            duration = int(row['duration'])
            for second in range(duration):
                offset = datetime.timedelta(seconds=second)
                current_timestamp = start_time_object + offset
                date_time_index = datetime.datetime.strftime(current_timestamp, "%Y-%m-%dT%H:%M:%S")
                if date_time_index in metadata_dict:
                    metadata_dict[date_time_index] = 1

    sorted_metadata = sorted(metadata_dict.items(), key=operator.itemgetter(0))
    return ([x[1] for x in sorted_metadata])

parser = argparse.ArgumentParser(description='SVM classifier with parser for one or more feature arrays')
parser.add_argument('training_metadata_file', type=str, help='Path to metadata file for training set, with columns: duration, stream_timestamp, UTC_timestamp')
parser.add_argument('test_metadata_file', type=str, help='Path to metadata file for test set, with columns: duration, stream_timestamp, UTC_timestamp')
parser.add_argument('training_dir', type=str, help='Path to directory only containing training feature dictionaries stored in .npy or .npz files')
parser.add_argument('test_dir', type=str, help='Path to directory only containing test feature dictionaries stored in .npy or .npz files')
args = parser.parse_args()

training_feature_vector = number_of_keys = dict_keys = 0
firstFile = True
number_of_features = len(fnmatch.filter(os.listdir(args.training_dir),'*.npy'))

for idx, val in enumerate(sorted(os.listdir(args.training_dir))):
    if val.endswith(".npy"):
        file_path = os.path.join(args.training_dir, val)
        training_dict = np.load(file_path).item()
        if firstFile:
            number_of_keys = len(training_dict)
            training_feature_vector = np.empty(shape=[number_of_keys, number_of_features])
            firstFile = False
            dict_keys = training_dict.keys()
        training_feature_vector[:,idx-1] = process_file(training_dict)
        continue
    else:
        continue

training_feature_vector = normalize(training_feature_vector, axis=0, norm='max')
#plt.plot(training_feature_vector[:,3])
#plt.show()
training_labels = process_metadata(args.training_metadata_file, sorted(dict_keys))
clf = svm.SVG(C=10)
print('Training error:', clf.fit(training_feature_vector, training_labels).score(training_feature_vector, training_labels))

test_feature_vector = number_of_keys = dict_keys = 0
firstFile = True
number_of_features = len(fnmatch.filter(os.listdir(args.test_dir),'*.npy'))

for idx, val in enumerate(sorted(os.listdir(args.test_dir))):
    if val.endswith(".npy"):
        file_path = os.path.join(args.test_dir, val)
        test_dict = np.load(file_path).item()
        if firstFile:
            number_of_keys = len(test_dict)
            test_feature_vector = np.empty(shape=[number_of_keys, number_of_features])
            firstFile = False
            dict_keys = test_dict.keys()
        processed = process_file(test_dict)
        test_feature_vector[:,idx-1] = process_file(test_dict)
        continue
    else:
        continue

test_feature_vector = normalize(test_feature_vector, axis=0, norm='max')
test_labels = process_metadata(args.test_metadata_file, sorted(dict_keys))
clf.score(test_feature_vector, test_labels)
predicted = clf.predict(test_feature_vector)
#print(sorted(predicted))
#print(accuracy_score(test_feature_vector, predicted))
print(classification_report(test_labels, predicted))
