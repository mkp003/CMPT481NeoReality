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
import csv
import json


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


def set_box_colours(bp, colours):
    """
    Set the colours of a given boxplot
    :param colours: Colours to use for the plots
    :param bp: The box plot to change colours for
    :return: Nothing
    """
    plt.setp(bp['boxes'][0], color=colours[0])
    plt.setp(bp['caps'][0], color=colours[0])
    plt.setp(bp['caps'][1], color=colours[0])
    plt.setp(bp['whiskers'][0], color=colours[0])
    plt.setp(bp['whiskers'][1], color=colours[0])
    plt.setp(bp['medians'][0], color=colours[0])

    plt.setp(bp['boxes'][1], color=colours[1])
    plt.setp(bp['caps'][2], color=colours[1])
    plt.setp(bp['caps'][3], color=colours[1])
    plt.setp(bp['whiskers'][2], color=colours[1])
    plt.setp(bp['whiskers'][3], color=colours[1])
    plt.setp(bp['medians'][1], color=colours[1])

    plt.setp(bp['boxes'][2], color=colours[2])
    plt.setp(bp['caps'][4], color=colours[2])
    plt.setp(bp['caps'][5], color=colours[2])
    plt.setp(bp['whiskers'][4], color=colours[2])
    plt.setp(bp['whiskers'][5], color=colours[2])
    plt.setp(bp['medians'][2], color=colours[2])



