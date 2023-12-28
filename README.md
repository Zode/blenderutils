Target blender version: 4.0

# Features
## Materials
### Goldsrc
* Import images & setup nodes for materials (chromes are automatically set up too)
### Common
* Turn material between diffuse and matcap (with optional additive or transparent mode)
* EZ one stop shop for texture baking
* classic vertex weighting (hit shift+q in weight paint mode)
* keybind to toggle custom weight gradient (hit ctrl+shift+q)
### Edit mode
* In vertex menu: New option "Vertex bones: make from selected" which will take the selected vertices, and make a proxy object & armature with said vertices rigged into bones controlled by the original mesh's vertices. Effectively allowing one to turn vertex animation into bone animation for goldsrc and others.
* In object menu: New option: "Vertex bones: make from selected" which will do the above, but on object level.

#  Installing & Updating
## Installing
Happens as any blender addon would, grab the master (not the release) as a .zip and slap it in blender
## Updating
The addon now includes automatic update checking. No need to hassle with that stuff anymore!

## Vertex bones:
a placeholder until the303 provides an article:

**note that a goldsrc skeleton cannot exceed 128 total bones**

for the edit mode vertex option:
1. Animate your model and save your project file
2. In edit mode select your vertices, and go `vertex` -> `Vertex bones: make from selected`
3. Put the playhead back at the beginning and select the newly created proxy armature, and set it to "rest mode"
4. Set up your BST paths, then with only proxy mesh selected export the reference SMD
If this is on an existing armature, like in cases of facial animation, parent the vertexbones to the proxy headbone
5. Set the "rest mode" in the proxy armature back to "pose mode" and in pose mode go to `Pose` -> `Animation` -> `Bake action` and set the time range.
**Note that you may need to enable visual keying in some situations**
6. Select only the animation in BST exportables list and export  
7. Compile model