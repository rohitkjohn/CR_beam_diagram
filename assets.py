# This file stores the assets. Assets includes shapes and figures like the cantilever figure
#---------------------------------------------------------------------------------- cantilever shape

import numpy as np
from Solver import *


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CL_bc_plot
def CL_bc_plot(beam_len, BC = "L"):
    '''
    returns list of dictionaries which describes the cantilever.
    This will be passed into the layout of the figure describing the beam
    beam_len: This is the lenght of the beam
    BC: gives the position of the cantilever support
    '''
    # y1 and y2 are the  arrays which store the y  position of the 6 diagonal lines in
    # cantilever support
    x1 = beam_len/20                                    # x position of one end of the 6 lines
    y1 = [i*beam_len/10 for i in [2,1,0,-1,-2,-3]]
    y2 = [i*beam_len/10 for i in [3,2,1,0,-1,-2]]
    # This array stores all data for rendering the diagonal lines
    if BC == 'L':# This defines the cantilever support on the left hand side
        cantilever_support_shape = [ 
                                    # The vertical line joining (0,4) to (0,-4)
                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': 0,
                                        'y0': 4,
                                        'x1': 0,
                                        'y1': -4,
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': -x1,
                                        'y0': y1[1-1],
                                        'x1': 0,
                                        'y1': y2[1-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': -x1,
                                        'y0': y1[2-1],
                                        'x1': 0,
                                        'y1': y2[2-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': -x1,
                                        'y0': y1[3-1],
                                        'x1': 0,
                                        'y1': y2[3-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': -x1,
                                        'y0': y1[4-1],
                                        'x1': 0,
                                        'y1': y2[4-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': -x1,
                                        'y0': y1[5-1],
                                        'x1': 0,
                                        'y1': y2[5-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': -x1,
                                        'y0': y1[6-1],
                                        'x1': 0,
                                        'y1': y2[6-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    } 
                                   ]


    elif BC == 'R':# This defines the cantilever support on the right hand side
        cantilever_support_shape = [
                                    # The vertical line joining (beam_len,4) to (beam_len,-4)
                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len,
                                        'y0': 4,
                                        'x1': beam_len,
                                        'y1': -4,
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len + x1,
                                        'y0': y1[1-1],
                                        'x1': beam_len,
                                        'y1': y2[1-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len + x1,
                                        'y0': y1[2-1],
                                        'x1': beam_len,
                                        'y1': y2[2-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len + x1,
                                        'y0': y1[3-1],
                                        'x1': beam_len,
                                        'y1': y2[3-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len + x1,
                                        'y0': y1[4-1],
                                        'x1': beam_len,
                                        'y1': y2[4-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len + x1,
                                        'y0': y1[5-1],
                                        'x1': beam_len,
                                        'y1': y2[5-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    },

                                    {
                                        'type': 'line',
                                        'xref': 'x',
                                        'yref': 'y',
                                        'x0': beam_len + x1,
                                        'y0': y1[6-1],
                                        'x1': beam_len,
                                        'y1': y2[6-1],
                                        'line': {
                                                'color': 'rgb(0, 0, 0)',
                                                'width': 3,
                                                },
                                    } 
                                   ]
    beam = {
            'type': 'rect',
            'xref': 'x',
            'yref': 'y',
            'x0': 0,
            'y0': -beam_len/100,
            'x1': beam_len,
            'y1': beam_len/100,
            'line': {
                    'color': 'rgb(55, 128, 191)',
                    'width': 3,
                    },
            'fillcolor': 'rgba(55, 128, 191, 0.6)',
            }
    cantilever_support_shape = cantilever_support_shape + [beam]
    return cantilever_support_shape
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CL_bc_plot
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SSB_plot
def SSB_bc_plot(beam_len, pin_pos, roller_pos):
    '''
    returns the simpy support beam figure
    This will be passed into the layout of the plot describing the beam figure
    beam_len: the lenght of the beam
    pin_pos: position of the pin 
    roller_pos: position of the roller
    '''
    simple_support_shape = [
                            {#-------------------------------------The roller
                                'type':"circle",
                                'xref':"x",
                                'yref':"y",
                                'x0': roller_pos - beam_len/60,
                                'y0': -beam_len/20 -beam_len/100,
                                'x1': roller_pos + beam_len/60,
                                'y1': -beam_len/100,
                                'line_color':"LightSeaGreen",
                            },
                            {#-------------------------------------The beam
                                'type': 'rect',
                                'xref': 'x',
                                'yref': 'y',
                                'x0': 0,
                                'y0': -beam_len/100,
                                'x1': beam_len,
                                'y1': beam_len/100,
                                'line': {
                                        'color': 'rgb(55, 128, 191)',
                                        'width': 3,
                                        },
                                'fillcolor': 'rgba(55, 128, 191, 0.6)',
                            },
                            {#-------------------------------------Pin
                                'type': 'line',
                                'xref': 'x',
                                'yref': 'y',
                                'x0': pin_pos,
                                'y0': -beam_len/100,
                                'x1': pin_pos - beam_len/40,
                                'y1': -beam_len/100 - 0.869*beam_len/20,
                                'line': {
                                        'color': 'rgb(0, 0, 0)'
                                        },
                            },
                            {
                                'type': 'line',
                                'xref': 'x',
                                'yref': 'y',
                                'x0': pin_pos - beam_len/40,
                                'y0': -beam_len/100 - 0.869*beam_len/20,
                                'x1': pin_pos + beam_len/40,
                                'y1': -beam_len/100 - 0.869*beam_len/20,
                                'line': {
                                        'color': 'rgb(0, 0, 0)'
                                        },
                            },
                            {
                                'type': 'line',
                                'xref': 'x',
                                'yref': 'y',
                                'x0': pin_pos,
                                'y0': -beam_len/100,
                                'x1': pin_pos + beam_len/40,
                                'y1': -beam_len/100 - 0.869*beam_len/20,
                                'line': {
                                        'color': 'rgb(0, 0, 0)'
                                        },
                            }
                           ]
    return simple_support_shape
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SSB_plot
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< arrow
def arrow(head_x, head_y, tail_x, tail_y, head_scale = 0.1, width = 1, head_angle = 45):
    ''' returns a list which describes an arrow which is rendered in a plot
        This will be passed into the layout of the plot describing the beam figure
        heax_x: x position of the bead
        head_y: y position of the bead
        tail_x: x position of the tail
        tail_y: y position of the tail
        head_scale: Defines the size of the head
        width: defines the thickness of the lines
        head_angle: the angle between the arrow head arms 
    '''
    rot = np.array([
                      [np.cos(np.pi*(head_angle/180)), -np.sin(np.pi*(head_angle/180))],
                      [np.sin(np.pi*(head_angle/180)), np.cos(np.pi*(head_angle/180))]
                     ])
    rot_t = np.transpose(rot)
    arrow_arm_1 = [x*head_scale for x in rot.dot(np.array([tail_x - head_x, tail_y - head_y]))]
    arrow_arm_2 = [x*head_scale for x in rot_t.dot(np.array([tail_x - head_x, tail_y - head_y]))]

    arr_shape = [
                {# This defines the body
                'type': 'line',
                'xref': 'x',
                'yref': 'y',
                'x0': head_x,
                'y0': head_y,
                'x1': tail_x,
                'y1': tail_y,
                'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': width,
                        },
                 },

                {# This defines the arrow head arm 1
                'type': 'line',
                'xref': 'x',
                'yref': 'y',
                'x0': head_x,
                'y0': head_y,
                'x1': head_x + arrow_arm_1[0],
                'y1': head_y + arrow_arm_1[1],
                'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': width,
                        },
                 },

                {# This defines the arrow head arm 1
                'type': 'line',
                'xref': 'x',
                'yref': 'y',
                'x0': head_x,
                'y0': head_y,
                'x1': head_x + arrow_arm_2[0],
                'y1': head_y + arrow_arm_2[1],
                'line': {
                        'color': 'rgb(0, 0, 0)',
                        'width': width,
                        },
                 },
                 ]

    return arr_shape
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> arrow

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< circular arrow
def dirc_arrow(cen_x, cen_y, rx, ry, no_pts, dir = 'CCW'):
    '''
    returns a list of x coordinates and y coordinates which will plot the circular
    arrow.
    This will be passed into the data for the beam figure
    cen_x: X coordinate of the centre
    cen_y: y coordinate of the centre
    rx: radius in the x direction (major axis)
    ry: radius in the y direction (minor axis)
    no_pts: number of points in the polygon describing the arrow
    dir: The direction of the arrow: CCW - counter clock wise, CW - clock wise
    '''
    if dir == 'CW':
        theta = np.linspace(2.5*np.pi, np.pi, no_pts)
    elif dir == 'CCW':
        theta = np.linspace(0.5*np.pi, 2*np.pi, no_pts)
    
    x = [cen_x + rx*np.cos(i) for i in  theta]
    y = [cen_y + ry*np.sin(i) for i in  theta]
    x = x + [x[-1], x[-1] - rx/2, x[-1], x[-1] + rx/2]
    y = y + [y[-1] + ry/2, y[-1], y[-1] + ry/2, y[-1]]
    return x,y
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> circular arrow
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< distributed force marker
def dist_force_marker_func(x_start, x_end, mag_start, mag_end, max_mag, beam_lenght):
    '''
    returns x_list, y_list which defines the distributed force
    This will be passed into the data for the beam figure
    x_start: This is the start of the distributed force
    x_end: This is the end of the distributed force
    mag_start: This is the magnitude of the force at the start
    mag_end: This is the magnitude of the force at the end 
    max_mag: This is the maximum magnitude of all distributed forces in the data table
    beam_lenght: This is the beam length
    '''
    y_max = beam_lenght/2.5
    y_start = (mag_start/max_mag) * y_max
    y_end = (mag_end/max_mag) * y_max

    if mag_start == 0:
        x_pts = [
                x_start, x_start, x_end, x_end, 
                x_end - beam_lenght/80, x_end, x_end + beam_lenght/80, 
                ]
        if mag_end > 0:
            y_pts = [
                    beam_lenght/100, y_start, y_end, beam_lenght/100, 
                    beam_lenght/20, beam_lenght/100, beam_lenght/20,
                    ]

        else:
            y_pts = [
                    beam_lenght/100, y_start, y_end, beam_lenght/100, 
                    -beam_lenght/20, beam_lenght/100, -beam_lenght/20, 
                    ]

    elif mag_end == 0:
        x_pts = [
                x_start - beam_lenght/80, x_start, x_start + beam_lenght/80, 
                x_start, x_start, x_end, x_end
                ]
        if mag_start > 0:
            y_pts = [
                    beam_lenght/20, beam_lenght/100, beam_lenght/20, 
                    beam_lenght/100, y_start, y_end, beam_lenght/100
                    ]

        else:
            y_pts = [
                    -beam_lenght/20, beam_lenght/100, -beam_lenght/20, 
                    beam_lenght/100, y_start, y_end, beam_lenght/100
                    ]

    else:
        x_pts = [
                x_start - beam_lenght/80, x_start, x_start + beam_lenght/80, 
                x_start, x_start, x_end, x_end, 
                x_end - beam_lenght/80, x_end, x_end + beam_lenght/80, 
                ]

        if mag_start > 0:
            if mag_end > 0:
                y_pts = [
                        beam_lenght/20, beam_lenght/100, beam_lenght/20,
                        beam_lenght/100, y_start, y_end, beam_lenght/100,
                        beam_lenght/20, beam_lenght/100, beam_lenght/20,
                        ]
            elif mag_end < 0:
                y_pts = [
                        beam_lenght/20, beam_lenght/100, beam_lenght/20,
                        beam_lenght/100, y_start, y_end, beam_lenght/100,
                        -beam_lenght/20, beam_lenght/100, -beam_lenght/20,
                        ]
        elif mag_start < 0:
            if mag_end > 0:
                y_pts = [
                        -beam_lenght/20, beam_lenght/100, -beam_lenght/20,
                        beam_lenght/100, y_start, y_end, beam_lenght/100,
                        beam_lenght/20, beam_lenght/100, beam_lenght/20,
                        ]
            elif mag_end < 0:
                y_pts = [
                        -beam_lenght/20, beam_lenght/100, -beam_lenght/20,
                        beam_lenght/100, y_start, y_end, beam_lenght/100,
                        -beam_lenght/20, beam_lenght/100, -beam_lenght/20,
                        ]


    return x_pts, y_pts

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> distributed force marker