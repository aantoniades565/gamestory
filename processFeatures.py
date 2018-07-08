import numpy as np
import os.path
import argparse
import operator
import csv
from collections import OrderedDict
import datetime

def file_choices(choices, fname):
    ext = os.path.splitext(fname)[1][1:]
    if ext not in choices:
       parser.error("File is not of type {}".format(choices))
    return fname

def process_file(file_path):
    file_dict = np.load(file_path).item()
    sorted_data = sorted(file_dict.items(), key=operator.itemgetter(0))
    return ([x[1] for x in sorted_data])

def process_metadata(file_path, timestamps):
    metadata_dict = dict(zip(timestamps, np.zeros(len(timestamps))))
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['UTC_timestamp'])
            start_time_object = datetime.datetime.strptime(row['UTC_timestamp'], "%Y-%m-%d %H:%M:%S")
            duration = int(row['duration'])
            for second in range(duration):
                offset = datetime.timedelta(seconds=second)
                current_timestamp = start_time_object + offset
                date_time_index = datetime.datetime.strftime(current_timestamp, "%Y-%m-%dT%H:%M:%S")
                metadata_dict[date_time_index] = 1

    sorted_metadata = sorted(metadata_dict.items(), key=operator.itemgetter(0))
    return ([x[1] for x in sorted_metadata])

parser = argparse.ArgumentParser(description='SVM classifier with parser for one or more feature arrays')
parser.add_argument('metadata_file', type=str, help='File path to metadata file, with columns: duration, stream_timestamp, UTC_timestamp')
parser.add_argument('feature_arrays', nargs='+', type=lambda s:file_choices(("npy", "npz"), s), help='Relative file paths of 1D feature arrays of equal length')
args = parser.parse_args()

first_dict = np.load(args.feature_arrays[0]).item()
number_of_keys = len(first_dict)
number_of_features = len(args.feature_arrays)

feature_vector = X = np.empty(shape=[number_of_keys, number_of_features])

for idx, val in enumerate(args.feature_arrays):
    feature_vector[:,idx] = process_file(val)

labels = process_metadata(args.metadata_file, sorted(first_dict.keys()))