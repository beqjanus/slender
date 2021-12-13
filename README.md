# Slender
Second Life Blender Tools

This is a Blender Addon designed to help me manage my Second Life and OpenSim builds. I am releasing it publicly in the hope that it might help others and improve workflows.
Open Sim note: This tools is designed to work with SecondLife viewer uploads, as such it is compatible with OpenSim and I will use the term SecondLife as meaning any derivative of Second Life. 
The notable exceptions to this are aspects such as Land Impact where the equations/rules for Land Impact are not enforced or are calculated differently. 

Tested on 2.8-2.93 so far.

## Key features
* Land Impact prediction. 
There are two aspects to this the "headline" feature is the Land Impact prediction.
  1) At present it can estimate the streaming cost for Second Life. which unless you are trying to do crazy stuff with the physics should be the dominant feature. NB: It is an estimation.
  2) It shows the cost ratio of each triangle in the LOD (at the scale applied in Blender). This is an accurate predictor of how important to the overall LI a given LOD is. Using this you can optimise the LODs in Blender with more confidence around the final import cost.

* Level Of Detail Management. 
The Second Life Viewer upload expects a Collada file (.DAE) for each Level of Detail (LOD), and for those files to represent the same scene/object as seen at a given level of fidelity. Thus if your scene is composed of 4 objects then the High LOD Collada file, will have 4 objects, the Medium LOD Collada file will have 4 objects etc. down to and including the physics file. There are strict naming conventions that allow the viewer to precisely identify which object is which in each LOD and make sure that they are correctly mapped during the import. If no match is found then it falls back to a far less robust "guessing" mode.

  Using SLender, we identify the models by placing them in the appropriate collection. If you follow the workflow that I use then they will be named correctly; this is the area that I expect the most discussion on as I expect many people to have very different ways of working, and thus I may need to find better ways to associate models with one another.

  With the objects organised, we can then export some or all objects in the scene at the click of a button, producing all the relevant LOD files, all named correctly for immediate import into SL.

* Material inspector. 
Historically, and for those on older viewers (currently) mesh import required that all LODs for a given model shared the exact same set of materials. I fixed this in Firestorm so that a true subset is now allowed. However, tracking the usage of materials, ensuring that you have the same materials assigned in each LOD is still useful.

* Simple cleanup
It can do some very basic cleanup of mesh exported via the the "Save As ... Collada" option in Third-Party viewers such as Firestorm. These functions are typically just easy access buttons to standard Blender Tools.

## Current Status
This is the first release. This was designed for me with my workflows in mind. As such it will be perfect for a few of you, useful to some of you, and a total pain in the arse to the rest. I hope that a number of the simple features will be useful more generally, with the export tools perhaps being the area I expect most contention over. 

What I'd like to hear back is where those rough edges are, how thoughts and ideas of how they can be made to work better for you.
## Is this really free? How much is this?
It is free of cost and will remain so, these tools are built upon Blender and the amazing community and, as such respect the licensing of Blender and are contributed in the hope that others will find these useful.

If you like the tools and feel like showing your appreciation then you are very welcome to send me a donation and appreciated, it is in no way expected/required (nor will it get you any special attention).


### In terms of managing expectations.
All work that I do on these tools is entirely voluntary, and it has to sit behind my primary volunteer effort as one of the small team of developers that bring you the Firestorm viewer; all voluntary work in turn is secondary to RL work and family. Support is not actively given, please raise a github issue, you will often find me in various inworld SecondLife builders groups and increasingly in the breakaway groups on discord such as Blender Benders.

## ROADMAP - Future idealistic thoughts

This is not so much a road map as an unsorted list of ideas.

* Use geometry nodes/modifiers to manage the LOD decimation.
The way that I tend to use this is to create an initial model that becomes the HIGH LOD. from there I clone it into the MED and start to simplify, then repeat this for the LOW and finally the LOWEST/IMPOSTER.
With geometry nodes the opportunity to automate some of the general simplification in a non-destructive manner is forming and as time allows I hope to be able to allow you to specify operations to simplify a mesh when the LOD is created from the parent.

* Create a shader setup that gives near Second Life shading look and feel
The SecondLife shaders are not PBR, SL Materials are "special" in the way in which the image 

* Add exact Land Impact Prediction
Calculate the Land Impact more accurately by replicating the internal asset format, thus knowing the correct size

* Add Mesh Validation to avoid import error in the viewer.
Support equivalent checks to those in the viewer.

* Add closer integration with the viewer
Inworld preview is the goal.

* Add imposter creation
Support Imposter creation using simple camera setups.

* Support gltf or other export
This is a stretch goal for sure as this requires me to do extensive work on the viewer as well.

* RAW land from mesh export
I actually wrote this code last year for my Fantasy Faire build, I just need to ~~weaponise~~ turn it into an addon.




