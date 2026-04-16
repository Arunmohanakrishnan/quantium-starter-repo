import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

regions = ["all"] + sorted(df["region"].unique().tolist())

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#2c3e50"}
        ),
        html.Div(
            [
                html.Label("Filter by Region:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": r.capitalize(), "value": r} for r in regions],
                    value="all",
                    inline=True,
                    style={"marginTop": "8px", "gap": "16px"}
                ),
            ],
            style={"marginBottom": "20px"}
        ),
        dcc.Graph(id="sales-chart"),
    ]
)

@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(selected_region):
    if selected_region == "all":
        filtered = df.groupby("date", as_index=False)["sales"].sum()
        title = "Total Pink Morsel Sales Over Time (All Regions)"
    else:
        filtered = df[df["region"] == selected_region].groupby("date", as_index=False)["sales"].sum()
        title = f"Pink Morsel Sales Over Time — {selected_region.capitalize()} Region"

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title=title,
        labels={"date": "Date", "sales": "Sales ($)"},
    )

    price_increase_date = pd.Timestamp("2021-01-15").timestamp() * 1000

    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", dash="dash", width=2),
    )

    fig.add_annotation(
        x=price_increase_date,
        y=1,
        xref="x",
        yref="paper",
        text="Price Increase (Jan 15, 2021)",
        showarrow=False,
        font=dict(color="red"),
        xanchor="left",
        yanchor="top",
    )

    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#ececec"),
        yaxis=dict(showgrid=True, gridcolor="#ececec"),
        title_x=0.5,
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
