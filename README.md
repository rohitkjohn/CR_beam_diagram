# Beam loading simulator
This containes the code for the web app which produces the shear and bending moment diagram of a beam subjected to external loads. There are three main parts: the Solver, the assets and the app.  The web app is given below:

https://cr-beam-loads.herokuapp.com/

The Solver contains functions which calculates the internal shear force, the internal moments, and the reaction loads. It can solve for a cantilever and a simply supported beam. The solver accepts loads a symbolic functions defined using sympy library and calculates the answer analylically. This ensures that the calculations have zero error. On the other hand, the solver becomes slow as the number of input loads increases. This may be mitigated using a numerical solver and this is suggested for future work. The solver can accept any kind of load as long as it can be analytically defined. 

The app containes the code for generating a web based graphical user interface. The user is able to select between two types of beams -  Cantilever and simply supported beam - and specify the dimension and support for the beam. Three types of loads can be placed on the beam : point force, point moment, and linear distributed force. Clicking the submit button adds the specified load into the load data table. Within the load data table, the user is able to modify the load and also remove it. Finally the update button calculates the internal loads and displays the external loads and internal loads in a figure.

For a cantilever the reaction loads were calculated by:

![first equation](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cdpi%7B120%7D%20F_%7B%5Ctext%20%7B%20reaction%20%7D%7D%3D-%5Cint_%7B0%7D%5E%7BL%7D%28%5Ctext%20%7B%20forces%20%7D%28x%29%29%20d%20x)

![second equation](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cdpi%7B120%7D%20M_%7B%5Ctext%20%7B%20reaction%20%7D%3D%7D-%5Cint_%7B0%7D%5E%7BL%7D%28%5Ctext%20%7B%20force%20%7D%20*%28L-x%29&plus;%5Ctext%20%7B%20moments%20%7D%29%20d%20x-F_%7B%5Ctext%20%7B%20reaction%20%7D%7D%20*%28L%29)

For the simply supported beam the reaction loads were calculated by:

![third equation](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cdpi%7B120%7D%20F_%7B%5Cmathrm%7Bpin%7D%7D&plus;F_%7B%5Cmathrm%7Broller%7D%7D%3D-%5Cint_%7B0%7D%5E%7BL%7D%28%5Coperatorname%7Bforces%7D%28%5Cboldsymbol%7Bx%7D%29%29%20%5Cboldsymbol%7Bd%7D%20%5Cboldsymbol%7Bx%7D)

![fourth equation](http://latex.codecogs.com/gif.latex?%5Cinline%20%5Cdpi%7B120%7D%20F_%7B%5Ctext%7Bpin%7D%7D%20%5Cleft%28L-x_%7B%5Ctext%7Bpin%7D%7D%5Cright%29&plus;F_%7B%5Ctext%7Broller%7D%7D%20%5Cleft%28L-x_%7B%5Ctext%7Broller%7D%7D%5Cright%29%3D-%5Cint_0%5EL%20%28%5Ctext%7Bforce%7D%20%28L-x%29&plus;%5Ctext%7Bmoments%7D%29%20%5C%2C%20dx)

The assets file contains the functions used to define the beam figure and the load markers.