def perform_statistical_analysis(datasets, labels, out_path, file_name, title, ylabel, verbose):
    '''
    Perform the statistical tests and export datasets as graphs
    :param datasets: A list of datasets
    :param labels: A list of string labels for the datasets
    :param out_path: The path to save data to
    :param file_name: Name for the output file NOT including extension
    :param title: The title for the dataset as a whole for the graph
    :param ylabel: The text to put on the y axis of the graph
    :param verbose: Print results to console and show plots
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
    for i in range(len(datasets)):
        for j in range(len(datasets)):
            if i != j:
                h_val, p_val = stat.mannwhitneyu(datasets[i], datasets[j])
                results["Mann-Whitney_" + str(i) + "_" + str(j)] = (h_val, p_val)

    # Make and save pretty graphs
    plt.figure()
    ax = plt.axes()

    # Make a boxplot for the data
    plt.boxplot(datasets)

    # Set the labels
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)

    # Set title
    plt.title(title)

    plt.savefig(out_path + "/" + file_name + ".png")

    if verbose:
        plt.show()

    write_new_dataset_csv(datasets, out_path, file_name, labels)
    write_results(results, out_path, file_name,  verbose)

    return results


def write_new_dataset_csv(datasets, outpath, file_name, labels):
    '''
    Write the sorted datasets to a csv
    :param datasets: A list of datasets to write
    :param outpath: Path  for results
    :param file_name: File name NOT including extension
    :param labels: Labels for each dataset
    :return: Nothing
    '''

    rows = zip(*datasets)
    file_name += "_dataset"
    with open(outpath + "/" + file_name + ".csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(labels)
        for row in rows:
            writer.writerow(row)

def write_results(results, outpath, file_name, verbose):
    '''
    Write the results to a json file
    :param results: A dictionary of the results to write
    :param outpath: The directory to write the file to
    :param file_name: The name for the file
    :param verbose: Print the output to the console
    :return: Nothing
    '''
    text = ""

    if results["Kruskall"][1] >= 0.05:
        text += "Kruskall-Wallis revealed no significant difference (X^2 = " + str(results["Kruskall"][0]) \
                + ", p = " + str(results["Kruskall"][1]) + "). \n\n"
    else:
        text += "Kruskall-Wallis revealed a significant difference (X^2 = " + str(results["Kruskall"][0]) \
               + ", p = " + str(results["Kruskall"][1]) + "). \n\n"

    text += "Post hoc Mann-Whitney U tests: \n"

    for i in range(2):
        for j in range(1,3):
            if i == j:
                continue
            if results["Mann-Whitney_" + str(i) + "_" + str(j)][1] > 0.05:
                text += "There is no significant difference between test " + str(i) + " and " + str(j) \
                        + "(U = " + str(results["Mann-Whitney_" + str(i) + "_" + str(j)][0]) \
                        + ". p = " + str(results["Mann-Whitney_" + str(i) + "_" + str(j)]) + " \n\n"
            else:
                text += "There is a significant difference between test " + str(i) + " and " + str(j) \
                        + "(U = " + str(results["Mann-Whitney_" + str(i) + "_" + str(j)][0]) \
                        + ". p = " + str(results["Mann-Whitney_" + str(i) + "_" + str(j)]) + " \n\n"

    for i in range(3):
        text += "Trial " + str(i) + " Mean: " + str(results["trial_" + str(i) + "_mean"]) + " \n"
        text += "Trial " + str(i) + " SD: " + str(results["trial_" + str(i) + "_SD"]) + "\n\n"

    if verbose:
        print(text)

    with open(outpath + "/" + file_name + ".txt", "w") as f:
        f.write(text)

def get_colour(num):

    if num == 1:
        return 'darkgreen'
    elif num ==2:
        return 'violet'
    elif num == 3:
        return 'maroon'
    elif num == 5:
        return 'blue'
    elif num == 6:
        return 'coral'
    elif num == 7:
        return 'green'
    elif num == 9:
        return 'indigo'
    elif num == 10:
        return 'orange'
    elif num == 11:
        return 'sienna'
    else:
        return 'w'

def create_large_graph(datasets, labels, dataset_names, plot_title, y_label,  verbose, outpath):
    """
    Create one graph for all three test categories
    :param datasets: The datasets to plot
    :param labels: The labels for each of the datasets
    :param dataset_names: The names of the dataset categories
    :param plot_title: The title for the plot
    :param y_label: The label for the y axis
    :param verbose: Display the plot
    :param outpath: The directory to save the plot to
    :return: Nothing
    """

    ax = plt.axes()

    i = 1
    j = 2
    k = 3
    for data in datasets:
        bp = plt.boxplot(data, positions=[i, j, k], widths=0.6)
        set_box_colours(bp, [get_colour(i),get_colour(j),get_colour(k)])

        i += 4
        j += 4
        k += 4


    ax.set_xticklabels(dataset_names)
    ax.set_xticks([2, 6, 10])

    h1, = plt.plot([1, 1], get_colour(1))
    h2, = plt.plot([1, 1], get_colour(2))
    h3, = plt.plot([1, 1], get_colour(3))
    h4, = plt.plot([1, 1], get_colour(5))
    h5, = plt.plot([1, 1], get_colour(6))
    h6, = plt.plot([1, 1], get_colour(7))
    h7, = plt.plot([1, 1], get_colour(9))
    h8, = plt.plot([1, 1], get_colour(10))
    h9, = plt.plot([1, 1], get_colour(11))

    plt.legend((h1, h2, h3, h4, h5, h6, h7, h8, h9), labels)
    plt.title(plot_title)
    plt.ylabel(y_label)

    h1.set_visible(False)
    h2.set_visible(False)
    h3.set_visible(False)
    h4.set_visible(False)
    h5.set_visible(False)
    h6.set_visible(False)
    h7.set_visible(False)
    h8.set_visible(False)
    h9.set_visible(False)

    plt.xlim(0, 12)

    plt.savefig(outpath + plot_title + "_large_graph.png", dpi=300)

    if verbose:
        plt.show()

def usage():
    '''
    Print the usage of this script
    :return: Nothing
    '''
    print("Analyze.py\n")
    print("Analyze VR research data with statistical analysis methods.\n")
    print("This script will take in a directory of csv files and parse out the datasets.  It will then perform a "
          "Kruskal-Wallis test on each dataset and perform post hoc Mann-Whitney U tests on each individual set.")
    print("")
    print("Options:")
    print("     -h:                 Print this help dialog")
    print("     -i <path>:          Specify the directory to get the data files from")
    print("     -o <path>:          Specify the directory to save output files to")
    print("     -v:                 Print output to console and display graphs as well as saving output files")


def main():

    input_directory = ''    # The directory to get the csv files from
    output_directory = ''   # The directory to save output to
    verbose = False

    # Try to parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:v", ["help", "input=", "output=", "verbose"])

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

        # Verbose mode
        elif opt in("-v", "--verbose"):
            verbose = True

        # Bad option, show help and exit
        else:
            print("Unhandled Option")
            usage()
            sys.exit(2)

    if(input_directory == '' or output_directory == ''):
        usage()
        sys.exit(2)

    # Get all csvs in input_directory
    csvs = find_all_csvs(input_directory)

    # Convert csvs to dataframes
    dataframes = read_csvs_as_dataframe(csvs)

    # seperate datasets
    datasets = separate_datasets(dataframes)

    # Design stats
    design_labels = ["Hexagon", "Circle", "Tube"]

    design_speeds = [datasets['trial_1_speeds'], datasets['trial_2_speeds'], datasets['trial_3_speeds']]
    perform_statistical_analysis(design_speeds, design_labels, output_directory, "design_speeds", "Design Speeds",
                                 "Time (s)", verbose)

    design_accuracies = [datasets['trial_1_accuracies'], datasets['trial_2_accuracies'], datasets['trial_3_accuracies']]
    perform_statistical_analysis(design_accuracies, design_labels, output_directory, "design_accuracies", "Design Accuracies",
                                 "Accuracy (correct/entered)", verbose)


    # Texture Stats
    texture_labels = ["Rock", "Metal", "Transparent"]

    texture_speeds = [datasets['trial_4_speeds'], datasets['trial_5_speeds'], datasets['trial_6_speeds']]
    perform_statistical_analysis(texture_speeds, texture_labels, output_directory, "texture_speeds", "Texture Speeds",
                                 "Time (s)", verbose)

    texture_accuracies = [datasets['trial_4_accuracies'], datasets['trial_5_accuracies'], datasets['trial_6_accuracies']]
    perform_statistical_analysis(texture_accuracies, texture_labels, output_directory, "texture_accuracies",
                                 "Texture Accuracies",
                                 "Accuracy (correct/entered)", verbose)

    # Feedback Stats
    feedback_labels = ["None", "Colour", "Audio"]

    feedback_speeds = [datasets['trial_7_speeds'], datasets['trial_8_speeds'], datasets['trial_9_speeds']]
    perform_statistical_analysis(feedback_speeds, feedback_labels, output_directory, "feedback_speeds", "Feedback Speeds",
                                 "Time (s)", verbose)

    feedback_accuracies = [datasets['trial_7_accuracies'], datasets['trial_8_accuracies'],
                          datasets['trial_9_accuracies']]
    perform_statistical_analysis(feedback_accuracies,  feedback_labels, output_directory, "feedback_accuracies",
                                 "Feedback Accuracies",
                                 "Accuracy (correct/entered)", verbose)

    all_labels = design_labels + texture_labels + feedback_labels

    create_large_graph([design_speeds, texture_speeds, feedback_speeds],
                       all_labels, ["Designs", "Textures", "Feedback Types"], "Speeds", "Time (s)", verbose, output_directory)

    create_large_graph([design_accuracies, texture_accuracies, feedback_accuracies],
                       all_labels, ["Designs", "Textures", "Feedback Types"], "Accuracies",
                       "Accuracy (#correct/#entered)", verbose, output_directory)

    print(design_accuracies)

if __name__ == "__main__":
    main()