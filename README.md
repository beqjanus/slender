# Slender
Second Life Blender Tools

This is a Blender Addon designed to help me manage my Second Life and OpenSim builds. I am releasing it publicly in the hope that it might help other and improve workflows.

Tested on 2.8-2.9 so far.

## What does it do? 
SLender does a number of things not all of which sit together in the same place logically.
It can help do some very basic clean up of mesh that has been exported using Firestorm's SaveAs Collada mechanism (it may of course work for other viewers but I have not tested them)

It's primary purpose is to help manage the multiple models that are required for LODs and to correctly export them for a streamlined (one click) load into the Firestorm/Second Life Mesh Uploader
Objects are managed in a series of collections and exported using the full and proper naming rules for SecondLife that ensures proper matching occurs in the uploader.

Additionally it will report on the materials that are in use in related models to confirm that that are an appropriate subset of the designnated HIGH LOD model. 

## Future idealisitc thoughts
The way that I tend to use this is to create an initial model that becomes the HIGH LOD. from there I clone it into the MED and start to simplify, then repeat this for the LOW and finally the LOWEST/IMPOSTER.
With geometry nodes the opportunity to automate some of the general simplification in a non-destructive manner is forming and as time allows I hope to be able to allow you to specify operations to simpify a mesh when the LOD is created from the parent.

## How much is this?
It is free and will remain so. All work that I do on this is entirely voluntary and has to slip in between RL work and family, Firestorm development and other things...
If you like the tools and feel like showing your appreciation then you are very welcome to send me a donation, it is in no way expected.
