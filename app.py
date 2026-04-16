import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

region_options = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]

app = dash.Dash(__name__)

app.layout = html.Div(
    className="page-wrapper",
    children=[
        html.Div(
            className="header",
            children=[
                html.Div("🍬", className="header-logo"),
                html.H1("Soul Foods Pink Morsel Sales Visualiser"),
                html.P("Tracking sales performance across all regions · 2018 – 2022"),
            ],
        ),
        html.Div(
            className="card",
            children=[
                html.Div("Filter by Region", className="filter-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=region_options,
                    value="all",
                    className="radio-group",
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[dcc.Graph(id="sales-chart", config={"displayModeBar": False})],
        ),
        html.Div("Soul Foods · Pink Morsel Analytics Dashboard", className="footer"),
    ],
)


@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(selected_region):
    if selected_region == "all":
        filtered = df.groupby("date", as_index=False)["sales"].sum()
        title = "Total Pink Morsel Sales — All Regions"
    else:
        filtered = (
            df[df["region"] == selected_region]
            .groupby("date", as_index=False)["sales"]
            .sum()
        )
        title = f"Pink Morsel Sales — {selected_region.capitalize()} Region"

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title=title,
        labels={"date": "Date", "sales": "Sales ($)"},
        color_discrete_sequence=["#e91e8c"],
    )

    fig.update_traces(line=dict(width=2.5))

    price_increase_ts = pd.Timestamp("2021-01-15").timestamp() * 1000

    fig.add_shape(
        type="line",
        x0=price_increase_ts,
        x1=price_increase_ts,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="#c62828", dash="dash", width=2),
    )

    fig.add_annotation(
        x=price_increase_ts,
        y=0.97,
        xref="x",
        yref="paper",
        text="Price Increase<br>Jan 15, 2021",
        showarrow=False,
        font=dict(color="#c62828", size=12),
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#c62828",
        borderwidth=1,
        borderpad=4,
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", color="#37474f"),
        title=dict(font=dict(size=18, color="#880e4f"), x=0.5, xanchor="center"),
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="#f3e5f5",
            linecolor="#e0e0e0",
            tickformat="%b %Y",
        ),
        yaxis=dict(
            title="Sales ($)",
            showgrid=True,
            gridcolor="#f3e5f5",
            linecolor="#e0e0e0",
            tickprefix="$",
        ),
        margin=dict(l=60, r=40, t=60, b=60),
        hovermode="x unified",
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
