from dash import html, dcc
from dash.dependencies import Input, Output

import app as app
from pages import search, stat

application = app

app.layout = html.Div([
        dcc.Location(id = 'url', refresh = False),
        html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/search':
        return search.layout
    else:
        return stat.layout


if __name__ == '__main__':
    # Set the debug to False when deploying app 
    app.run_server(host='0.0.0.0', port=8080, debug=True)  