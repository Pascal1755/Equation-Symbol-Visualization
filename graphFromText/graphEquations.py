import plotly.graph_objects as go
from numpy import random
from graphFromText.graphByEquals import graphByEquals2, graphByEqualsFxn1,\
    graphByEquals3, graphByEquals4
from graphFromText.fxnFromText.fxnGraph import getRowsByKeyMulti

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

def graphEquationsWithFxn(myText):
    ### Need to update so that it calls graphByEquals5(myText) and getRowsByKeyMulti(symbolGraph) ###

    symbolGraphMulti, err = graphByEqualsFxn1(myText)

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
    rowsByKey = getRowsByKeyMulti(symbolGraphMulti)  #outputs dicionary where values are row number
    max_lvl = max([item[3] for item in rowsByKey.keys()])
    for key in rowsByKey:
        if (key not in x_pos_by_key and key not in y_pos_by_key):
            y_pos_by_key[key] = rowsByKey[key]
            lvl = key[3]  # key[3] corresponds to the fxn level determined by words followed by parens
            dataOrFxn = key[2]  # key[2] corresponds to the type of the node, 'data' or 'fxn'
            eqNum = key[4]
            if ( lvl == -1 ):  # if lvl is -1, then its a LHS data item
                x_pos_by_key[key] = lvl + 0.25*(lvl%2) - 0.25*(eqNum%2)
            else:
                if (dataOrFxn == 'fxn'):
                    x_pos_by_key[key] = lvl-0.5 + 0.25*((lvl+1)%2)
                else:
                    x_pos_by_key[key] = lvl + 0.25*(lvl%2)

    ######################### old stuff to plot out on x-y plane #######################################
    #row = 21 #dash will automatically resize the graph, so negative row #'s are ok
    #leftCol=0
    #rightCol=5
    #for key in graphOfLeft:
    #    leftCol=1-leftCol  #toggle the leftCol value between 0 and 1
    #    row-=1  #move down one row with each new key
    #    if ( key not in x_pos_by_key and key not in y_pos_by_key ):
    #        x_pos_by_key[key]=(leftCol-0.5)+1+0.1*(row%2)
    #        y_pos_by_key[key]=row+0.1*random.rand()
    #    for k, sym in enumerate(graphOfLeft[key]):
    #        if ( (sym not in x_pos_by_key) and
    #                (sym not in y_pos_by_key) ):
    #            x_pos_by_key[sym]=rightCol+0.2*(row%2)
    #            y_pos_by_key[sym]=row+0.2*(row%2)
    #            row-=1


    ###################### plot out all symbols as nodes on x-y plane ##################################
    traceRecode = []
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text',
                            textposition="bottom center",
                            hoverinfo="text", marker={'size': 20, 'color': 'LightSkyBlue'})
    for node in x_pos_by_key:
        nodeSymbol = node[0]  # added, 1-4-2020
        hovertext = "Symbol: " + nodeSymbol  # modified, 1-4-2020
        text = nodeSymbol  # modified, 1-4-2020
        node_trace['x'] += tuple([x_pos_by_key[node]])
        node_trace['y'] += tuple([y_pos_by_key[node]])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])

    traceRecode.append(node_trace)

    ############ Connect the dots (nodes), plot out lines between nodes/symbols on x-y plane ###########
    listOfEdges=[]
    for key in symbolGraphMulti:
        x1 = x_pos_by_key[key]
        y1 = y_pos_by_key[key]
        for k, sym in enumerate(symbolGraphMulti[key]):
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
                                  height=len(symbolGraphMulti)*100+100,
                                  annotations=listOfArrows
                            )}
    return figure