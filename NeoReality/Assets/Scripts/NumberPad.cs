using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;


public class NumberPad : MonoBehaviour {

    // Reference to the controller
    [SerializeField]
    private GameObject experimentManager;

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

    public Vector3 testPosition;
    public Vector3 endPosition;

    private bool enter = false;
    private bool leave = false;
    private bool testStarted = false;

    public bool testDone = false;

    private void FixedUpdate()
    {
        if (enter && this.transform.position.x > this.testPosition.x)
        {
            this.transform.position = new Vector3(this.transform.position.x - 0.015f, this.transform.position.y, this.transform.position.z);
        }

        if (leave && this.transform.position.x > this.endPosition.x)
        {
            this.transform.position = new Vector3(this.transform.position.x - 0.015f, this.transform.position.y, this.transform.position.z);
        }

        if(this.transform.position.x <= this.testPosition.x && !testStarted)
        {
            this.testStarted = true;
            StartTimer();
        }
    }

    // Use this for initialization
    void Start () {
        this.buttonInput = new List<string>();
	}
	
    public void Enter()
    {
        this.enter = true;
    }


    /// <summary>
    /// Grab the start time for this test
    /// </summary>
    public void StartTimer()
    {
        print("Timer started");
        this.startTime = Time.time;
    }

    /// <summary>
    /// Grab the end time for this test
    /// </summary>
    public void EndTimer(string[] newFile)
    {
        this.endTime = Time.time;
        bool createNewFile;
        bool.TryParse(newFile[0], out createNewFile);
        EndTest(createNewFile);
        this.experimentManager.SendMessage("SubmitCurrentTest");
    }

    /// <summary>
    /// Adds the input from the button to the list of user inputs
    /// </summary>
    /// <param name="input"></param>
	public void ButtonInput(string[] input)
    {
        print("Keypad recieved input: " + input.ToString());
        this.buttonInput.Add(input[0]);
    }


    /// <summary>
    /// Finish this test
    /// </summary>
    public void EndTest(bool newFile)
    {
        this.leave = true;
        float speed = this.endTime - this.startTime;
        float accuracy = CalculateAccuracy();

        WriteTestToCSV(newFile, speed, accuracy);
        testDone = true;
    }
    

    /// <summary>
    /// Calculate the accuracy for this test
    /// </summary>
    /// <returns>The calculated accuracy for this test</returns>
    public float CalculateAccuracy()
    {
        float numEntered = this.buttonInput.Count;

        float numCorrect = 0;

        int currentAnswer = 0;

        // Check if the user actually inputed any values. If not, their accuracy is 0.
        if (numEntered > 0)
        {

            foreach (string answer in buttonInput)
            {
                if (correctSequence[currentAnswer].Equals(answer))
                {
                    numCorrect += 1;
                    currentAnswer++;
                }
            }

            return numCorrect / numEntered;
        }
        else
        {
            return 0;
        }

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
            string name = f.Name;
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
            string header = "Test Number" + ',' + "Speed" + ',' + "Accuracy" + System.Environment.NewLine;

            File.WriteAllText(this.filePath + newFileName, header);
        }

        string data = testNum.ToString() + ',' + speed.ToString() + ',' + accuracy.ToString() + System.Environment.NewLine;

        File.AppendAllText(this.filePath + newFileName, data);


    }


}
