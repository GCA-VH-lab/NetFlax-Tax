# NAVIGATING INSIDE THE APP

# Import packages
import dash
import base64
from dash import html
import dash_bootstrap_components as dbc

# Import aesthetics specifics
from assets.color_scheme import *
from images import *


logo = './images/app_logo.png'
logo_base64 = base64.b64encode(open(logo, 'rb').read()).decode('ascii')

netflax_icon = './images/favicon.ico'
netflax_icon_base64 = base64.b64encode(open(netflax_icon, 'rb').read()).decode('ascii')


# ------------------------- NAVIGATION BAR -----------------------------

navbar = dbc.Navbar(
    dbc.Container([
        # Navigation Bar, left hand side. The Application Title
        dbc.Row([
            dbc.Col([
                dbc.Col(
                    html.Img(src='data:image/png;base64,{}'.format(logo_base64), height='30px')
                ),
            ], width={'size': 'auto'})
        ],
            # If a second page is to be added here is an example of how
            # dbc.Col([
            #     dbc.Nav([
            #         dbc.NavItem(dbc.NavLink('Second Page', href = '/secondpage'))
            #     ], navbar = True),
        align = 'center', 
        className = 'g-0'),
        # Navigation Bar, right hand side. Icons and links
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(
                        # Link to NetFlax
                        dbc.NavLink(
                            html.Img(src='data:image/png;base64,{}'.format(netflax_icon_base64), height='15px'),
                                href = '''https://server.atkinson-lab.com/netflax''',
                                external_link = True)),
                    dbc.NavItem(
                        # Ling to Lab's GitHub
                        dbc.NavLink(
                            html.I(className = 'bi bi-github'),
                                href = '''https://github.com/GCA-VH-lab''',
                                external_link = True)),
                    dbc.NavItem(
                        # Link to Lab's Twitter
                        dbc.NavLink(
                            html.I(className = 'bi bi-twitter'),
                                href = '''https://twitter.com/webflags1?ref_src=twsrc%5Etfw%7Ctwcamp%5Eembeddedtimeline%7Ctwterm%5Escreen-name%3Awebflags1%7Ctwcon%5Es2''',
                                external_link = True))
                ], navbar = True)
            ])
        ], align = 'center')
    ], fluid = True),
    color = navigation_bar,
    dark = True)
