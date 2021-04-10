import dash
import dash_core_components as dcc
import dash_html_components as html
#import plotly.graph_objects as go
#from numpy import random
from graphFromText.graphByEquals import graphByEquals2, graphByEqualsFxn1, graphByEquals3, graphByEquals4
from graphFromText.graphEquations import graphEquations, graphEquationsWithFxn

# This is a dash application created by Pascal Nespeca on 9/9/2020
# created in order to help visualize systems of equations. It's initial
# intent is to facilitate tracking dependencies of Ordinary Differential
# Equations (ODE). The Python packages Plotly and Dash are used to publish the
# parsed equations.
#
# Portions of this code are borrowed from Jiahui Hwang's project
# https://github.com/jhwang1992/network-visualization
# Most notably, it borrows from the idea that the visualization
# of a graph data structure consists of nodes drawn as a scatter plot
# in plotly and the edges of the graph are drawn as lines.
#
# Notable differences are that the NetworkX library is not used
# and there is a rudimentary parser in the graphFromText folder.
# The graphByEquals2 function creates a graph from the equations
# entered by the user. This needs further development.

my_app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = my_app.server  #used to tell gunicorn where the $(VARIABLE_NAME) can be found,
                     #in this case, it is "app". Supposedly, this is a server?

colors = {'background': '#FFFFFF','text': '#111111'}

