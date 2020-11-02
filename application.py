import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from numpy import random
from graphFromText.graphByEquals import graphByEquals2, graphByEquals3

# This is a dash application created by Pascal Nespeca on 9/9/2020
# created in order to help visualize systems of equations. It's initial
# intent is to facilitate tracking dependencies of Ordinary Differential
# Equations. The Python packages Plotly and Dash are used to publish the
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

colors = {'background': '#111111','text': '#7FDBFF'}

my_app.layout = html.Div(style={'backgroundColor': colors['background']},
    children = [
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#global in scope which can be problematic. This is sanctioned by dash.plotly.com
#see page https://dash.plotly.com/sharing-data-between-callbacks
myText = 'y = 3*x+u\nz = 4*x + 8*y + 9*v\nw=z+y^9+v\n'
def graphEquations(myText):

    graphOfLeft, err = graphByEquals2(myText)

    ###### if there is an error with equations in myText, then return blank figure ########
    if (err is not None):
        return {"data": [go.Scatter()],
                "layout": go.Layout(title='Equation Symbol Visualization',
                                    showlegend=False, hovermode='closest',
                                    margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                    xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                    yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                    height=300,
                                    )}

    ################### assign positions in x-y plane in units pixels by each symbol/key ###############
    x_pos_by_key=dict() #dictionary to lookup x position by symbol key
    y_pos_by_key=dict() #dictionary to lookup y position by symbol key
    #row=len(graphOfLeft)*max([len(item) for item in graphOfLeft.values()])
    row = 21 #dash will automatically resize the graph, so negative row #'s are ok
    leftCol=0
    rightCol=5
    for key in graphOfLeft:
        leftCol=1-leftCol  #toggle the leftCol value between 0 and 1
        row-=1  #move down one row with each new key
        if ( key not in x_pos_by_key and key not in y_pos_by_key ):
            x_pos_by_key[key]=(leftCol-0.5)+1+0.1*(row%2)
            y_pos_by_key[key]=row+0.1*random.rand()
        for k, sym in enumerate(graphOfLeft[key]):
            if ( (sym not in x_pos_by_key) and
                    (sym not in y_pos_by_key) ):
                x_pos_by_key[sym]=rightCol+0.2*(row%2)
                y_pos_by_key[sym]=row+0.2*(row%2)
                row-=1

    ###################### plot out all symbols as nodes on x-y plane ##################################
    traceRecode = []
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text',
                            textposition="bottom center",
                            hoverinfo="text", marker={'size': 20, 'color': 'LightSkyBlue'})
    for node in x_pos_by_key:
        hovertext = "Symbol: " + node
        text = node
        node_trace['x'] += tuple([x_pos_by_key[node]])
        node_trace['y'] += tuple([y_pos_by_key[node]])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])

    traceRecode.append(node_trace)

    ############ Connect the dots (nodes), plot out lines between nodes/symbols on x-y plane ###########
    listOfEdges=[]
    for key in graphOfLeft:
        x1 = x_pos_by_key[key]
        y1 = y_pos_by_key[key]
        for k, sym in enumerate(graphOfLeft[key]):
            x0 = x_pos_by_key[sym]
            y0 = y_pos_by_key[sym]
            listOfEdges.append({'from':sym,'to':key})
            trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                               mode='lines',
                               line={'width': 2},
                               opacity=0.25)
            traceRecode.append(trace)

    ################################### produce figure from traceRecode ################################
    listOfArrows=[dict(ax=(x_pos_by_key[edge['from']] + x_pos_by_key[edge['to']]) / 2,
                       ay=(y_pos_by_key[edge['from']] + y_pos_by_key[edge['to']]) / 2,
                       axref='x', ayref='y',
                       x=(x_pos_by_key[edge['to']] * 3 + x_pos_by_key[edge['from']]) / 4,
                       y=(y_pos_by_key[edge['to']] * 3 + y_pos_by_key[edge['from']]) / 4,
                       xref='x', yref='y', showarrow=True, arrowhead=3, arrowsize=4,
                       arrowwidth=1, opacity=1) for edge in listOfEdges]

    figure = {"data": traceRecode,
              "layout": go.Layout(title='Equation Symbol Visualization', showlegend=False, hovermode='closest',
                                  margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                  xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                  yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                  height=len(graphOfLeft)*100+100,
                                  annotations=listOfArrows
                            )}
    return figure

index_page = html.Div(id='index-page',
                      style={'backgroundColor': colors['background']}, \
        children = [
        dcc.Link(id='P1-link',children='Equation Symbol Visualization', \
            href='/page-1', style={'color': colors['text']}),
        html.Br(),
        dcc.Link(id='P2-link', children='How to use Equation Symbol Visualization',
                 href='/page-2', style={'color': colors['text']})
])

