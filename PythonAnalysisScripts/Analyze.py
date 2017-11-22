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
import sys
import os


def find_all_csvs(dir):
    '''
    Find all csv files in the given directory and return them as a list
    :param dir: The directory to search in
    :return: A list of csv files
    '''
    csv_files = []
    for file in os.listdir(dir):
        if file.endswith(".csv"):
            csv_files.append(dir + '/' + file)

    return csv_files


def read_csvs_as_dataframe(csvs):
    '''
    Take all csv files in a given list and read them into pandas dataframes
    :param csvs: The list of csv files to read
    :return: A list of dataframes
    '''
    dataframes = []

    for csv in csvs:
        df = pd.read_csv(csv)
        dataframes.append(df)

    return dataframes

def separate_datasets(dataframes):
    '''
    Separate the data in the dataframes into different datasets based on trial number
    :param dataframes: A list of dataframes to parse from
    :return: A dictionary of lists In the format
     {trial_#_speeds: [values], trial_#_accuracies: [values]}
    '''

    datasets = {}

    for df in dataframes:
        for index, row in df.iterrows():
            # Get the speed and accuracy for each trial and append it to the list of values for that trial
            speed_name = "trial_" + str(int(row["Test Number"])) + "_speeds"
            accuracy_name = "trial_" + str(int(row["Test Number"])) + "_accuracies"

            # Check to see if the key exists
            if speed_name in datasets.keys():
                datasets[speed_name].append(row["Speed"])\

            # If not, initialize the list of values
            else:
                datasets[speed_name] = [row["Speed"]]

            if accuracy_name in datasets.keys():
                datasets[accuracy_name].append(row["Accuracy"])
            else:
                datasets[accuracy_name] = [row["Accuracy"]]

    return datasets


def perform_statistical_analysis(datasets):
    '''
    Perform the statistical tests
    :param datasets: A list of datasets
    :return: The statistical values as a dictionary keyed by test name
    '''
    results = {}

    # Perform Kruskall Wallis test
    h_val_kruskall, p_val_kruskall = stat.mstats.kruskalwallis(datasets)

    results["Kruskall"] = (h_val_kruskall, p_val_kruskall)

    # get mean and S.D for each trial
    for i in range(len(datasets)):
        results["trial_" + str(i) + "_SD"] = np.std(datasets[i])
        results["trial_" + str(i) + "_mean"] = np.mean(datasets[i])

    # For each trial perform a Mann-Whitney test using scipy.stats

    

    # TODO: Make and save pretty graphs


def write_new_dataset_csv(datasets):
    '''
    Write the sorted datasets to a csv
    :param datasets: A list of datasets to write
    :return: Nothing
    '''
    pass

def usage():
    '''
    Print the usage of this script
    :return: Nothing
    '''
    pass
    # TODO: print usage


def main():

    input_directory = ''    # The directory to get the csv files from
    output_directory = ''   # The directory to save output to

    # Try to parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])

    # Catch any errors and print them
    except getopt.GetoptError as err:
        print(str(err))
        usage()             # Print the usage for help
        sys.exit(2)

    # Check each of the command line arguments
    for opt, arg in opts:
        # Print the usage for the script
        if opt in ("-h", "--help"):
            usage()
            sys.exit()

        # Get the input directory for files
        elif opt in("-i", "--input"):
            input_directory = arg

        # Get the output direvtory for files
        elif opt in("-o", "--output"):
            output_directory = arg

        # Bad option, show help and exit
        else:
            print("Unhandled Option")
            usage()
            sys.exit(2)


    # Get all csvs in input_directory
    csvs = find_all_csvs(input_directory)

    # Convert csvs to dataframes
    dataframes = read_csvs_as_dataframe(csvs)

    # seperate datasets
    datasets = separate_datasets(dataframes)

    perform_statistical_analysis([datasets['trial_1_speeds'], datasets['trial_2_speeds'], datasets['trial_3_speeds']])

if __name__ == "__main__":
    main()