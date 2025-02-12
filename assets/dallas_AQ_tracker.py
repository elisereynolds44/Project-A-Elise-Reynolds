import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Preparing your data for usage *******************************************

df = pd.read_csv("ad_viz_plotval_data.csv")
df["Local Site Name"] = pd.Series(df["Local Site Name"]).str.lower()
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
df = (
    df.groupby([df["date"].dt.date, "Local Site Name"])["Daily Mean PM2.5 Concentration"]
    .mean()
    .reset_index()
)


# App Layout **************************************************************

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(
    [
        html.Div(
            html.H1(
                "Dallas Air Quality Analysis (PM2.5 Concentration)", style={"textAlign": "center"}
            ),
            className="row",
        ),
        html.Div(dcc.Graph(id="line-chart", figure={}), className="row"),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="my-dropdown",
                        multi=True,
                        options=[
                            {"label": station, "value": station}
                            for station in sorted(df["Local Site Name"].unique())
                        ],
                        value=[sorted(df["Local Site Name"].unique())[0]],
                    ),
                    className="three columns",
                ),
                html.Div(
                    html.A(
                        id="my-link",
                        children="Click here for more accurate air quality data",
                        href="www.no",
                        target="_blank",
                    ),
                    className="two columns",
                ),
            ],
            className="row",
        ),
    ]
)


# Callbacks ***************************************************************
@app.callback(
    Output(component_id="line-chart", component_property="figure"),
    [Input(component_id="my-dropdown", component_property="value")],
)
def update_graph(selected_stations):
    print(f"Values chosen by user: {selected_stations}")

    if len(selected_stations) == 0:
        return {}
    else:
        df_filtered = df[df["Local Site Name"].isin(selected_stations)]
        fig = px.line(
            data_frame=df_filtered,
            x="date",
            y="Daily Mean PM2.5 Concentration",
            color="Local Site Name",
            log_y=True,
            labels={
                "Daily Mean PM2.5 Concentration": "PM2.5 Concentration (µg/m³)",
                "date": "Date",
                "Local Site Name": "Station",
            },
        )
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)


