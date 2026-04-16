import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

price_increase_ts = pd.Timestamp("2021-01-15").timestamp() * 1000

app = dash.Dash(__name__)

app.layout = html.Div(id="app-container", children=[
    html.Div(id="header-container", children=[
        html.H1("Pink Morsel Sales Visualiser", id="header"),
        html.P("Soul Foods — Pink Morsel performance over time", id="subheader"),
    ]),
    html.Div(id="controls-container", children=[
        html.Label("Filter by Region", id="radio-label"),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All",   "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "South", "value": "south"},
                {"label": "East",  "value": "east"},
                {"label": "West",  "value": "west"},
            ],
            value="all",
            inline=True,
            inputStyle={"margin-right": "6px"},
            labelStyle={"margin-right": "20px"},
        ),
    ]),
    html.Div(id="chart-container", children=[
        dcc.Graph(id="sales-chart"),
    ]),
])


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    daily = filtered.groupby("date", as_index=False)["sales"].sum()

    fig = px.line(
        daily,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Sales ($)"},
    )
    fig.add_vline(
        x=price_increase_ts,
        line_dash="dash",
        line_color="#e74c3c",
        annotation_text="Price Increase (15 Jan 2021)",
        annotation_position="top left",
        annotation_font_color="#e74c3c",
    )
    fig.update_traces(line_color="#9b59b6", line_width=2)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ecf0f1",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        margin=dict(l=40, r=40, t=20, b=40),
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
