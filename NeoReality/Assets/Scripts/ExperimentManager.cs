using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExperimentManager : MonoBehaviour {


    // Objects that will be used in the demo part of the game, to familiarize
    // users with VR are listed below.
    [SerializeField]
    private GameObject table;
    [SerializeField]
    private GameObject playObj1;
    [SerializeField]
    private GameObject playObj2;
    [SerializeField]
    private GameObject playObj3;

    // Lights for the room
    [SerializeField]
    private GameObject light1;
    [SerializeField]
    private GameObject light2;
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
        Invoke("ExitSandbox", 10);
	}

    private void FixedUpdate()
    {
        if (turnningOff)
        {
            light1.GetComponent<Light>().intensity -= 0.0006f;
            light2.GetComponent<Light>().intensity -= 0.0006f;
        }
        if (turnningOn)
        {
            light1.GetComponent<Light>().intensity += 0.0006f;
            light2.GetComponent<Light>().intensity += 0.0006f;
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
        table.SetActive(false);
        playObj1.SetActive(false);
        playObj2.SetActive(false);
        playObj3.SetActive(false);
        Invoke("TurnOffBrightness", 10);
    }

    private void TurnOffBrightness()
    {
        this.turnningOn = false;
    }

    private void RetrieveNextTest()
    {
        if (listOfTests.Count > 0)
        {
            currentTest = listOfTests[0];
            currentTest.SetActive(true);
            listOfTests.RemoveAt(0);
            currentTest.SendMessage("StartTimer");
        }
    }

    private void SubmitCurrentTest()
    {
        this.currentTest.SetActive(false);
    }
}
