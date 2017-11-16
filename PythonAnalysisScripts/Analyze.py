"""
Analysis script for CMPT 481 VR research

This script will take in a series of CSV data files with speeds and accuracies.  It will perform a kruskal wallis test
and a mann whitney test to determine the statistical significance of the trials
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stat
import getopt


def find_all_csvs(dir):
    '''
    Find all csv files in the given directory and return them as a list
    :param dir: The directory to search in
    :return: A list of csv files
    '''
    pass


def read_csvs_as_dataframe(csvs):
    '''
    Take all csv files in a given list and read them into pandas dataframes
    :param csvs: The list of csv files to read
    :return: A list of dataframes
    '''
    pass

def separate_datasets(dataframes):
    '''
    Separate the data in the dataframes into different datasets based on trial number
    :param dataframes: A list of dataframes to parse from
    :return: A dictionary of lists In the format
     {Design: [trial0, trial1, trial2], Texture: [trial3, trial4, trial5], Feedback: [trial6, trial 7, trial 8]}
    '''
    pass

def perform_statistical_analysis(datasets):
    '''
    Perform the statistical tests
    :param datasets: A list of datasets indexed by their trial number
    :return: Nothing
    '''
    pass

    # TODO: perfrom the kruskal wallis test using scipy.stats and write to stats file

    # TODO: get mean and S.D for each trial - append to stats file named by dictionary key

    # TODO: For each trial perform a Mann-Whitney test using scipy.stats - append to stats file

    # TODO: Write all datasets to a new organized csv file

    # TODO: Make and save pretty graphs


def write_new_dataset_csv(datasets):
    '''
    Write the sorted datasets to a csv
    :param datasets: A list of datasets to write
    :return: Nothing
    '''
    pass


def main():
    pass

# TODO: get command line options

# TODO: get all csvs

# TODO: convert to dataframes

# TODO: seperate datasets

# TODO: perform statistical analysis for designs

# TODO: perfrom stat analysis for textures

# TODO: perform stat analysis for feedback

if __name__ == "__main__":
    main()