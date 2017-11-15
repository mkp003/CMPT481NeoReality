using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class NumberPad : MonoBehaviour {

    // The path to the storage directory
    public string filePath;

    // The test number
    public int testNum;

    // The correct sequence for this test
    [SerializeField]
    private List<string> correctSequence;

    // The sequence the user entered
    private List<string> buttonInput;

    // The start time for this test
    private float startTime;

    // The end time for this test
    private float endTime;

	// Use this for initialization
	void Start () {
        this.buttonInput = new List<string>();
	}
	

    /// <summary>
    /// Grab the start time for this test
    /// </summary>
    public void StartTimer()
    {
        this.startTime = Time.time;
    }

    /// <summary>
    /// Grab the end time for this test
    /// </summary>
    public void EndTimer(bool newFile)
    {
        this.endTime = Time.time;
        EndTest(newFile);
    }

    /// <summary>
    /// Adds the input from the button to the list of user inputs
    /// </summary>
    /// <param name="input"></param>
	public void ButtonInput(string input)
    {
        this.buttonInput.Add(input);
    }


    /// <summary>
    /// Finish this test
    /// </summary>
    public void EndTest(bool newFile)
    {
        float speed = this.endTime - this.startTime;
        float accuracy = CalculateAccuracy();

        WriteTestToCSV(newFile, speed, accuracy);
    }
    

    /// <summary>
    /// Calculate the accuracy for this test
    /// </summary>
    /// <returns>The calculated accuracy for this test</returns>
    public float CalculateAccuracy()
    {
        int numEntered = this.buttonInput.Count;

        int numCorrect = 0;

        int currentAnswer = 0;

        foreach (string answer in buttonInput){
            if (correctSequence[currentAnswer].Equals(answer))
            {
                numCorrect += 1;
                currentAnswer++;
            }    
        }

        return numCorrect / numEntered;

    }

    /// <summary>
    /// Write the results to a CSV file
    /// </summary>
    /// <param name="speed">The speed for the test</param>
    /// <param name="accuracy">The accuracy for the test</param>
    public void WriteTestToCSV(bool newFile, float speed, float accuracy)
    {
        // Find the existing files and create a new one with the next id number if necessary
        DirectoryInfo dir = new DirectoryInfo(filePath);
        FileInfo[] info = dir.GetFiles("*.csv");

        int lastFile = 0;

        foreach (FileInfo f in info)
        {
            string name = f.ToString();
            string number = name.Substring(5, 3);
            int fileNum = int.Parse(number);

            if(fileNum > lastFile)
            {
                lastFile = fileNum;
            }
        }

        if (newFile) {
            lastFile += 1;
        }

        string newFileName = "";
        if (lastFile < 10)
        {
            newFileName = "Part-00" + lastFile.ToString() + ".csv";
        }else if(lastFile < 100)
        {
            newFileName = "Part-0" + lastFile.ToString() + ".csv";
        }
        else
        {
            newFileName = "Part-" + lastFile.ToString() + ".csv";
        }

        if (newFile)
        {
            string header = "Test Number" + ',' + "Speed" + ',' + "Accuracy";

            File.WriteAllText(newFileName, header);
        }

        string data = testNum.ToString() + ',' + speed.ToString() + ',' + accuracy.ToString();

        File.AppendAllText(newFileName, data);

    }


}
