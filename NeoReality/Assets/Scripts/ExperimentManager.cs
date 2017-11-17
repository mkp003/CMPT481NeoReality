using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExperimentManager : MonoBehaviour {


    // Objects that will be used in the demo part of the game, to familiarize
    // users with VR are listed below.
    [SerializeField]
    private GameObject demoObjects;

    // Lights for the room
    //[SerializeField]
    //private GameObject light1;
    //[SerializeField]
    //private GameObject light2;
    [SerializeField]
    private GameObject light;

    private bool turnningOn = false;
    private bool turnningOff = false;

    // Objects for the test
    [SerializeField]
    private GameObject conveyerBelt;
    [SerializeField]
    private GameObject testSwitch;

    [SerializeField]
    private List<GameObject> listOfTests = new List<GameObject>();


    private GameObject currentTest;


    // Use this for initialization
    void Start () {
        currentTest = listOfTests[0];
        Invoke("ExitSandbox", 3);
	}

    private void FixedUpdate()
    {
        if (turnningOff)
        {
            light.GetComponent<Light>().intensity -= 0.0041f;
            //light2.GetComponent<Light>().intensity -= 0.0006f;
        }
        if (turnningOn)
        {
            light.GetComponent<Light>().intensity += 0.0041f;
            //light2.GetComponent<Light>().intensity += 0.0006f;
        }
    }

    private void ExitSandbox()
    {
        turnningOff = true;
        Invoke("OpenTests", 10);
    }

    private void OpenTests()
    {
        turnningOff = false;
        turnningOn = true;
        demoObjects.SetActive(false);
        testSwitch.SetActive(true);
        Invoke("TurnOffBrightness", 10);
    }

    private void TurnOffBrightness()
    {
        this.turnningOn = false;
    }

    private void RetrieveNextTest()
    {
        if (listOfTests.Count > 0 && !this.currentTest.activeInHierarchy)
        {
            currentTest = listOfTests[0];
            currentTest.SetActive(true);
            listOfTests.RemoveAt(0);
            currentTest.SetActive(true);
            //currentTest.SendMessage("StartTimer");
            this.currentTest.GetComponent<NumberPad>().StartTimer();
        }
        if(listOfTests.Count == 0)
        {
            //Test is done, put finishing code here!
        }
    }

    private void SubmitCurrentTest()
    {
        this.currentTest.SetActive(false);
    }
}
