import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table as dt

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

import sympy as sp
import numpy as np
import pandas as pd

from Solver import *
from assets import *

external_stylesheets = ['style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Initialisation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Initialisation
length_beam = 10 #[m] This is the initial lenght of the beam

# ..Load table <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Load table
# This initialises the table
loads_table = {
                'type':['point moment', 'point force','distributed force'],
                'point position':[1,4,np.nan],
                'point value':[2,2,np.nan],
                'start value':[np.nan,np.nan,2],
                'end value':[np.nan,np.nan,5],
                'start position':[np.nan,np.nan,1],
                'end position':[np.nan,np.nan,2]
              }

loads_df = pd.DataFrame(loads_table)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Load table
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Initialisation
# Setup  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Setup
# ..Buttons <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Buttons
#----------------------------------------------------------------------------------------------------------- Help popup display button
# Clicking this button displays the help popup
button_Help = html.Div([
                       html.Button(
                                  id = 'open_help', 
                                  children = 'Help!',
                                  style = {
                                          'marginTop' : '10px',
                                          'marginBottom' : '5px',
                                          'fontSize':'200%'
                                          },
                                  )],
                                className = 'row'
                                )
# A separate button for each force stype is used because, a single button would then require inputs from
# all the input text fields. However when a the load type is selcted, the remain load specification text
# boxes are not present in the webpage, so when the callback is activated, the function will have 
# insuficient argument (other argument inputs do not exist) raising an error. This is solved using one 
# button for each load type   
#----------------------------------------------------------------------------------------------------------- Submit button for distributed force
# This button triggers the callback which stores the distributed
# text field as a hidden table
button_DF = html.Div([
                      html.Button(
                                 id = 'submit_button_DF', 
                                 n_clicks = 0, 
                                 children = 'Submit',
                                 style = {'marginTop': '10px', 'marginBottom': '10px'}
                                 )
                     ],
                     id = 'submit_button_DF_div',
                     className = 'row'
                    ) 
#----------------------------------------------------------------------------------------------------------- Submit button for point force
#This button triggers the callback which stores the point force text field as a hidden table. 
button_PF = html.Div([
                      html.Button(
                                 id = 'submit_button_PF', 
                                 n_clicks = 0, 
                                 children = 'Submit',
                                 style = {'marginTop': '10px', 'marginBottom': '10px'},
                                 )
                     ],
                     id = 'submit_button_PF_div',
                     className = 'row'
                    )
#----------------------------------------------------------------------------------------------------------- Submit button for point moment
# This button triggers the callback which stores the point moment 
# text field as a hidden table
button_PM = html.Div([
                       html.Button(
                                  id = 'submit_button_PM', 
                                  n_clicks = 0, 
                                  children = 'Submit',
                                  style = {'marginTop': '10px', 'marginBottom': '10px'}
                                  )
                     ],

                     id = 'submit_button_PM_div',
                     className = 'row'
                    )
#----------------------------------------------------------------------------------------------------------- Update button to update graph
# This button updates the graph with the data given in the
# data table
button_update_graph = html.Div([
                               html.Button(
                                          id = 'update_graph_button',
                                          n_clicks = 0,
                                          children = 'Update',
                                          style = {'marginTop': '10px', 'marginBottom': '10px'}
                                          )
                               ],
                               id = 'update_button_div',
                               className = 'row'
                              ) 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Buttons
# ..Data tables <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data table
#----------------------------------------------------------------------------------------------------------------- Loads Data Table
# This division contains the table which displays the loads acting
# on the beam 
col = []
for i in loads_df.columns:
    if i == 'type':
        col = col + [{"name": i, "id": i, "deletable": True}]
    else:
        col = col + [{"name": i, "id": i, "deletable": True, 'type': 'numeric'}]

loads_data_table = dt.DataTable(
                               id = 'loads_data_table',
                               columns = col,
                               data = loads_df.to_dict('records'),
                               editable = True,
                               row_deletable = True,
                               selected_rows = [],
                               style_table = {
                                             'minWidth': '0px',
                                             'whiteSpace': 'normal', 
                                             'maxHeight': '240px',
                                             #'maxWidth': '600px',
                                             #'overflowX': 'scroll', 
                                             #'overflowY': 'scroll',
                                             },
                               #filter_action = "native",
                               #sort_action = "native",
                               #sort_mode = "multi",
                               #row_selectable = "multi",
                               )
#----------------------------------------------------------------------------------------------------------------- Division 1.2.1
# This stores the container which will store the data table
data_table_div = html.Div([
                            loads_data_table
                          ],
                          className = 'row',
                          style = {'overflowY': 'scroll'}
                          )
#----------------------------------------------------------------------------------------------------------------- HIDDEN division (forces)
# This is a hidden contained which stores the point force loads acting on the
# beam. This is updated when the callback is triggered by the button used for  
# adding point force. 
hidden_point_point_force_table_Div =  html.Div([
                                                dt.DataTable(
                                                            id = 'hidden_PF_table',
                                                            columns = [ {"name": i, "id": i, "deletable": True} for i in loads_df.columns ],
                                                            data = [],
                                                            ),
                                               ],
                                               style={'display': 'none'}
                                               )
#----------------------------------------------------------------------------------------------------------------- HIDDEN division (moments)
# This is a hidden contained which stores the point moment loads acting on the
# beam. This is updated when the callback is triggered by the button used for  
# adding point moment. 
hidden_point_point_moment_table_Div = html.Div([
                                                dt.DataTable(
                                                            id = 'hidden_PM_table',
                                                            columns = [ {"name": i, "id": i, "deletable": True} for i in loads_df.columns ],
                                                            data = [],
                                                            ),
                                               ],
                                               style={'display': 'none'}
                                               )
#----------------------------------------------------------------------------------------------------------------- HIDDEN division (distributed force)
# This is a hidden contained which stores the distributed force acting on the
# beam. This is updated when the callback is triggered by the button used for  
# adding distributed force. 
hidden_point_dist_force_table_Div = html.Div([
                                              dt.DataTable(
                                                          id='hidden_DF_table',
                                                          columns = [ {"name": i, "id": i, "deletable": True} for i in loads_df.columns ],
                                                          data=[{'a':1,'b':2}],
                                                          ),
                                             ],
                                             style={'display': 'none'}
                                            )
#----------------------------------------------------------------------------------------------------------------- HIDDEN division (Cantilever specs) 
# This table stores the specification of the cantilever. The graph updater callback will need input from the 
# cantilever specification and simply supported beam specification. At a time only one of these inputs will be 
# displayed so the updater function will have a missing argument. To bypass this issue this hidden table is
# is taken as one of the inputs. It will exist is the page (but is hidden) so it can be called anytime.
# The CL input callback will input data into this hidden table.  
hidden_CL_def_table = html.Div([
                                dt.DataTable(
                                            id = 'hidden_CL_table',
                                            columns = [
                                                        {"name":'lenght', "id":'lenght'},
                                                        {"name":'BC', "id":'BC'}
                                                      ], #BC => Boundary condition
                                            data = [{"length":10, "BC":'L'}]
                                            )
                               ],
                               style={'display': 'none'}
                              )
#----------------------------------------------------------------------------------------------------------------- HIDDEN division (Simply supported beam specs) 
# This table stores the specification of the cantilever. The graph updater callback will need input from the 
# cantilever specification and simply supported beam specification. At a time only one of these inputs will be 
# displayed so the updater function will have a missing argument. To bypass this issue this hidden table is
# is taken as one of the inputs. It will exist is the page (but is hidden) so it can be called anytime.
# The SSB input callback will input data into this hidden table.
hidden_SSB_def_table = html.Div([
                                dt.DataTable(
                                            id = 'hidden_SSB_table',
                                            columns = [
                                                        {"name":'lenght', "id":'lenght'},
                                                        {"name":"pin", "id":'pin'}, 
                                                        {"name": "roller", "id": "roller"}
                                                      ], #BC => Boundary condition
                                            data = [{"length":10, "pin":0, "roller":5}]
                                            )
                                ],
                                style={'display': 'none'}
                               )
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Data table
# ..Drop down  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Drop down
#----------------------------------------------------------------------------------------------------------------- beam selector dropdown
# This defines the dropdown box which is used to select the type
# of beam i.e. Cantilever or Simply Supported Beam 
beam_selector_dropdown = dcc.Dropdown(
                                     options = [
                                               {'label': 'Cantiliver', 'value': 'CL'},
                                               {'label': 'Simply Supported beam', 'value': 'SSB'}
                                               ],
                                     value ='CL',
                                     id = 'beam_selector',
                                     clearable = False
                                     )
#----------------------------------------------------------------------------------------------------------------- Division 1.1.1
# This defines the HTML container which will displace the beam selector dropdown 
beam_selector_Div = html.Div([
                              html.Label('Select beam'),
                              beam_selector_dropdown,
                             ],
                             className = 'row',
                             )
#----------------------------------------------------------------------------------------------------------------- force selector dropdown
# This defines the dropdown box which is selects the type of 
# force to be added to the load data table 
force_selector_dropdown = dcc.Dropdown(
                                      options = [
                                                {'label': 'Point force', 'value': 'PF'},
                                                {'label': 'Point Moment', 'value': 'PM'},
                                                {'label': 'Distributed Force', 'value': 'DF'}
                                                ],
                                      value ='PF',
                                      id = 'force_selector',
                                      clearable = False
                                      )
#----------------------------------------------------------------------------------------------------------------- Division 1.2.1
# This defines the HTML container which will store the force selector dropdown
force_selector_div = html.Div([
                               html.Label('Select Loads'),
                               force_selector_dropdown,
                              ],
                              className = 'row',
                              )
#----------------------------------------------------------------------------------------------------------------- Division 1.2.2
# This defines the container which will store the force specification input boxes
# This division will have its own load definition input, and a submit button
# These are defined in the callback. Each submit button triggers and event 
# which stores the data. So there will be 3 callbacks, for each load type
# However, an output (in this case the datatable) cannot be modified by
# by more than one callbacks. To tackle this, each load storing call back
# stores its output data in a hidden table. When any of this hidden table
# is modified, the main table is modified
force_specs_div = html.Div(
                          id = 'force_spec_input_boxes'
                          )
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Drop down
# ..Input text boxes <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Input text boxes
#----------------------------------------------------------------------------------------------------------- Point force Magnitude division
# This defines the text input box which accepts the magnitude of the point force
input_PF_mag = html.Div([
                         html.P(
                               'Point Force magnitude [N]',
                               style = {'marginTop': '10px', 'marginBottom': '1px'}
                               ),
                         dcc.Input(
                                  id = 'Point_force_mag', 
                                  value = 1, 
                                  type = 'number'
                                  )
                        ],
                        className = 'six columns',
                        )
#----------------------------------------------------------------------------------------------------------- Point force Position division
# This defines the text input box which accepts the position of the point force
input_PF_pos = html.Div([
                         html.P(
                               'Point Force position [m]',
                               style = {'marginTop': '10px', 'marginBottom': '1px'}
                               ),
                         dcc.Input(
                                  id = 'Point_force_pos', 
                                  value = 0, 
                                  type = 'number'
                                  )
                         ],
                         className = 'six columns',
                        )
#----------------------------------------------------------------------------------------------------------- Point moment Magnitude division
# This defines the text input box which accepts the magnitude of the point moment
input_PM_mag = html.Div([
                         html.P(
                               'Point moment magnitude [N m]',
                               style = {'marginTop': '10px', 'marginBottom': '1px'}
                               ),
                         dcc.Input(
                                  id = 'Point_moment_mag', 
                                  value = 1, 
                                  type = 'number'
                                  )
                        ],
                        className = 'six columns',
                        )
#----------------------------------------------------------------------------------------------------------- Point moment Position division
# This defines the text input box which accepts the position of the point moment
input_PM_pos = html.Div([
                         html.P(
                               'Point moment position [m]',
                               style = {'marginTop': '10px', 'marginBottom': '1px'}
                               ),
                         dcc.Input(
                                  id = 'Point_moment_pos', 
                                  value = 0, 
                                  type = 'number'
                                  )
                        ],
                        className = 'six columns',
                        )
#----------------------------------------------------------------------------------------------------------- Distributed force start position
# This defines the input text box which accepts the start position
# of the deistributed force.
input_DF_start_pos = html.Div([
                               html.P(
                                     'Start position',
                                     style = {'marginTop': '10px', 'marginBottom': '1px'}
                                     ),
                               dcc.Input(
                                        id = 'dist_start_pos', 
                                        value = '0', 
                                        type = 'number'
                                        )
                              ],
                              className = 'three columns',
                              )
#----------------------------------------------------------------------------------------------------------- Distributed force end position
# This defines the input text box which accepts the end position
# of the deistributed force.
input_DF_end_pos = html.Div([
                             html.P(
                                   'End position',
                                   style = {'marginTop': '10px', 'marginBottom': '1px'}
                                   ),
                             dcc.Input(
                                      id = 'dist_end_pos', 
                                      value = 1, 
                                      type = 'number'
                                      )
                            ],
                            className = 'three columns',                         
                            )
#----------------------------------------------------------------------------------------------------------- Distributed force start magnitude
# This defines the input text box which accepts the start magnitutde
# of the deistributed force
input_DF_start_mag = html.Div([
                               html.P(
                                     'Start magnitude',
                                     style = {'marginTop': '10px', 'marginBottom': '1px'}
                                     ),
                               dcc.Input(
                                        id = 'dist_start_mag', 
                                        value = 0, 
                                        type = 'number'
                                        )
                              ],
                              className = 'three columns',
                              )
#----------------------------------------------------------------------------------------------------------- Distributed end start magnitude
# This defines the input text box which accepts the énd magnitutde
# of the deistributed force
input_DF_end_mag = html.Div([
                             html.P(
                                   'End magnitutde',
                                   style = {'marginTop': '10px', 'marginBottom': '1px'}
                                   ),
                             dcc.Input(
                                      id = 'dist_end_mag', 
                                      value = 1, 
                                      type = 'number'
                                      )
                            ],
                            className = 'three columns',                            
                            )
#----------------------------------------------------------------------------------------------------------- Cantilever length
# This input accepts the length of the cantilever beam
input_beam_lenght_CL = html.Div([
                              html.P(
                                    'Length of beam [m]',
                                    style = {'marginTop': '10px', 'marginBottom': '1px'}
                                    ),
                              dcc.Input(
                                       id = 'beam_len_CL', 
                                       value = 10, 
                                       type = 'number'
                                       )  
                             ],
                             className = 'six columns'
                            )
#----------------------------------------------------------------------------------------------------------- Simply supported beam leam
# This input accepts the length of the simply supported beam
input_beam_lenght_SSB = html.Div([
                                  html.P(
                                        "Beam length",
                                        style = {'marginTop': '10px', 'marginBottom': '1px'}
                                        ),
                                  dcc.Input(
                                           id = 'beam_len_SSB', 
                                           value = 10, 
                                           type = 'number'
                                           ) 
                                 ],
                                 className = 'four columns'
                                )
#----------------------------------------------------------------------------------------------------------- Simply supported beam pin pos
# This input accepts the position of the pin joint of the
# simply supported beam
input_SSB_pin = html.Div([
                          html.P(
                                "Pin position",
                                style = {'marginTop': '10px', 'marginBottom': '1px'}
                                ),
                          dcc.Input(
                                   id = 'pin_pos', 
                                   value = 3, 
                                   type = 'number') 
                         ],
                         className = 'four columns'
                        )
#----------------------------------------------------------------------------------------------------------- Simply supported beam roller pos
# This impot accepts the position of the roller support of 
# the simply supported beam
input_SSB_roller = html.Div([
                             html.P(
                                   "roller position",
                                   style = {'marginTop': '10px', 'marginBottom': '1px'}
                                   ),
                             dcc.Input(
                                       id = 'roll_pos', 
                                       value = 6, 
                                       type = 'number'
                                      ) 
                            ],
                            className = 'four columns'
                           )
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Input text boxes
# ..Other Containers <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Other Containers
#----------------------------------------------------------------------------------------------------------------- Division 1.1.2
# This stores the container which will display the inputs for defining
# the beam 
beam_definition_Div = html.Div(
                              id = 'beam_definition',
                              className = 'row'
                              )
#----------------------------------------------------------------------------------------------------------------- Division 1.1.3
# This stores the container which will display the graph 
figure_Div = html.Div(                        
                     id = "graph_div",
                     className = 'row',
                     )
#----------------------------------------------------------------------------------------------------------------- Horizontal line
# This stores the definition of a horizontal line
hori_line = html.Hr(
                   style = {
                           'marginTop': '5px', 
                           'marginBottom': '5px'
                           }
                   )
#----------------------------------------------------------------------------------------------------------------- Message
# This stores the definition of the division which will display the output messages
message_div = html.Div(
                      id = 'message', 
                      children = "Updating",
                      style = {
                              'marginTop': '10px',
                              "border" : "1px solid black",
                              'backgroundColor':'#dadee6',
                              'textAlign' : 'center'
                              }
                      )
#----------------------------------------------------------------------------------------------------------------- Help Popup
# This is the help popup division
help_popup_div = html.Div([  # modal div
                          html.Div([  # content div
                                   html.Div([
                                            '''Step 1: Choose the type of beam from the 'Select beam' dropdown box''',
                                            html.Br(),
                                            '''Step 2: Specify the beam length and choose the position of the support 
                                            for a cantilever or specify the position of the pin and roller supports''',
                                            html.Br(),
                                            '''Step 3: Add loads. Select the type of load using the select loads 
                                            dropdown box and specify the load''',
                                            html.Br(),
                                            '''Step 4: Click submit button to add the load in the Loads data table''',
                                            html.Br(),
                                            '''Step 5: Edit the loads in the Loads data table if required. To edit a 
                                            value double click the field, edit the value and press enter. To remove a
                                            load, click the small 'x' button in the first column''',
                                            html.Br(),
                                            '''Step 6: Click the update button to update the figure''',
                                            html.Br(),
                                            '''If there are errors they will be shown above or under the figure''',
                                            html.Br(),
                                            '''The code for this app can be found '''
                                            ,html.A('here', href='https://github.com/rohitkjohn/CR_beam_diagram')
                                            ],
                                            style = {'textAlign' : 'left'}
                                           ),
                                   html.Hr(),
                                   html.Button('Close', id='modal-close-button')
                                   ],
                                   style = {'textAlign': 'center'},
                                   className = 'modal-content',
                                  ),
                          ],
                          id = 'modal',
                          className = 'modal',
                          style = {"display": "none"},
                        )
#----------------------------------------------------------------------------------------------------------------- Message update triggers
# The message updates corresponding to three events: initial loading, updating the graph and loading completed.
# These events are triggered by: loading the webpage, clicking the update button and graph update completed. 
# These events update the corresponding hidden Divs and this act of updating provides the stimulus to update
# the message. Since more than one callback cannot have the same output, these hidden Divs serve as proxies
# which are triggered by different callbacks and change in any of these will trigger the message callback   
hidden_div_Loading = html.Div(id = 'Loading', children = '0', style={'display': 'none'})
hidden_div_Updating = html.Div(id = 'Updating', children = '0', style={'display': 'none'})
hidden_div_Complete = html.Div(id = 'Complete', children = '0', style={'display': 'none'})
hidden_div_data_error = html.Div(id = 'data_error', children = '0', style={'display': 'none'})
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Other Containers
# ..Radio button <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Radio button
#------------------------------------------------------------------------------------------------ Cantilever support position radio button
# This radio button is used to set the position of the fixed end of
# the cantilever
radio_CL_boundary = html.Div([
                              html.P(
                                    'Select position of boundary',
                                    style = {'marginTop': '10px', 'marginBottom': '1px'}
                                    ),
                              dcc.RadioItems(
                                             options = [
                                                        {'label':'Left', 'value': 'L'},
                                                        {'label':'Right', 'value': 'R'}
                                                       ],
                                             value = 'L',
                                             labelStyle = {'display':'inline-block'},
                                             id = 'radio_CL_BC',                                             
                                             ),                       
                              ],
                              className = 'six columns'
                              )
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Radio button
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Setup
# Webpage design <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Webpage design
app.layout = html.Div([ # ---------------------------------------------------------------------------------Division 1                
                      html.Div([ # ------------------------------------------------------------Division 1.1
                               button_Help,
                               beam_selector_Div,#-------------------------------Division 1.1.1
                               beam_definition_Div,#-----------------------------Division 1.1.2                               
                               hori_line,#_________________________________________________________
                               force_selector_div,#-----------------------------Division 1.2.1
                               force_specs_div,#--------------------------------Division 1.2.2
                               hori_line,#_________________________________________________________
                               data_table_div,#---------------------------------Division 1.2.4                               
                               button_update_graph,#----------------------------Division 1.2.5
                               help_popup_div

                               ],
                               className = 'seven columns',
                              ),

                      html.Div([ # ------------------------------------------------------------Division 1.2
                               message_div,
                               figure_Div,
                               ],
                               className = 'five columns',
                              ),

                     html.Div([ # ------------------------------------------------------------ Hidden Division 1.2
                               hidden_point_point_force_table_Div,#------- Hidden Division 1.2.1
                               hidden_point_point_moment_table_Div,#------ Hidden Division 1.2.2
                               hidden_point_dist_force_table_Div,#-------- Hidden Division 1.2.3
                               hidden_CL_def_table,#---------------------- Hidden Division 1.2.4
                               hidden_SSB_def_table,#--------------------- Hidden Division 1.2.5
                               hidden_div_Loading,
                               hidden_div_Updating,
                               hidden_div_Complete,
                               hidden_div_data_error
                              ],
                               className = 'row',
                              )
                     ],
                      className = 'row',
                     )
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Webpage design
# Interactivity <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Interactivity
app.config['suppress_callback_exceptions'] = True # This makes sure crazy call backs can be done
# ..Beam selector interaction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Beam selector interaction
# This callback is used to select the type of beam: catilever or simply supported
@app.callback(
             Output('beam_definition', 'children'),
             [Input('beam_selector', 'value')]
             )

def update_beam_def(input_value):
    # This function checks what beam type is selected and output the children
    # which will populate the division between the beam selector dropdown box 
    # and the force selector sropdown box
    if input_value == 'CL': # This corresponds to choosing a cantilever
        child = [
                input_beam_lenght_CL,
                radio_CL_boundary                
                ]

    if input_value == 'SSB': # This corresponds to choosing a simply supported beam
        child = [
                input_beam_lenght_SSB,
                input_SSB_pin,
                input_SSB_roller,
                ]
    return child
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Beam selector interaction
# ..Load selector interaction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Load selector interaction
# This callback accpets the state of the force_selector dropdown box
# and returns a division with the appropriate input boxes
@app.callback(
             Output('force_spec_input_boxes', 'children'),
             [Input('force_selector', 'value')]
             )
def update_output_div(input_value):
    # This function checks the type of load selected and output the children
    # (input boxes) which will populate the space between the dropdown box 
    # and the table

    if input_value == None:
        child = [
                 input_PF_mag,
                 input_PF_pos,
                 button_PF,
                ]

    if input_value == 'PF': # This corresponds to selecting a point load
        child = [
                 input_PF_mag,
                 input_PF_pos,
                 button_PF,
                ]

    if input_value == 'PM': # This corresponds to selecting a point moment
        child = [
                 input_PM_mag,
                 input_PM_pos,
                 button_PM
                ]
    if input_value == 'DF': # This corresponds to selecting a distributed force
        child = [
                 input_DF_start_pos,
                 input_DF_end_pos,
                 input_DF_start_mag,
                 input_DF_end_mag,
                 button_DF,
                ]
    return child
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Load selector interaction
# ..Load addition interaction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Load addition interaction
#----------------------------------------------------------------------------------------------------------------- Data table updater
# This is triggered when any of the hidden tables are updated. This callback takes the new 
# information put into the hidden tables and updates the main data table
@app.callback(
             [
              Output('loads_data_table', 'data'),
              Output('data_error', 'children')
             ],
             [
              Input('hidden_PF_table','data'),
              Input('hidden_PM_table','data'),
              Input('hidden_DF_table','data')
             ],
             [
              State('force_selector', 'value'),
              State('loads_data_table', 'data'),
              State('hidden_CL_table','data'),
              State('hidden_SSB_table', 'data'),
              State('beam_selector', 'value'),
             ]
            )

def update_table(PF, PM, DF, force_sel, loads_data_table, CL_data, SSB_data, beam_type):
    # if the force selection dropdown box is empty 
    if force_sel == None:
        return loads_data_table
    
    # This gets the beam lenght. This is used to eliminate the values which are out of
    # bound 
    if beam_type == "CL":
        beam_len = float(CL_data[0]['length'])
    elif beam_type == "SSB":
        beam_len = float(SSB_data[0]['length'])
    
    # This stores all the error messages
    error_msg = '0'

    # This checks the input values and returns to the hidden div if it is acceptable
    if force_sel == 'PF':
        if PF != []:
            cond1 = (float(PF[0]['point position']) > beam_len)
            cond2 = (float(PF[0]['point position']) < 0.0)
            if cond1 or cond2:
                data = loads_data_table
                error_msg = 'Error: Point force position out of bound. Check value of position'
            else:
                if float(PF[0]['point value']) == 0.0:
                    data = loads_data_table
                    error_msg = 'Error: Point force magnitude entered should not be 0'
                else:
                    data = loads_data_table + PF
        else:
            data = loads_data_table     

    if force_sel == 'PM':
        if PM != []:
            cond1 = (float(PM[0]['point position']) > beam_len)
            cond2 = (float(PM[0]['point position']) < 0.0)
            if cond1 or cond2:
                data = loads_data_table
                error_msg = 'Error: Point moment position out of bound. Check value of position'
            else:
                if float(PM[0]['point value']) == 0.0:
                    data = loads_data_table
                    error_msg = 'Error: Point moment magnitude entered should not be 0'
                else:
                    data = loads_data_table + PM
        else:
            data = loads_data_table

    if force_sel == 'DF':
        
        if DF != []:
            cond1 = (float(DF[0]['start position']) > beam_len)
            cond2 = (float(DF[0]['start position']) < 0.0)
            cond3 = (float(DF[0]['end position']) > beam_len)
            cond4 = (float(DF[0]['end position']) < 0.0)

            if cond1 or cond2 or cond3 or cond4:
                data = loads_data_table
                error_msg = 'Error: Distributed force position out of bound. Check value of position'  
            else:
                cond1 = float(DF[0]['start value']) == 0
                cond2 = float(DF[0]['end value']) == 0
                cond3 = float(DF[0]['start position']) == float(DF[0]['end position'])

                if cond1 and cond2:
                    data = loads_data_table
                    error_msg = 'Error: Distributed force magnitude entered should not be 0'
                elif cond3:
                    data = loads_data_table
                    error_msg = 'Error: Distributed force magnitude start and end position should not be the same'
                else:
                    data = loads_data_table + DF
        else:
            data = loads_data_table + DF
    return data, error_msg
#----------------------------------------------------------------------------------------------------------------- Distributed force acceptor
# This is triggered the submit buttons for distributed force is clicked. This callback takes the distributed force 
# specification values in the text input box and stores it in a hidden table
@app.callback(
             Output('hidden_DF_table','data'),
             [Input('submit_button_DF', 'n_clicks')],
             [
              State('dist_start_pos', 'value'),               
              State('dist_end_pos', 'value'),
              State('dist_start_mag', 'value'),               
              State('dist_end_mag', 'value')
             ]
             )

def load_addition(n_clicks, \
                  dist_start_pos, \
                  dist_end_pos, \
                  dist_start_mag, \
                  dist_end_mag
                  ):
    if n_clicks == 0:
        return []

    new_row = {
              'type':'distributed force',
              'point position' : np.nan,
              'point value' : np.nan,
              'start value' : dist_start_mag,
              'end value' : dist_end_mag,
              'start position' : dist_start_pos,
              'end position' : dist_end_pos
              }
    return [new_row]
#----------------------------------------------------------------------------------------------------------------- Point force acceptor
# This is triggered the Submit button for point force is clicked. This callback takes the point force
# specification values in the text input box and stores it in a hidden table
@app.callback(
             Output('hidden_PF_table', 'data'),
             [Input('submit_button_PF', 'n_clicks')],
             [
              State('Point_force_mag', 'value'),               
              State('Point_force_pos', 'value')
             ]
             )

def load_addition(
                 n_clicks, \
                 Point_force_mag, \
                 Point_force_pos, \
                 ):
    # This callback is called during the webpage loading. This acan add unwanted things into the table. This is
    # avoided using this statement  
    if n_clicks == 0: 
        return []
    
    new_row = {
              'type':'point force',
              'point position' : Point_force_pos,
              'point value' : Point_force_mag,
              'start value' : np.nan,
              'end value' : np.nan,
              'start position' : np.nan,
              'end position' : np.nan
              }
    return [new_row]
#----------------------------------------------------------------------------------------------------------------- Point moment acceptor
# This is triggered the Submit button for point moment is clicked. This callback takes the point moment  
# specification values in the text input box and stores it in a hidden table.
@app.callback(
             Output(component_id = 'hidden_PM_table', component_property='data'),
             [Input('submit_button_PM', 'n_clicks')],
             [
              State('Point_moment_mag', 'value'),               
              State('Point_moment_pos', 'value')
             ]
             )

def load_addition(
                 n_clicks, \
                 Point_moment_mag, \
                 Point_moment_pos, \
                 ):

    # This callback is called during the webpage loading. This acan add unwanted things into the table. This is
    # avoided using this statement  
    if n_clicks == 0:
        return []
    
    new_row = {
              'type':'point moment',
              'point position' : Point_moment_pos,
              'point value' : Point_moment_mag,
              'start value' : np.nan,
              'end value' : np.nan,
              'start position' : np.nan,
              'end position' : np.nan
              }
    return [new_row]
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Load addition interaction
# ..Update graph interaction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Update graph interaction
# The following two callbacks update the hidden tables associated with the cantilever specification data and simply supported beam 
# specification data. Only one beam is specified in the webpage at any instance. However the update graph button need the specs
# of the two types of beams and uses value of the beam selector dropdown to choose which one to display. So hidden tables are used
# to store the beam specs and these are present all the time in the webpage but are not displayed. This way the update graph
# callback can access specs of both types of beams  
#----------------------------------------------------------------------------------------------------------------- store cantilever specification
# This callback updates the hidden cantiliver specification table
@app.callback(
             Output('hidden_CL_table', 'data'),
             [
               Input('beam_len_CL', 'value'),
               Input('radio_CL_BC', 'value')
             ]
             )
def upadate_CL_def_table(len, BC):
    return [{"length":len, "BC":BC}]
#----------------------------------------------------------------------------------------------------------------- store simply supported beam specification
# This callback stores the input data into the hidden simpy supported beam specification table
@app.callback(
               Output('hidden_SSB_table', 'data'),
               [
                 Input('beam_len_SSB', 'value'),
                 Input('pin_pos', 'value'),
                 Input('roll_pos', 'value')
               ]
             )
def update_SSB_def_table(len, pin_pos, roll_pos):
    return [{"length":len, "pin":pin_pos, "roller":roll_pos}]
#----------------------------------------------------------------------------------------------------------------- Displaying graph
@app.callback(
             [
               Output('graph_div', 'children'),
               Output('Updating', 'children')
             ],
             [Input('update_graph_button', 'n_clicks')],
             [  
               State('loads_data_table','data'),
               State('hidden_CL_table','data'),
               State('hidden_SSB_table', 'data'),
               State('beam_selector', 'value'),
             ]
             )

def update_graph(n_clicks, \
                data, \
                CL_data,\
                SSB_data, 
                beam_type,\
                #upd_mess
                ):

    # Initialisation
    def_PF = []         # This stores the magnitude and position of the point force
    def_PM = []         # This stores the magnitude and position of the point moment
    def_DF = []         # This stores the start and end magnitude and start and end position of the distributed force
    force_arrows = []   # This stores the arrows which will represent the point forces
    moment_arrows = []  # This stores the arrows which will represent the point moment
    dist_force_marker = [] # This stores the marker which will represent the distributed force
    refinement = []     # This stores the point where the mesh (discreet data points of beam) is refined to capture discontinuities
    dist_force_max = 0  # This stores the max magnitude of the distributed force. It will be used for scaling
    point_force_max = 0 # This stores the max magnitude of the point force. It will be used for scaling
    point_moment_max = 0# This stores the max magnitude of the point moment. It will be used for scaling
    error_msg = []      # This stores the error messages, if any are detected
    msg = ''            # This stores any general message

    x,y = sp.symbols('x,y')     # These are the symbols which will be used in this function
    point_force_function = 0    # This stores the function which defines all the point forces acting on the beam
    point_moment_function = 0   # This stores the function which defines all the point moment acting on the beam
    dist_force_function = 0     # This stores the function which defines all the distributed force acting on the beam

    # This block of code extracts the lenght of the beam
    if beam_type == "CL":
        beam_len = CL_data[0]['length']

    elif beam_type == "SSB":
        beam_len = SSB_data[0]['length']

    # Extracting the values from the data
    for val in data:
        if val['type'] == 'point force':
            # This condition becomes true when the lenght of the beam is reduced while the data table does not change
            cond1 = float(val['point position']) > beam_len
            if cond1:
                error_msg = error_msg + ['Point Force out of bound: Point value = ' + \
                                            str(val['point value']) + \
                                            ', Point position = ' + \
                                            str(val['point position']) + \
                                            ' Please remove from table\n']

            else:
                def_PF.append([
                              float(val['point value']), 
                              float(val['point position'])
                             ])
                if abs(float(val['point value'])) > point_force_max:
                    point_force_max = abs(float(val['point value']))

        if val['type'] == 'point moment':
            # This condition becomes true when the lenght of the beam is reduced while the data table does not change
            cond1 = float(val['point position']) > beam_len
            if cond1:
                error_msg = error_msg + [
                                         'Point Moment out of bound: Point value = ' + \
                                         str(val['point value']) + \
                                         ', Point position = ' + \
                                         str(val['point position']) + \
                                         ' Please remove from table\n'
                                        ]
            else:
                def_PM.append([
                              float(val['point value']), 
                              float(val['point position'])
                             ])
                if abs(float(val['point value'])) > point_moment_max:
                    point_moment_max = abs(float(val['point value']))

        if val['type'] == 'distributed force':
            cond1 = float(val['start position']) > beam_len
            cond2 = float(val['end position']) > beam_len
            if cond1 or cond2:
                error_msg = error_msg + [
                                        'Distributed Force out of bound: Start position = ' + \
                                        str(val['start position']) + \
                                        ', End position = ' + \
                                        str(val['end position']) + \
                                        '. Please remove from table\n'
                                        ]

            else:
                def_DF.append([
                                  [float(val['start value']), float(val['end value'])], 
                                  [float(val['start position']), float(val['end position'])]
                             ])
                max_mag = max(
                             abs(float(val['start value'])), 
                             abs(float(val['end value']))
                             )
                # The following line is used to find the max value of the distributed force
                # This is used to scale all the other forces so that they can be displayed in the
                # figure  
                if max_mag > dist_force_max:
                    dist_force_max = max_mag

    # This scales the two types of forces relative to each other
    if dist_force_max > point_force_max:
        point_force_max = dist_force_max

    else:
        dist_force_max = point_force_max

    # Load function definition
    # This creates the functions which define the loads acting on the beam and the
    # items which represent the functions in the figure 
    for val in def_PF:
        point_force_function = point_force_function + val[0]*sp.DiracDelta(x - val[1])

        # The following block defines the arrows which will represent the point forces
        if val[0] > 0:
            force_arrows = force_arrows + arrow(
                                               val[1],                                   # x position of the load, X position of the arrow head
                                               beam_len/100,                             # Y position of the arrow head
                                               val[1],                                   # X position of the arrow tail
                                               abs((val[0]/point_force_max)*(beam_len*3/10)), # Y position of the arrow tail
                                               width = 2, 
                                               head_angle = 20, 
                                               head_scale = 0.3
                                               )

        elif val[0] < 0:
            force_arrows = force_arrows + arrow(
                                               val[1],                                    # x position of the load, X position of the arrow head
                                               -beam_len/100,                             # Y position of the arrow head
                                               val[1],                                    # X position of the arrow tail
                                               -abs((val[0]/point_force_max)*(beam_len*3/10)), # Y position of the arrow tail
                                               width = 2, 
                                               head_angle = 20, 
                                               head_scale = 0.3
                                               ) 
           

        # Mesh refinement
        refinement = refinement + [val[1] - 0.000001, val[1] + 0.000001]

    for val in def_PM:
        point_moment_function = point_moment_function + val[0]*sp.DiracDelta(x - val[1])
        # This defines the arrows for the moments
        if val[0] > 0:
            arr_x, arr_y = dirc_arrow(
                                     val[1],                                    # X coordinate of centre
                                     0,                                         # Y coordinate of centre
                                     abs((beam_len/20)*(val[0]/point_moment_max)),   # X radius
                                     abs((beam_len/10)*(val[0]/point_moment_max)),   # Y radius.
                                     # Due to the axis scaling x radius and y radius are note same. This way they appear circular
                                     20,                                        # Number of points
                                     "CCW"                                      # Direction of moment
                                     )
            moment_arrows = moment_arrows + [[arr_x,arr_y]]

        if val[0] < 0:
            arr_x, arr_y = dirc_arrow(
                                     val[1],                                    # X coordinate of centre
                                     0,                                         # Y coordinate of centre
                                     abs((beam_len/20)*(val[0]/point_moment_max)),   # X radius
                                     abs((beam_len/10)*(val[0]/point_moment_max)),   # Y radius.
                                     # Due to the axis scaling x radius and y radius are note same. This way they appear circular
                                     20,                                        # Number of points
                                     "CW"                                      # Direction of moment
                                     )
            moment_arrows = moment_arrows + [[arr_x,arr_y]]
        # Mesh refinement
        refinement = refinement + [val[1] - 0.000001, val[1] + 0.000001]

    for val in def_DF:
        dist_force_function = dist_force_function + PW_lerp(
                                                           val[1][0], val[0][0], #(start pos, start mag)
                                                           val[1][1], val[0][1], #(end pos, end mag)
                                                           x
                                                           )
        arr_x, arr_y = dist_force_marker_func(
                                        val[1][0], 
                                        val[1][1], 
                                        val[0][0], 
                                        val[0][1], 
                                        dist_force_max, 
                                        beam_len
                                        ) # adapt for beam length
        dist_force_marker = dist_force_marker + [[arr_x,arr_y]]
        # Mesh refinement
        refinement = refinement + [val[1][0] - 0.000001, val[1][0] + 0.000001, val[1][1] - 0.000001, val[1][1] + 0.000001]
    # This stores the function which defines all the loads acting on the beam
    force_function = point_force_function + dist_force_function 
    moment_function = point_moment_function
    
    # Generate graph
        # If selected type is cantilever
    if beam_type == 'CL':
        beam_len = CL_data[0]['length']
        beam_BC = CL_data[0]['BC']

        # Calculating the reaction force and moment
        if beam_BC == 'L':
            r_f, r_m, r_t = cantilever_solver(moment_function, force_function, [], x, beam_len, BC = 'L')
            f_f_CL = r_f*sp.DiracDelta(x)   # This function refines the reaction force at the boundary for the cantilever
            f_m_CL = r_m*sp.DiracDelta(x)   # This function refines the reaction moment at the boundary for the cantilever
            refinement = refinement + [0.0001]

        elif beam_BC == 'R':
            r_f, r_m, r_t = cantilever_solver(moment_function, force_function, [], x, beam_len, BC = 'R')
            f_f_CL = r_f*sp.DiracDelta(x - beam_len)   # This function refines the reaction force at the boundary for the cantilever
            f_m_CL = r_m*sp.DiracDelta(x - beam_len)   # This function refines the reaction moment at the boundary for the cantilever
            refinement = refinement + [beam_len - 0.0001]
            
        msg = ['The reaction force is: ' + str(round(r_f, 2))] + ['\nThe reaction moment is: ' + str(round(r_m,2))]

        # Denerating the data points for graph    
        total_ext_force_func  = force_function + f_f_CL
        total_ext_moment_func = moment_function + f_m_CL

        # ----------------------------------------------------------------------- Beam diagram
        if beam_BC == 'L':
            layout_beam_diagram = {
                                  'shapes': CL_bc_plot(beam_len, 'L') +     # cantilever_support_shape is imported from assets.
                                            force_arrows                    # These arrows show the point forces                                                                     
                                  }
        elif beam_BC == 'R':
            layout_beam_diagram = {
                                  'shapes': CL_bc_plot(beam_len, 'R') +     # cantilever_support_shape is imported from assets.
                                            force_arrows                    # These arrows show the point forces                                                                     
                                  }
        
        # If selected type is Simply supported beam
    elif beam_type == 'SSB':
        beam_len = SSB_data[0]['length']
        pin_pos = SSB_data[0]['pin']
        roller_pos = SSB_data[0]['roller']

        # The following block checks whether the pin and roller positions are
        # acceptable 
        cond1 = (pin_pos > beam_len) or (pin_pos < 0)
        cond2 = (roller_pos > beam_len) or (roller_pos < 0)
        cond3 = pin_pos == roller_pos

        if cond1:
            child_graph = html.Div([html.H6('Roller and pin position error: Pin is placed outside beam')])
            no_times_update = 1
            return child_graph, str(no_times_update)

        if cond2:
            child_graph = html.Div([html.H6('Roller and pin position error: Roller is placed outside beam')])
            no_times_update = 1
            return child_graph, str(no_times_update)

        if cond3:
            child_graph = html.Div([html.H6('Roller and pin position error: They should not be the same')])
            no_times_update = 1
            return child_graph, str(no_times_update)

        # refining the grid around the pin and roller
        refinement = refinement + \
                     [pin_pos - 0.00001, pin_pos, pin_pos + 0.00001] + \
                     [roller_pos - 0.00001, roller_pos, roller_pos + 0.00001]

        # calculating the reaction force
        r_pin, r_roller = simply_supported_solver(moment_function, force_function, x, beam_len, pin_pos, roller_pos)
        r_pin_func = r_pin*sp.DiracDelta(x - pin_pos)
        r_roller_func = r_roller*sp.DiracDelta(x - roller_pos)

        msg = ["The pin reaction force is: " + str(round(r_pin,2))] + ["\nThe roller reaction force is: " + str(round(r_roller,2))]

        # Calculating net force and moment on the beam
        total_ext_force_func  = force_function + r_pin_func + r_roller_func
        total_ext_moment_func = moment_function 

        # ----------------------------------------------------------------------- Beam diagram
        layout_beam_diagram = {
                              'shapes': SSB_bc_plot(beam_len, pin_pos, roller_pos) +     # cantilever_support_shape is imported from assets.
                                        force_arrows                   # These arrows show the point forces                                                                     
                              }

    # Calculating the data points
    # Calculating the shear force and the bending moment symbolic functions
    sign_conv = -1 # This gives the sign convention of the force and shear to the left
                   # . In This case, it is -ve of the global sign
    v = sign_conv*force_sum(total_ext_force_func, x, y)
    m = sign_conv*moment_sum(total_ext_moment_func, total_ext_force_func, x, y)

    # Calcating shear force and moment at discreet points
    x_pts = np.linspace(0, beam_len, 100)
    x_pts = np.append(x_pts, refinement)
    x_pts.sort()
    x_pts = np.unique(x_pts, axis=0)
    shear_data = list_eval(v, y, x_pts) 
    moment_data = list_eval(m, y, x_pts)

    # Generating the graph
    # ----------------------------------------------------------------------- Shear force diagram
    trace_shear = go.Scatter(
                            x = x_pts,
                            y = shear_data,
                            name = "shear",
                            line = {'color':'#ff6b6b'},
                            fill='tozerox'
                            )
    max_shear = max(shear_data)
    min_shear = min(shear_data)
    shear_graph_range = [                         
                        min_shear - 0.05*(max_shear - min_shear),
                        max_shear + 0.05*(max_shear - min_shear)
                        ]
    print(shear_graph_range)
    # ----------------------------------------------------------------------- Moment force diagram
    trace_moment = go.Scatter(
                                x = x_pts,
                                y = moment_data,
                                name = "moment",
                                line = {'color':'#1db1cf'},
                                fill='tozerox'
                                )
    max_moment = max(moment_data)
    min_moment = min(moment_data)
    moment_graph_range = [                          
                         min_moment - 0.05*(max_moment - min_moment),
                         max_moment + 0.05*(max_moment - min_moment),
                         ]
    
    # Displaying the graph    
    fig = tools.make_subplots(
                             rows = 3, 
                             cols = 1, 
                             specs = [[{}], [{}], [{}]],
                             shared_xaxes = True, 
                             shared_yaxes = False,
                             vertical_spacing = 0.001
                             )
    fig.append_trace(trace_moment, 3, 1)
    fig.append_trace(trace_shear, 2, 1)

    # This appends the point moment markers to the figure
    for i in range(len(def_PM)):
        dummy_trace = go.Scatter(
                                x = moment_arrows[i][0],
                                y = moment_arrows[i][1],
                                showlegend = False,
                                mode = "lines",
                                line = {'color':'black'}
                                )
        fig.append_trace(dummy_trace, 1, 1)

    # This appends the point force markers to the figure
    for i in range(len(def_DF)):
        dummy_trace = go.Scatter(
                                x = dist_force_marker[i][0],
                                y = dist_force_marker[i][1],
                                showlegend = False,
                                mode = "lines",
                                fill = 'tozeroy'
                                )
        fig.append_trace(dummy_trace, 1, 1)

    # adds the beam and the distributed force markers as a layout
    fig['layout'].update(
                        shapes = layout_beam_diagram['shapes'], 
                        height = 630, 
                        margin = {'l' : 50, 'r' : 20, 't' : 20, 'b' : 20}#dict(l=50, r=20, t=20, b=20)
                        )   
    fig['layout']['yaxis1'].update(title = "beam diagrams", range = [-beam_len/2,beam_len/2])     # This sets the y axis range for the beam figure
    fig['layout']['yaxis2'].update(title = "Shear force diagrams", range = shear_graph_range)     # This sets the y axis range for the shear force fig
    fig['layout']['yaxis3'].update(title = "Moment diagrams", range = moment_graph_range)         # This sets the y axis range for the bending moment fig
    fig['layout']['yaxis1'].update(showticklabels = False, showgrid = False, zeroline = False)    # Removes the grid from beam figure

    # return graph and error messages
    if error_msg == []:
        child_graph = html.Div([  dcc.Graph(id = "Shear", figure = fig)   ] + msg)
        child_mess = "Updating graph"
        no_times_update = 1

    else:
        child_graph = html.Div([  dcc.Graph(id = "Shear", figure = fig)   ] + error_msg + msg)
        child_mess = "Updating graph"
        no_times_update = 1
       
    return child_graph, str(no_times_update)
#----------------------------------------------------------------------------------------------------------------- Display message
@app.callback(
             Output('message', 'children'),
             [
               Input('update_graph_button', 'n_clicks'),
               Input('graph_div', 'children'),
               Input('data_error', 'children')
             ],
             [
               State('message', 'children')
             ]
             )
def update_complete_message(n_clicks, com, error_msg, prev_msg):
    ctx = dash.callback_context
    if not ctx.triggered:
        ans = "Loading"
    else:
        trig = ctx.triggered[0]['prop_id'] # This print updating.children, find a way to remove the children bit
    
    if trig == 'update_graph_button.n_clicks':
        if n_clicks == 0:
            ans = "Loading"
        elif n_clicks > 0:
            ans = html.Div(
                          id = 'message_1', 
                          children = "Updating the graphs",
                          style = {
                                  'marginTop': '10px',
                                  "border" : "1px solid black",
                                  'backgroundColor':'#ff0066',
                                  'textAlign' : 'center'
                                  }
                          )

    elif trig == 'graph_div.children':
        ans = "Completed"

    elif trig == 'data_error.children':
        if error_msg == '0':
            if prev_msg == "Loading":
                ans = prev_msg

            else:
                ans = "  ...  "

        else:
            ans = error_msg

    return ans
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Update graph interaction
# .. Help popup interaction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Help popup interaction
#----------------------------------------------------------------------------------------------------------------- Close popup interaction
@app.callback(
              Output('modal', 'style'),
              [Input('modal-close-button', 'n_clicks')]
             )
def close_modal(n):
    if (n is not None) and (n > 0):
        return {"display": "none"}
    else:
        return {"display": "block"}

#----------------------------------------------------------------------------------------------------------------- Open popup
@app.callback(
              Output('modal-close-button', 'n_clicks'),
              [Input('open_help', 'n_clicks')]
             )
def reset(n):
    if (n is not None) and (n > 0):
        return 0
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Help popup interaction
if __name__ == '__main__':
    app.run_server(debug=False)

