import os
import pandas as pd
import numpy as np


class LoadingData:
    def __init__(self, true_position, filename_dataset, filename_anchors, indexes, start, end, start_comb, end_comb):
        self.true_position = true_position
        self.filename_dataset = filename_dataset
        self.filename_anchors = filename_anchors
        self.indexes = indexes
        self.start = start
        self.end = end
        self.start_comb = start_comb
        self.end_comb = end_comb
        self.ranges_order = np.arange(0, len(indexes))

    def loadDataSet(self):
        if self.dataset_header:
            self.dataset_header = None
            self.start = 1

        # actual_directory = os.getcwd()
        # filename = actual_directory + self.filename_dataset
        filename = self.filename_dataset
        # loading data considering the number of elements and indexes to load
        if self.end > 0:
            data_loaded = pd.read_csv(filename, header=self.dataset_header,
                                      skiprows=self.start, nrows=self.end, usecols=self.indexes)
        else:
            data_loaded = pd.read_csv(
                filename, header=self.dataset_header, skiprows=self.start,  usecols=self.indexes)
        data_loaded = data_loaded.to_numpy()  # convert pandas into numpy array
        return data_loaded

    def loadDataWithoutHeaders(self):
        # self.start = 0
        # actual_directory = os.getcwd()
        # filename = actual_directory + self.filename_dataset
        filename = self.filename_dataset
        if self.end > 0:
            data_loaded = pd.read_csv(
                filename, header=None, skiprows=self.start, nrows=self.end, usecols=self.indexes)
        else:
            data_loaded = pd.read_csv(
                filename, header=None, skiprows=self.start,  usecols=self.indexes)

        data_loaded = data_loaded.to_numpy()  # convert pandas into numpy array
        return data_loaded

    def loadWithHeaders(self):
        self.start = 1
        # actual_directory = os.getcwd()
        # filename = actual_directory + self.filename_dataset
        filename = self.filename_dataset
        if self.end > 0:
            data_loaded = pd.read_csv(
                filename, header=None, skiprows=self.start, nrows=self.end, usecols=self.indexes)
        else:
            data_loaded = pd.read_csv(
                filename, header=None, skiprows=self.start, usecols=self.indexes)

        data_loaded = data_loaded.to_numpy()  # convert pandas into numpy array
        return data_loaded

    def loadAnchorsCoordinates(self):
        # actual_directory = os.getcwd()
        # filename = actual_directory + self.filename_anchors
        filename = self.filename_anchors
        if filename:        
            anchors_coordinates = pd.read_csv(filename, header=None).to_numpy() # loading list of coordinate form the anchors
        else:
            anchors_coordinates = None
        return anchors_coordinates

    def loadingPosDataFromRangeIter(self, index):
        # actual_directory = os.getcwd()
        # filename = actual_directory + self.filename_dataset
        filename = self.filename_dataset
        data = pd.read_csv(filename, usecols=self.indexes)
        return data[data["range_set"] == index].to_numpy()

    def loadingPosDataWithCondition(self, numb_comb, comb):
        # actual_directory = os.getcwd()
        # filename = actual_directory + self.filename_dataset
        filename = self.filename_dataset
        data = pd.read_csv(filename, usecols=self.indexes)

        if comb == None:
            return data[data["num_comb"] == numb_comb].to_numpy()
        else:
            result = data[data["num_comb"] == numb_comb]
            result = result[result['combination'].str.contains(comb)]
            return result.to_numpy()
