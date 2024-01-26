import dash
import dash_bootstrap_components as dbc
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app =dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

app.scripts.config.serve_locally = True
server = app.server