my_app.layout = html.Div(style={'backgroundColor': colors['background']},
    children = [
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# myText is global in scope, which can be problematic. This is actually
# allowed by dash.plotly.com
# see page https://dash.plotly.com/sharing-data-between-callbacks
myText = 'y = 3*x+u\nz = 4*x + 8*y + 9*v\nw = z+y^2+v\n'
HomeMD='''
From the following equations:  
y = 3\*x+u  
z = 4\*x + 8\*y + 9\*v  
w = z+y^2+v

Comes the visualization:
'''
index_page = html.Div(id='index-page',
                      style={'backgroundColor': colors['background']}, \
        children = [
        dcc.Link(id='P1-link',children='Use Equation Symbol Visualization Tool', \
            href='/page-1', style={'color': colors['text']}),
        html.Br(),
        dcc.Link(id='P2-link', children='How to use Equation Symbol Visualization',
                 href='/page-2', style={'color': colors['text']}),
        html.Hr(),
        dcc.Markdown(id='Home-Eq1', children=HomeMD, style={'color': colors['text']}),
        html.Br(),
        html.Img(src=my_app.get_asset_url('graph1-white.png'))
])

page_1_layout = html.Div(id='page1',style={'backgroundColor': colors['background']},
    children = [
    ############## Links elsewhere ####################################
    dcc.Link(id='page1-link1', children='How to use Equation Symbol Visualization', href='/page-2',
                 style={'color': colors['text']}),
    html.Br(),
    dcc.Link(id='page1-link2', children='Go back to home', href='/',
                 style={'color': colors['text']}),
    html.Hr(),
    html.H1(id='page1-H1',children='Equation Symbol Visualization',
            style={'color':colors['text']}),
    html.H2(id='page1-H2',children="Write out some equations in the text box below",
            style = {'color': colors['text']}),
    dcc.Textarea(id='page-1-input', value=myText,
                 style={'width': '100%', 'height': 200, 'color': colors['text'],
                        'backgroundColor': colors['background']}),
    html.Br(),
    html.Button(id='submit-val', n_clicks=0, children='Submit'),
    html.Hr(),
    ############## Options ############################################
    html.H4(id='page1-H4', children="Options", style={'color': colors['text']}),
    html.Br(),
    ############## Light or Dark Theme Selector #######################
    dcc.RadioItems(id='light-dark-theme',
        options=[{'label': i, 'value': i} for i in ['Light', 'Dark']],
        value='Light',
        labelStyle={'display': 'inline-block'},
        style={'color': colors['text'], 'backgroundColor': colors['background']}),
    html.Br(),
    ############## New, added 1-4-2020 #######################
    dcc.RadioItems(id='fxn-option',
        options=[{'label': i, 'value': i} for i in ['Map symbols to functions',\
                                                    'Do not map symbols to functions']],
        value='Do not map symbols to functions',
        labelStyle={'display': 'inline-block'},
        style={'color': colors['text'], 'backgroundColor': colors['background']}),
    html.Hr(),
    ############## Graph of the graph here ############################
    dcc.Graph(id='page-1-graph', figure=graphEquations(myText)),
    ############## Display Graph in JSON / Python dict ################
    html.Hr(),
    html.Div(id='page-1-content',
            style={'whiteSpace': 'pre-line', 'color': colors['text']})  # new
])

#[dash.dependencies.Input('page-1-input', 'value')])
@my_app.callback(dash.dependencies.Output('page-1-content', 'children'),
                [dash.dependencies.Input('submit-val', 'n_clicks'),
                 dash.dependencies.Input('fxn-option','value')], #new
                [dash.dependencies.State('page-1-input', 'value')])  #new
def page_1_text(n_clicks, fxnOptionSelection, input_value):
    myText = input_value
    graphOfLeft, err = graphByEquals2(input_value)
    if (fxnOptionSelection == 'Do not map symbols to functions'):
        graphOfLeft, err = graphByEquals2(input_value)
    else:
        graphOfLeft, err = graphByEqualsFxn1(input_value)
    if (err is None):
        return 'The graph in python dictionary / JSON form: {}'.format('\n' + str(graphOfLeft))
    else:
        return 'There was an error: {}'.format('\n' + str(err.args[0]))


'''[dash.dependencies.Input('page-1-input', 'value'),
 dash.dependencies.Input('light-dark-theme', 'value')]'''
@my_app.callback(dash.dependencies.Output('page-1-graph', 'figure'),
                 [dash.dependencies.Input('submit-val', 'n_clicks'),
                  dash.dependencies.Input('light-dark-theme', 'value'),
                  dash.dependencies.Input('fxn-option','value')], #new
                 [dash.dependencies.State('page-1-input', 'value')]) #new
def update_graph(n_clicks,lightOrDarkSelection,fxnOptionSelection,input_value):
    myText = input_value
    if (fxnOptionSelection == 'Do not map symbols to functions'):
        myFig=graphEquations(myText)
    else:
        myFig=graphEquationsWithFxn(myText)
    ############### Graph Color Update ###############################
    if (lightOrDarkSelection == 'Light'):
        localColors = {'background': '#FFFFFF',
                  'text': '#111111'}
    else:
        localColors = {'background': '#111111',
                  'text': '#7FDBFF'}

    myFig['layout']['plot_bgcolor']=localColors['background']
    myFig['layout']['paper_bgcolor']=localColors['background']
    myFig['layout']['font_color']=localColors['text']
    for arrow in myFig['layout']['annotations']:
        arrow['arrowcolor']=localColors['text']

    return myFig

how_to_markdown_text = '''
### Description
Equation Symbol Visualization is a [__dash app__](http://dash.plotly.com) created to create a visual representation of information 
flow for systems of equations. It is presumed that the leftmost symbol on the left hand side of the equation represents 
assignment.

### Usage

Simply navigate from home to the "Equation Symbol Visualization".

Enter equations with one symbol on the left hand side for assignment and one or more symbols on the right hand side

For example, if the following were entered in the text box:  
y = 3\*x+u  
z = 4\*x + 8\*y + 9\*v  
w = z+y^2+v  
v = -y+x  

The following graph data structure as a python dictionary / JSON representation would be produced:  
{'y': \['x', 'u'], 'z': \['x', 'y', 'v'], 'w': \['z', 'y', 'v'], 'v': \['y', 'x']}  

Also, a visualization of the equations will be produced below the textbox of the equations which uses the dash and
plotly packages. Where the visualization would show the following:  
* x and u would point to y
* x, y and v would point to z
* z, y and v would point to w
* y and x would point to v

### Notes

* Symbols such as '9bears' are considered illegal since the first character contains a number. However, the symbol 
'bears9' is perfectly acceptable.

* There is an options section at the bottom of the web tool that allows a user to select a light or dark theme.

* There is also a new option to map symbols using functional notation, e.g. y = f(x).

* In the current implementation, note that in the event that more than one symbol appears on the left hand side, 
it will be treated as if the leftmost symbol were used for assignment and the other symbol(s) were moved to the 
right hand side. For example:  
   >y = 3\*x+u  
   >x+v = 8\*y + u  
   >z = v + y  
   >
   >Will produce the following graph data structure of symbols:
   >{'y': \['x', 'u'], 'x': \['y', 'u', 'v'], 'z': \['v', 'y']}
   >
   >Since both x and v are found in _x+v_ on the left hand side, x is leftmost symbol, v is moved over to the right 
   >hand side.
   >
   >In this case, the visualization would show the following:  
   >* x and u would point to y
   >* y, u and v would point to x
   >* v and y would point to z

### Source Code

* Source code can be found at [__Pascal's Git Hub repo__](https://github.com/Pascal1755/Equation-Symbol-Visualization)

### Future Improvements
Desired improvements would be as follows:
* Special visual representation for reflexive expressions used in coding statements, like x = x + 1
* More options for multiple assignments on the left hand side 
* Support for inequality statements, i.e. <=, >=
* A user input to help identify unnecessary variables or unnecessary equations

### Usefulness
Utilizing the graphical representation of a system of equations can be helpful from the standpoint of identifying
relations between symbols, sub-systems of equations and identifying unnecessary equations.
'''

page_2_layout = html.Div(style={'backgroundColor': colors['background']},
    children = [
    dcc.Link(id='page2-link1', children='Use Equation Symbol Visualization Tool',
             href='/page-1',style={'color': colors['text']}),
    html.Br(),
    dcc.Link(id='page2-link2', children='Go back to home', href='/',
             style={'color': colors['text']}),
    html.Hr(),
    html.H1(id='page2-H1',children='How to use Equation Symbol Visualization',
            style={'color': colors['text']}),
    dcc.Markdown(id='page2-MD', children=how_to_markdown_text,
                 style={'color': colors['text']})
])

# Update the index
@my_app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
# You could also return a 404 "URL not found" page here

@my_app.callback([dash.dependencies.Output('page1-H1','style'),
               dash.dependencies.Output('page1-H2','style'),
               dash.dependencies.Output('page1-H4','style'),
               dash.dependencies.Output('page-1-input','style'),
               dash.dependencies.Output('page-1-content','style'),
               dash.dependencies.Output('page1','style'),
               dash.dependencies.Output('page1-link1','style'),
               dash.dependencies.Output('page1-link2','style'),
               dash.dependencies.Output('light-dark-theme','style'),
               dash.dependencies.Output('fxn-option','style')],
              [dash.dependencies.Input('light-dark-theme','value')])
def lightDarkSelector(lightOrDarkSelection):
    global colors #strange that Dash needs this
    if (lightOrDarkSelection == 'Light'):
        localColors = {'background': '#FFFFFF',
                  'text': '#111111'}
    else:
        localColors = {'background': '#111111',
                  'text': '#7FDBFF'}
    colors=localColors  #strange artifact of dash,
                        #does this actually update the global colors?
    localStyle = {'backgroundColor': localColors['background'],
                  'color': localColors['text']}
    localStyles = [localStyle for k in range(0, 10)]
    ############### Handle special cases #############################
    localStyles[3]={'width': '100%', 'height': 200,
                    'color': localColors['text'],
                    'backgroundColor': localColors['background']}
    return localStyles

if __name__ == '__main__':
    my_app.run_server(debug=True)