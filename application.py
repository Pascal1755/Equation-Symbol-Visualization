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

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#global in scope? this is sanctioned by dash.plotly.com, but not recommended?
myText = 'y = 3*x\nz = 4*x + 8*y\nw+y=z+x'

def graphEquations(myText):

    graphOfLeft, err = graphByEquals2(myText)

    ###### if there is an error with equations in myText, then return blank figure ########
    if (err is not None):
        return {"data": [go.Scatter()],
                "layout": go.Layout(title='Equation Visualization',
                                    showlegend=False, hovermode='closest',
                                    margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                    xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                    yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                    height=300,
                                    )}

    ################### assign positions in x-y plane in units pixels by each symbol/key ###############
    x_pos_by_key=dict() #dictionary to lookup x position by symbol key
    y_pos_by_key=dict() #dictionary to lookup y position by symbol key
    row=len(graphOfLeft)*max([len(item) for item in graphOfLeft.values()])
    col=0
    for key in graphOfLeft:
        col=0
        if ( key not in x_pos_by_key ):
            x_pos_by_key[key]=col+0.2*random.rand()
        if ( key not in y_pos_by_key ):
            y_pos_by_key[key]=row+0*random.rand()
        for k, sym in enumerate(graphOfLeft[key]):
            if ( (sym not in x_pos_by_key) and
                    (sym not in y_pos_by_key) ):
                col = 2
                x_pos_by_key[sym]=col+0.5*random.rand()
                y_pos_by_key[sym]=row+0.2*random.rand()
            row-=1

    ###################### plot out all symbols as nodes on x-y plane #####################################
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

    ###################### plot out lines between nodes/symbols on x-y plane ##################################
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

    ################################### produce figure from traceRecode ####################################
    listOfArrows=[dict(ax=(x_pos_by_key[edge['from']] + x_pos_by_key[edge['to']]) / 2,
                       ay=(y_pos_by_key[edge['from']] + y_pos_by_key[edge['to']]) / 2,
                       axref='x', ayref='y',
                       x=(x_pos_by_key[edge['to']] * 3 + x_pos_by_key[edge['from']]) / 4,
                       y=(y_pos_by_key[edge['to']] * 3 + y_pos_by_key[edge['from']]) / 4,
                       xref='x', yref='y', showarrow=True, arrowhead=3, arrowsize=4,
                       arrowwidth=1, opacity=1) for edge in listOfEdges]

    figure = {"data": traceRecode,
              "layout": go.Layout(title='Equation Visualization', showlegend=False, hovermode='closest',
                                  margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                  xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                  yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                  height=len(graphOfLeft)*100+100,
                                  annotations=listOfArrows
                            )}
    return figure

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('Page 1'),
    html.H2("Write out some equations in the text box"),
    dcc.Textarea(id='page-1-input', value=myText,
                 style={'width':'100%', 'height':200},),
    ############## Display Graph in JSON / Python dict ################
    html.Div(id='page-1-content', style={'whiteSpace': 'pre-line'}),
    html.Br(),
    ############## Graph of the graph here ############################
    dcc.Graph(id='page-1-graph', figure=graphEquations(myText)),
    ############## Links elsewhere ####################################
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

])


@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-input', 'value')])
def page_1_text(input_value):
    myText = input_value
    graphOfLeft, err = graphByEquals2(input_value)
    if (err is None):
        return 'The graph in JSON / python dictionary form: \n{}'.format(str(graphOfLeft))
    else:
        return 'There was an error: \n{}'.format(str(err.args[0]))

@app.callback(dash.dependencies.Output('page-1-graph','figure'),
              [dash.dependencies.Input('page-1-input','value')])
def update_graph(input_value):
    myText = input_value
    return graphEquations(input_value)

page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)