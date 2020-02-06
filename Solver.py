#Import the necessary packages
import sympy as sp
import numpy as np

#  force_sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< force_sum
def force_sum(forces, x, x1):
    """ 
    returns the sum of all forces from -1 to x1
    forces: item or list: is the list of all the forces that acts on the beam, these as 
    functions
    x: symbol:  is the variable/ argument of the functions which represent the force
    x1: symbol or value: is a point along the beam. This function calculates the total force acting 
    on the beam for -1 < x <= x1 
    """   
    
    # This variable stores the sum of all the force
    sum = 0

    # The following block checks whether the second input is a symbol or not----------------------------Check input
    if not isinstance(x, sp.Symbol):
        print("force_sum error: the second argument is not a symbol. Check")
        return

    if not isinstance(x1,sp.Symbol):
        if x1 <= 0:
            print("force_sum error: the third input is not greater than 0, check")
            return 

    if isinstance(forces, list):

        for f in forces:
            if isinstance(f, list):
                print("force_sum error: the input is a list of list. Check the input")
                return
            # this block checks if the input is a proper list of expression.
            # It returns
            # an error if the input is a list of list.
    #---------------------------------------------------------------------------------------------------\Check input

        for f in forces:
            # as mentioned earlier, this function calculates the sum of all
            # forces from
            # -1 to x1.
            # Why -1?  That is because the reaction force acts at x = 0 and it
            # is defined
            # by a dirac delta function and integral(diracDelta(x), from 0 to
            # inf) has a
            # definition which we cannot use meaningfully
            sum = sum + sp.integrate(f,[x, -1, x1])

        return sum

    # the following block is used when the input is just a single function
    sum = sum + sp.integrate(forces,[x, -1, x1])
    return sum
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> force_sum
# moment_sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< moment_sum
def moment_sum(moments, forces, x, x1):
    """ 
    returns the sum of all moments from -1 to x1
    moments: item or list: is the list of all the moments that acts on the beam, these as 
    functions
    forces: item or list: is the list of all the forces
    x: symbol: is the variable/ argument of the functions which represent the moment
    x1: symbol or value: is a point along the beam. This function calculates the total moment acting 
    on the beam for -1 < x <= x1 
    """   
    
    # This variable stores the sum of all the moment---------------------------------------------Check input
    sum = 0

    # The following block checks whether the third input is a symbol or not
    if not isinstance(x, sp.Symbol):
        print("moment_sum error: the third argument is not a symbol. Check")
        return
        
    if not isinstance(x1,sp.Symbol):
        if x1 <= 0:
            print("moment_sum error: the fourth input is not greater than 0, check")
            return 
    #------------------------------------------------------------------------------------------\Check input
    if isinstance(moments, list):
            #-----------------------------------------------------------------------------------Check input
        for m in moments:
            if isinstance(m, list):
                print("moment_sum error: the input -moments- is a list of list. Check the input")
                return
            # this block checks if the input is a proper list of expression.
            # It returns
            # an error if the input is a list of list.

            #----------------------------------------------------------------------------------\Check input

        for m in moments:
            # as mentioned earlier, this function calculates the sum of all
            # moments from
            # -1 to x1.
            # Why -1?  That is because the reaction moment acts at x = 0 and it
            # is defined
            # by a dirac delta function and integral(diracDelta(x), from 0 to
            # inf) has a
            # definition which we cannot use meaningfully
            sum = sum + sp.integrate(m,[x, -1, x1]) # here x is the running 
            # variable for the integration

    # This line gets the moment if only one moment is input into the system
    else:
        sum = sum + sp.integrate(moments,[x, -1, x1])

    if isinstance(forces, list):

        for f in forces:
            # this adds the moment due to the forces acting on the beam-----------------------------Check input
            if isinstance(f, list):
                print("moment_sum error: the input -forces- is a list of list. Check the input")
                return
            # this block checks if the input is a proper list of expression.
            # It returns
            # an error if the input is a list of list.
            
            #--------------------------------------------------------------------------------------\Check input

        for f in forces:
                sum = sum + sp.integrate(f*(x1 - x), [x, -1, x1])        
        # returns the moment after adding all the moments and the moment due to shear
        return sum

    # the following block is used when the input is just a single function
    else:
        sum = sum + sp.integrate(forces*(x1 - x),[x, -1, x1])
        return sum
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> moment_sum
# cantilever_solver <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< cantilever_solver
def cantilever_solver(moments,forces, torques, x, len, BC = 'L'):
    """ returns F_reaction, M_reaction, T_reaction
    the reaction force and the reaction moment and reaction torque at the 
    forces: item or list: this is the list of forces acting on the beam
    moment: item or list: this is the list of moments acting on the beam
    x: symbol: This is the variable/argument of the functions defing the forces and moments
    len: value or symbol: This is the lenght of the beam
    BC: 0 or 1: it is the location of the boundary condition, 0 -> left & 1 -> right
    """

    # the following block of code checks the input-------------------------------------input checking
    if not isinstance(x, sp.Symbol):
        print("cantilever_solver error: the fourth argument is not a symbol, chech")
        return

    if not isinstance(len,sp.Symbol):
        if len <= 0:
            print("cantilever_solver error: the fifth input is not greater than 0, check")
            return 

    if isinstance(forces, list):
        for f in forces:
            if isinstance(f, list):
                print("cantilever_solver error: the first argument is not a proper list check the input")
                return


    if isinstance(moments, list):
        for f in moments:
            if isinstance(f, list):
                print("cantilever_solver error: the second argument is not a proper list check the input")
                return

    if isinstance(torques, list):
        for f in torques:
            if isinstance(f, list):
                print("cantilever_solver error: the third argument is not a proper list check the input")
                return

    #--------------------------------------------------------------------------------------------\input checking
    
    # This line calculates the reaction force applied by the cantilever wall on the beam
    # To find this, integrate all the forces from -1 to len +1. The beam lies in the closed
    # interval [0, len], and if a point force where to act at the ends, the result would have a
    # heaviside(0) term which is not defined. So to avoid this integrate in the interval [-1, len + 1]
    # This does not change anything as there will be no force outside the beam

    F_reaction = -force_sum(forces, x, len + 1) 
    T_reaction = -force_sum(torques, x, len + 1) 

    # Moment is found by using the fact that the moment beyond the end of the beam is 0
    if BC == 'L':
        M_reaction = -moment_sum(moments, forces, x, len + 1) - F_reaction*(len + 1)

    elif BC == 'R':
        M_reaction = -moment_sum(moments, forces, x, len + 1) - F_reaction*(1)   
        
    else:
        print("cantilever_solver error: the sixth input (BC) is neither 1 nor 0")
        return

    return F_reaction, M_reaction, T_reaction
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cantilever_solver
# simply supported beam solver <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< simply supported beam solver
def simply_supported_solver(moments,forces, x, len, f1_loc = "blah", f2_loc = "blah"):
    """ returns f_left, f_right,
    the the two reactions at the two ends
    forces: item or list: this is the list of forces acting on the beam
    moment: item or list: this is the list of moments acting on the beam
    x: symbol: This is the variable/argument of the functions defing the forces and moments
    len: value or symbol: This is the lenght of the beam
    """
    # the following block of code checks the input-------------------------------------input checking
    if not isinstance(x, sp.Symbol):
        print("simply_supported_solver error: the third argument is not a symbol, chech")
        return

    if not isinstance(len,sp.Symbol):
        if len <= 0:
            print("simply_supported_solver error: the third input is not greater than 0, check")
            return 

    if isinstance(forces, list):
        for f in forces:
            if isinstance(f, list):
                print("simply_supported_solver error: the first argument is not a proper list check the input")
                return


    if isinstance(moments, list):
        for f in moments:
            if isinstance(f, list):
                print("simply_supported_solver error: the second argument is not a proper list check the input")
                return

    #--------------------------------------------------------------------------------------------\input checking

    #--------------------------------------------------------------------------------------------- pins position
    if f1_loc == "blah":
        f1_loc = 0

    if f2_loc == "blah":
        f2_loc = len

    # f1 and f2: symbols: they represent the two normal reactions at the end
    # of the beam
    f1,f2 = sp.symbols('f1,f2')

    # This is the sum of the forces on the beam and the moments at x+1
    eq1 = f1 + f2 + force_sum(forces, x, len + 1)
    eq2 = (1 + len - f1_loc)*f1 + (1 + len - f2_loc)*f2 + moment_sum(moments, forces, x, len + 1 )

    # solving eq1 and eq2
    eqs = [eq1, eq2]
    sol = sp.linsolve(eqs, (f1, f2))

    # assigning the solutions to variable f_left for f1 and f_right for f2
    f_left, f_right = sol.args[0]

    return f_left, f_right
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> simply supported beam solver
# list_eval <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< list_eval
def list_eval(f, x, l):
    """
    retunrs a list. It evaluates the expression f for an array list.
    The function handles the heaviside(0) as 1
    f: expression: the expression to be evaluated
    x: symbol: the symbol in the expression
    list: the list which is to be substituted 
    """
    ans = np.array([])

    for i in l:

        ans = np.append(ans, float(sp.N((f.subs(x,i)).replace(sp.Heaviside(0), sp.Heaviside(0,1)))))


    return ans
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> list_eval
# PW_lerp <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PW_lerp
def PW_lerp(x1, y1, x2, y2, x):
    '''
    Piece wise linear interpolation
    returns a linear interpolation in the symbol x between the points (x1, y1) and (x2, y2) 
    in the closed interval [x1, x2]. It is zero outside the interval [x1, x2]
    x1: x position of the first point
    y1: y position of the first point
    x2: x position of the second point
    y2: y position of the second point
    x: the symbolic argument of the function which defines the interpolation
    '''
    if x1 == x2:
        print('PW_lerp error: x1 and x2 passed to this function are equal. Check input')
        return

    poly_1 = y1*( (x - x2) / (x1 - x2))
    poly_2 = y2*( (x - x1) / (x2 - x1))
     
    if x1 < x2:
        ans = sp.Piecewise( 
                           (0.0, x < x1),
                           (0.0, x > x2),
                           (poly_1 + poly_2, True)
                          )

    if x2 < x1:
        ans = sp.Piecewise( 
                           (0.0, x < x2),
                           (0.0, x > x1),
                           (poly_1 + poly_2, True)
                          )

    return ans
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PW_lerp
# dist_shear <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< dist_shear
def dist_shear(x1, y1, x2, y2, x):
    '''
    returns returns the shear function of a distributed load
    in the closed interval [x1, x2]. It is zero outside the interval [x1, x2]
    x1: x position of the first point
    y1: load of the first point
    x2: x position of the second point
    y2: load of the second point
    x: the symbolic argument of the function which defines the interpolation
    '''
    if x1 == x2:
        print('dist_shear error: x1 and x2 passed to this function are equal. Check input')
        return

    if x1 < x2:
        ans = sp.Piecewise(
                            (-((x1 - x2)*(y1 + y2))/2.0, x > x2),
                            (0,                          x < x1),
                            (((x - x1)*(x*y1 + x1*y1 - 2*x2*y1 - x*y2 + x1*y2))/(2.0*(x1 - x2)), True)
                          )
    if x2 < x1:
        ans = sp.Piecewise(
                            (-((x1 - x2)*(y1 + y2))/2.0, x > x1),
                            (0,                          x < x2),
                            (((x - x2)*(x*y1 + x2*y1 - 2*x1*y1 - x*y2 + x2*y2))/(2.0*(x2 - x1)), True)
                          )
    return ans
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> dist_shear
# dist_moment <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< dist_moment
def dist_moment(x1, y1, x2, y2, x):
    '''
    returns returns the bending moment function of a distributed load
    in the closed interval [x1, x2]. It is zero outside the interval [x1, x2]
    x1: x position of the first point
    y1: load of the first point
    x2: x position of the second point
    y2: load of the second point
    x: the symbolic argument of the function which defines the interpolation
    '''
    if x1 == x2:
        print('dist_moment error: x1 and x2 passed to this function are equal. Check input')
        return

    if x1 < x2:
        ans = sp.Piecewise(
                            (((x1 - x2)*(-3*x*(y1 + y2) + x1*(2*y1 + y2) + x2*(y1 + 2*y2)))/6.0,  x > x2),
                            (0,                          x < x1),
                            ((((x1 - x)**2)*(-3*x2*y1 + x*(y1 - y2) + x1*(2*y1 + y2)))/(6.*(x1 - x2)), True)
                          )
    if x2 < x1:
        ans = sp.Piecewise(
                            (((x2 - x1)*(-3*x*(y1 + y2) + x2*(2*y1 + y2) + x1*(y1 + 2*y2)))/6.0,  x > x1),
                            (0,                          x < x2),
                            ((((x2 - x)**2)*(-3*x1*y1 + x*(y1 - y2) + x2*(2*y1 + y2)))/(6.*(x2 - x1)), True)
                          )
    return ans
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> dist_moment