﻿using System.Collections;
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
    public GameObject conveyorTop;
    [SerializeField]
    private GameObject testSwitch;

    [SerializeField]
    private List<GameObject> listOfTests = new List<GameObject>();


    private GameObject currentTest;

    private bool isFirstTest = true;

    


    // Use this for initialization
    void Start () {
        currentTest = listOfTests[0];
        Invoke("ExitSandbox", 90f);
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
        this.conveyerBelt.SetActive(true);
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
            print("calling next test");
            if (this.currentTest.GetComponent<NumberPad>().testDone || this.isFirstTest)
            {
                if (this.isFirstTest)
                {
                    this.conveyorTop.GetComponent<Animator>().Play("ConveyorMove");
                }
                this.isFirstTest = false;
                print("test on its way");
                currentTest = listOfTests[0];
                currentTest.SetActive(true);
                listOfTests.RemoveAt(0);
                currentTest.SendMessage("Enter");
            }
        }
        if(listOfTests.Count == 0)
        {
            //Test is done, put finishing code here!
        }
    }

    private void SubmitCurrentTest()
    {
       // this.currentTest.SetActive(false);
    }
}
