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


    // Use this for initialization
    void Start () {
        Invoke("ExitSandbox", 10);
        print("end of start");
	}

    private void ExitSandbox()
    {
        print("Invoke method exit called.");
        print("inital value: " + light1.GetComponent<Light>().intensity);
        while (light1.GetComponent<Light>().intensity > 0) {
            light1.GetComponent<Light>().intensity = Mathf.MoveTowards(0.3f, 0f, Time.deltaTime);
            light2.GetComponent<Light>().intensity = Mathf.MoveTowards(0.3f, 0f, Time.deltaTime);
        }
        Invoke("OpenTests", 10);
    }

    private void OpenTests()
    {
        print("new value: " + light1.GetComponent<Light>().intensity);
        print("opening tests");
        //table.SetActive(false);
        //playObj1.SetActive(false);
        //playObj2.SetActive(false);
        //playObj3.SetActive(false);
        Mathf.Lerp(0, 0.3f, Time.deltaTime);
        Mathf.Lerp(0, 0.3f, Time.deltaTime);
    }
}
