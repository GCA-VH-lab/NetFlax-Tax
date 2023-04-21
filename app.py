import dash
from dash import html

import dash_bootstrap_components as dbc



# --------------------------- CREATE APP -------------------------------

app = dash.Dash(
    __name__,
    assets_folder='assets', 
    external_stylesheets = [dbc.themes.SANDSTONE, 
                            dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions = True,
    use_pages = True
)



server = app.server
app.title = ('./assets/favicon.ico')


app.layout = html.Div(children=[
    dash.page_container
])


if __name__ == '__main__':
    # Set debug to False when deploying
    app.run_server(host = '0.0.0.0', port = '8080', debug = True)