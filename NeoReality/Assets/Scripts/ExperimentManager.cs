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


    // Use this for initialization
    void Start () {
        Invoke("ExitSandbox", 10);
        print("end of start");
	}

    private void FixedUpdate()
    {
        if (turnningOff)
        {
            light1.GetComponent<Light>().intensity -= 0.0005f;
            light2.GetComponent<Light>().intensity -= 0.0005f;
        }
        if (turnningOn)
        {
            light1.GetComponent<Light>().intensity += 0.0005f;
            light2.GetComponent<Light>().intensity += 0.0005f;
        }
    }

    private void ExitSandbox()
    {
        print("Invoke method exit called.");
        turnningOff = true;
        print("inital value: " + light1.GetComponent<Light>().intensity);
        Invoke("OpenTests", 10);
    }

    private void OpenTests()
    {
        turnningOff = false;
        turnningOn = true;
        print("new value: " + light1.GetComponent<Light>().intensity);
        print("opening tests");
        //table.SetActive(false);
        //playObj1.SetActive(false);
        //playObj2.SetActive(false);
        //playObj3.SetActive(false);
        Invoke("TurnOffBrightness", 10);
    }

    private void TurnOffBrightness()
    {
        this.turnningOn = false;
    }
}
