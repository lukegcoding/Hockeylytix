import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from dashboard.data import get_team_options, get_season_options, get_event_type_options, get_event_location

app = dash.Dash(__name__)

team_options = get_team_options()
season_options = get_season_options()
event_type_options = get_event_type_options()

app.layout = html.Div([
    html.H1("Game Event Explorer"),
    dcc.Dropdown(options=team_options, value=21, id='team'),
    dcc.Dropdown(options=season_options, value=season_options[-1]['value'], id='season'),
    # dcc.Dropdown(games, id='demo-dropdown'), (Maybe not a dropdown possibly a text field)
    dcc.Dropdown(options=event_type_options, value='goal', id='event_type'),
    dcc.Graph(id='event-chart')
])

@app.callback(
    Output('event-chart', 'figure'),
    Input('team', 'value'),
    Input('season', 'value'),
    Input('event_type', 'value'),
)
def update_chart(team_id, season, event_type):
    rows = get_event_location(team_id, season, event_type)

    x_vals = [row[0] for row in rows]
    y_vals = [row[1] for row in rows]

    fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='markers'))

    return fig


if __name__ == "__main__":
    app.run(debug=True)