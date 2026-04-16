import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

price_increase_ts = pd.Timestamp("2021-01-15").timestamp() * 1000

total_sales = df["sales"].sum()
peak_day = df.groupby("date")["sales"].sum().idxmax()
date_range = f"{df['date'].min().strftime('%b %Y')} – {df['date'].max().strftime('%b %Y')}"

app = dash.Dash(__name__)

app.layout = html.Div(id="app-container", children=[

    html.Div(id="header-container", children=[
        html.H1("Pink Morsel Sales Visualiser", id="header"),
        html.P("Soul Foods — Pink Morsel performance over time", id="subheader"),
    ]),

    html.Div(id="stats-bar", children=[
        html.Div(className="stat-card", children=[
            html.Div(f"${total_sales:,.0f}", className="stat-value"),
            html.Div("Total Sales", className="stat-label"),
        ]),
        html.Div(className="stat-card", children=[
            html.Div(peak_day.strftime("%d %b %Y"), className="stat-value"),
            html.Div("Peak Sales Day", className="stat-label"),
        ]),
        html.Div(className="stat-card", children=[
            html.Div(date_range, className="stat-value", style={"fontSize": "1.1rem"}),
            html.Div("Date Range", className="stat-label"),
        ]),
        html.Div(className="stat-card", children=[
            html.Div("15 Jan 2021", className="stat-value", style={"color": "#f64f59"}),
            html.Div("Price Increase", className="stat-label"),
        ]),
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
            inputStyle={"margin-right": "6px", "accent-color": "#c471ed"},
            labelClassName="region-option",
        ),
    ]),

    html.Div(id="chart-container", children=[
        dcc.Loading(
            type="circle",
            color="#c471ed",
            children=dcc.Graph(id="sales-chart", config={"displayModeBar": False}),
        ),
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
        line_color="#f64f59",
        line_width=1.5,
        annotation_text="Price Increase — 15 Jan 2021",
        annotation_position="top left",
        annotation_font_color="#f64f59",
        annotation_font_size=12,
    )

    fig.update_traces(
        line=dict(color="#c471ed", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(196, 113, 237, 0.08)",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ecf0f1", family="Inter, sans-serif"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            tickfont=dict(color="#8892a4"),
            title_font=dict(color="#c471ed"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            tickfont=dict(color="#8892a4"),
            title_font=dict(color="#c471ed"),
            tickprefix="$",
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1a1a3e",
            bordercolor="#c471ed",
            font_color="#ecf0f1",
        ),
        transition=dict(duration=400, easing="cubic-in-out"),
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
