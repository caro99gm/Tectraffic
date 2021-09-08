// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python
// Sergio. Julio 2021
// Actualizado Lorena Mtz E. Agosto 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class AgentController : MonoBehaviour
{
    List<List<Vector3>> positions;
    public GameObject[] prefabs;
    public GameObject luzRoja;
    public GameObject luzVerde;


    public int clonesOfAgent1;
    public int clonesOfAgent2;

    GameObject[] agents;
    GameObject[] semaforos;
    Vector3[] positionSem;

    public float timeToUpdate = 1.0f;
    private float timer;
    float dt;
    bool newPos = false;

    // IEnumerator - yield return
    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";   //El puerto debe coincidir con el del server
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            //www.SetRequestHeader("Content-Type", "text/html");
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log(www.downloadHandler.text);    // Answer from Python
                //Debug.Log("Form upload complete!");
                //Data tPos = JsonUtility.FromJson<Data>(www.downloadHandler.text.Replace('\'', '\"'));
                //Debug.Log(tPos);
                List<Vector3> newPositions = new List<Vector3>();
                string txt = www.downloadHandler.text.Replace('\'', '\"');
                txt = txt.TrimStart('"', '{', 'd', 'a', 't', 'a', ':', '[');
                txt = "{\"" + txt;
                txt = txt.TrimEnd(']', '}');
                txt = txt + '}';
                string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
                Debug.Log("strs.Length:"+strs.Length);
                for (int i = 0; i < strs.Length; i++)
                {
                    strs[i] = strs[i].Trim();
                    if (i == 0) strs[i] = strs[i] + '}';
                    else if (i == strs.Length - 1) strs[i] = '{' + strs[i];
                    else strs[i] = '{' + strs[i] + '}';
                    Vector3 test = JsonUtility.FromJson<Vector3>(strs[i]);
                    newPositions.Add(test);
                }

                int sumAgents = clonesOfAgent1 + clonesOfAgent2;
                List<Vector3> poss = new List<Vector3>();
                for(int s = 0; s < sumAgents; s++)
                {
                    //spheres[s].transform.localPosition = newPositions[s];
                    poss.Add(newPositions[s]);
                }
                positions.Add(poss);
                Debug.Log("Agregamos un set de posisiones nuevas.");
                Debug.Log("Set de posiciones: " + positions.Count);
                Debug.Log("El set tiene "+positions[0].Count);
                //Debug.Log("Y la primera es: "+positions[0][0].ToString);
                /*for(int i = 0; i < positions.Count; i++)
                {
                    for(int j = 0; j < positions[i].Count; j++){
                        Debug.Log(positions[i]);
                    }
                    
                }*/
            }
        }

    }

    // Start is called before the first frame update
    void Start()
    {
        agents = new GameObject[clonesOfAgent1];
        for (int i = 0; i < clonesOfAgent1; i++)
        {
            agents[i] = Instantiate(prefabs[UnityEngine.Random.Range(0, 4)], Vector3.zero, Quaternion.identity);
        }

        positionSem = new[] { new Vector3(21.0f, 7.0f, 28.0f), new Vector3(27.0f, 7.0f, 40.0f), new Vector3(32.0f, 7.0f, 22.0f), new Vector3(38.0f, 7.0f, 34.0f) };
        semaforos = new GameObject[clonesOfAgent2];
        for (int i = 0; i < clonesOfAgent2; i++)
        {
            semaforos[i] = Instantiate(luzRoja, positionSem[i], Quaternion.identity);
        }

        positions = new List<List<Vector3>>();
        Debug.Log(agents.Length);
#if UNITY_EDITOR
        //string call = "WAAAAASSSSSAAAAAAAAAAP?";
        Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        string json = EditorJsonUtility.ToJson(fakePos);
        //StartCoroutine(SendData(call));
        StartCoroutine(SendData(json));
        timer = timeToUpdate;
#endif
    }

    // Update is called once per frame
    void Update()
    {
        /*
         *    5 -------- 100
         *    timer ----  ?
         */
        timer -= Time.deltaTime;
        //Debug.Log(timer);
        dt = 1.0f - (timer / timeToUpdate);

        if(timer < 0.2 && newPos == false)
        {
            newPos = true;
#if UNITY_EDITOR    //https://docs.unity3d.com/Manual/PlatformDependentCompilation.html
            Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine(SendData(json));
#endif
        }

        if (timer < 0)
        {
            newPos = false;
#if UNITY_EDITOR    //https://docs.unity3d.com/Manual/PlatformDependentCompilation.html
            timer = timeToUpdate; // reset the timer
#endif
        }


        if (positions.Count > 1)
        {
            int c = 0;
            int agentSum = clonesOfAgent1 + clonesOfAgent2;
            for (int s = 0; s < agentSum; s++)
            {
                // Get the last position for s
                List<Vector3> last = positions[positions.Count - 1];

                // Get the previous to last position for s
                List<Vector3> prevLast = positions[positions.Count - 2];

                if (s < clonesOfAgent1)
                {
                    // Interpolate using dt
                    Vector3 interpolated = Vector3.Lerp(prevLast[s] * 4.0f, last[s] * 4.0f, dt);  //https://docs.unity3d.com/ScriptReference/Vector3.Lerp.html
                    agents[s].transform.localPosition = interpolated;
                    //if (interpolated.magnitude != 1)
                    //{
                    //    //agents[s].transform.position = interpolated;
                    //    Debug.Log("hola");
                    //} else
                    //{
                    //    agents[s].transform.localPosition = interpolated;
                    //}
                    //apuntar en direccion
                    Vector3 dir = last[s] * 4.0f - prevLast[s] * 4.0f;
                    if (dir != Vector3.zero) agents[s].transform.rotation = Quaternion.LookRotation(dir);
                } 
                else
                {
                    Destroy(semaforos[c]);
                    if (last[s].x == 1)
                    {
                        semaforos[c] = Instantiate(luzVerde, positionSem[c], Quaternion.identity);
                    } 
                    else
                    {
                        semaforos[c] = Instantiate(luzRoja, positionSem[c], Quaternion.identity);
                    }
                    c++;
                }





            }
        }
    }
}
