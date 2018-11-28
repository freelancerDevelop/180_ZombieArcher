using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Gun : MonoBehaviour {

    public Rigidbody bullet;
    public int bulletspeed;
    public Transform barrel;

    void SpawnBullet() {
        Rigidbody b;
        b = Instantiate(bullet, new Vector3(barrel.position.x, barrel.position.y, barrel.position.z), barrel.rotation) as Rigidbody;
        b.AddForce(b.transform.forward * bulletspeed);

    }
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {

        if (Input.GetButtonDown("Fire1")) { 
            SpawnBullet();
        }
	}
}
