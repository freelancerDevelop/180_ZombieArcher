﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

// Description: 
// Decrements the zombies health when an arrow contacts the zombie
// Removes the zombie from the game environment when the zombie runs out of health
public class ZombieHealth : MonoBehaviour {

    // Public variables
    public int damagePerShot = 20;      // How much damage each arrow deals to zombie
    public int startingHealth = 100;    // Starting health of zombie
    public int currentHealth;           // Current health of zombie
    public int scoreValue = 10;         // Score increase for each zombie hit
    //public AudioClip deathClip;       // TODO: Sound zombie makes when dies

    // Private variables
    //AudioSource zombieAudio;            // Audio source for zombie
    //ParticleSystem hitParticles;      // TODO: Will contain blood
    //CapsuleCollider capsuleCollider;    // Capsule collider for zombie
    

	// Use this for initialization
	void Awake () {
        //zombieAudio = GetComponent<AudioSource>();
        //hitParticles = GetComponentInChildren<ParticleSystem>(); // TODO: Find particle system
        //capsuleCollider = GetComponent<CapsuleCollider>();         // Get reference to capsule collider
        currentHealth = startingHealth;                            // Initialize current health
	}
	
	// Update is called once per frame
	void Update () {

	}

    void OnTriggerEnter(Collider other)
    {
        // If an arrow is in the capsule collider
        if (other.gameObject.tag == "Arrow")
        {
            // Deal damage to zombie
            ZombieTakeDamage(damagePerShot);
        }
    }

    void ZombieTakeDamage(int amount)
    {
        // TODO: Play zombie audio when zombie is damaged
        //zombieAudio.Play();

        //Decrement zombie health
        currentHealth -= amount;

        // Increase the player's score
        ScoreManager.score += amount;

        // TODO: Display blood
        //hitParticles.Play();

        // If the current health is less than 0, zombie is dead
        if(currentHealth <= 0)
        {
            Death();
        }

    }

    void Death()
    {

        //TODO: Set zombie audio to deathclip
        //zombieAudio.clip = deathClip;

        //TODO: Play zombie death audio
        //zombieAudio.Play();

        // Turn off mesh agent component to get zombie to stop following player
        GetComponent<NavMeshAgent>().enabled = false;

        // Remove zombie from game environment
        Destroy(gameObject, 1);


    }

}
