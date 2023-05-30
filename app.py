# LAUNCH THE APP

# Import packages
import dash
from dash import html
import dash_bootstrap_components as dbc


# --------------------------- CREATE APP -------------------------------

# Create the app
app = dash.Dash(
    __name__,
    assets_folder='assets', 
    external_stylesheets = [dbc.themes.SANDSTONE, 
                            dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions = True,
    use_pages = True
)

# Server
server = app.server

# App layout
app.title = ('NetFlax Tax')
app.layout = html.Div(children=[
    dash.page_container
])


# Run the app
if __name__ == '__main__':
    # Set debug to False when deploying
    app.run_server(host = '0.0.0.0', port = '8080', debug = True)