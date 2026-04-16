import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

daily_sales = df.groupby("date", as_index=False)["sales"].sum()

fig = px.line(daily_sales, x="date", y="sales", labels={"date": "Date", "sales": "Sales ($)"})

price_increase_date = pd.Timestamp("2021-01-15").timestamp() * 1000

fig.add_vline(
    x=price_increase_date,
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase",
    annotation_position="top left",
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig),
])

if __name__ == "__main__":
    app.run(debug=True)
