# Molecule-Viewer
Ability to add/remove and view molecules using the localhost server

1:mol.c/mol.h backend 

2:C to pyhton code via swig(molecule.i) and python code(Moldisplay.py) to create svg files from sdf

3:SQL databse in python

4:server+frondend via HTTP,HTML,CSS,JAVASCRIPT,DOM,AJAX

Assignment Description/Requirements
Add/remove elements from the system:
Design an interface that allows users to add and
remove elements from the system. Users should be able to specify the element number,
element code, element name, 3 colour values, and radius of an element. It is not required to be
able to edit element values, you can always remove one and replace it with a new one. There
should be a default set of colours and radius for any elements contained in molecules that do
not have an entry in the system. It should not be possible for the user to enter malicious
parameters for the element that can damage the system.

Upload sdf files to the system:
Design an interface that allows users to upload sdf files to the
system. Invalid sdf files should be detected, and an error message generated. It should not be
possible to damage the system with a malicious sdf file. Upon uploading an sdf file, the user
should be informed of success. The user should be able to assign the molecule contained in the
sdf file a name (a malicious name should not be able to damage the system).
Select from a list of molecules. Design an interface that allows users to select one of the
molecules that is in the system. Inform the user of the number of atoms and bonds that are in
the molecule before they select it.

Upload sdf files to the system:
Design an interface that allows users to upload sdf files to the
system. Invalid sdf files should be detected, and an error message generated. It should not be
possible to damage the system with a malicious sdf file. Upon uploading an sdf file, the user
should be informed of success. The user should be able to assign the molecule contained in the
sdf file a name (a malicious name should not be able to damage the system).
Select from a list of molecules. Design an interface that allows users to select one of the
molecules that is in the system. Inform the user of the number of atoms and bonds that are in
the molecule before they select it.

Display a selected molecule:
Display a selected molecule showing all the atoms as shaded
spheres according to the element table. Implement a method to change the angle of the
molecule (without reloading the entire web-page page).
Navigate between pages. Design a method to navigate between the different functions listed
above.