page_1_layout = html.Div(id='page1',style={'backgroundColor': colors['background']},
    children = [
    html.H1(id='page1-H1',children='Equation Symbol Visualization',
            style={'color':colors['text']}),
    html.H2(id='page1-H2',children="Write out some equations in the text box",
            style = {'color': colors['text']}),
    dcc.Textarea(id='page-1-input', value=myText,
                 style={'width': '100%', 'height': 200, 'color': colors['text'],
                        'backgroundColor': colors['background']}),
    ############## Display Graph in JSON / Python dict ################
    html.Div(id='page-1-content', style={'whiteSpace': 'pre-line','color': colors['text']}),
    html.Br(),
    ############## Graph of the graph here ############################
    dcc.Graph(id='page-1-graph', figure=graphEquations(myText)),
    ############## Light or Dark Theme Selector #######################
    html.Br(),
    dcc.RadioItems(
        id='light-dark-theme',
        options=[{'label': i, 'value': i} for i in ['Light', 'Dark']],
        value='Dark',
        labelStyle={'display': 'inline-block', 'color': colors['text']}
        ),
    ############## Links elsewhere ####################################
    html.Br(),
    dcc.Link(id='page1-link1',children='How to use Equation Symbol Visualization', href='/page-2',
             style={'color': colors['text']}),
    html.Br(),
    dcc.Link(id='page1-link2',children='Go back to home', href='/',
             style={'color': colors['text']})
])

@my_app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-input', 'value')])
def page_1_text(input_value):
    myText = input_value
    graphOfLeft, err = graphByEquals2(input_value)
    if (err is None):
        return 'The graph in python dictionary / JSON form: \n{}'.format(str(graphOfLeft))
    else:
        return 'There was an error: \n{}'.format(str(err.args[0]))

@my_app.callback(dash.dependencies.Output('page-1-graph','figure'),
              [dash.dependencies.Input('page-1-input','value'),
               dash.dependencies.Input('light-dark-theme','value')])
def update_graph(input_value,lightOrDarkSelection):
    myText = input_value
    myFig=graphEquations(myText)
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
Equation Symbol Visualization is a [dash app](dash.plotly.com) created to create a visual representation of information 
flow for systems of equations. It is presumed that the leftmost symbol on the left hand side of the equation represents 
assignment.

### Usage

Simply navigate from home to the "Equation Symbol Visualization".

Enter equations with one symbol on the left hand side for assignment and one or more symbols on the right hand side

For example, if the following were entered in the text box:  
y = 3\*x+u  
z = 4\*x + 8\*y + 9\*v  
w = z+y^9+v  
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
'bears9' is perfectly acceptable

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

### Future Improvements
Desired improvements would be as follows:
* Support for functions inside equations, such as 'f' in z = x^2 + 6*f(x,y)
* Visual representation for reflexive expressions used in coding statements, like x = x + 1
* More meaningful support for multiple assignments on the left hand side 
* Support for inequality statements, i.e. <=, >=
* A user input to help identify unnecessary variables or unnecessary equations
* Ambitiously, some form of support for LaTeX

### Usefulness
Utilizing the graphical representation of a system of equations can be helpful from the standpoint of identifying
relations between symbols, sub-systems of equations and identifying unnecessary equations.
'''

page_2_layout = html.Div(style={'backgroundColor': colors['background']},
    children = [
    html.H1(id='page2-H1',children='How to use Equation Symbol Visualization',
            style={'color': colors['text']}),
    dcc.Markdown(id='page2-MD', children=how_to_markdown_text,
                 style={'color': colors['text']}),
    html.Br(),
    dcc.Link(id='page2-link1',children='Go to Equation Symbol Visualization',
             href='/page-1',
             style={'color': colors['text']}),
    html.Br(),
    dcc.Link(id='page2-link2',children='Go back to home', href='/',
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
               dash.dependencies.Output('page-1-input','style'),
               dash.dependencies.Output('page-1-content','style'),
               dash.dependencies.Output('page1','style'),
               dash.dependencies.Output('page1-link1','style'),
               dash.dependencies.Output('page1-link2','style'),
               dash.dependencies.Output('light-dark-theme','style')],
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
    localStyles = [localStyle for k in range(0, 8)]
    ############### Handle special cases #############################
    localStyles[2]={'width': '100%', 'height': 200,
                    'color': localColors['text'],
                    'backgroundColor': localColors['background']}
    return localStyles

if __name__ == '__main__':
    my_app.run_server(debug=True)