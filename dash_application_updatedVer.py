from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

colors = {
    'background': "#E9F4F3",
    'text': "#f80707",
    'header': '#100a0a',
    'panel_bg': '#fff',
    'panel_border': "#dad1e0"
}
region_colors = {'north': "#490505", 'south': "#07d737", 'east': "#c00b87", 'west': "#24036a"}

font_family = 'Calibri, Arial, TimesNewRoman'

data = {"Date": ["2021-01-10", "2021-01-25", "2021-02-17", 
                 "2021-01-12", "2021-01-15", "2021-02-15",
                 "2021-01-13", "2021-01-19", "2021-02-11", 
                 "2021-01-14", "2021-01-26", "2021-02-12"
                 ],
        "Region": ['North', 'North', 'North', 
                   'South', 'South', 'South',
                   'East', 'East', 'East',
                   'West', 'West', 'West'
                   ],
        "Sales": [28.4, 30.0, 29.2, 
                  18.0, 21.5, 23.2,
                  21.3, 25.6, 29.3,
                  24.0, 26.9, 32.3
                  ]}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df['Region'] = df['Region'].str.lower()

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            'Pink Morsels Sales Report',
            style = {'textAlign': 'center', 'color': colors['header'], 'fontFamily': font_family, 'fontWeight': '900', 'letterSpacing': '1px', 'marginTop': '30px'}
        ),
        html.Div(
            'Filter sales by region:',
            style = {'textAlign': 'center', 'color': colors['text'], 'fontFamily': font_family, 'marginBottom': '16px', 'fontSize': '18px'}
        ),
        html.Div(
            dcc.RadioItems(
                id = 'region-radio',
                options = [
                    {'label': 'All', 'value': 'all'},
                    {'label': 'North', 'value': 'north'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'West', 'value': 'west'},
                ],
                value = 'all',
                labelStyle = {
                    'display': 'inline-block', 
                    'marginRight': '16px',
                    'marginTop': '30px', 
                    'fontWeight': '900',
                    'fontFamily': font_family,
                    'padding': '10px 24px',
                    'border': f'1.5px solid {colors["panel_border"]}', 
                    'borderRadius': '8px',
                    'cursor': 'pointer',
                    'background': colors['panel_bg'],
                    'transition': 'background 0.2s'
                },
                style = {'textAlign': 'center', 'marginBottom': '38px'}
            ),
            style = {'textAlign': 'center'}
        ),
        html.Div(
            dcc.Graph(id = 'sales-graph'),
            style = {
                'background': colors['panel_bg'],
                'border': f'1.5px solid {colors["panel_border"]}',
                'borderRadius': '18px',
                'boxShadow': '0 8px 32px 0 rgba(123,50,191,0.08), 0 1.5px 3px 0 rgba(118, 27, 147, 0.05)',
                'padding': '30px',
                'width': '80%',
                'margin': 'auto'
            }
        )   
    ],
    style={'backgroundColor': colors['background'], 'minHeight': '100vh', 'paddingBottom': '40px', 'fontFamily': font_family}
)
df['Sales_label'] = df['Sales'].apply(lambda x: f"{x:.1f} %")

@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-radio', 'value')
)

def update_graph(selected_region):
    selected_region = selected_region.lower()
    all_regions = df['Region'].unique()
    if selected_region == 'all':
        plot_df = df.sort_values(['Region', 'Date'])
        fig = px.line(
            plot_df,
            x='Date',
            y='Sales',
            color='Region',
            color_discrete_map = region_colors,
            markers=True,
            line_shape='spline',
            text='Sales_label',
            title='Pink Morsels Sales Over Time - All Regions',
            labels={"Date": "Date", "Sales": "Sales (Pounds)", "Region": "region"}
        )
    elif selected_region in all_regions:
        plot_df = df[df['Region'] == selected_region].sort_values('Date')
        fig = px.line(
            plot_df,
            x = "Date",
            y =  "Sales",
            markers=True,
            line_shape='spline',
            text='Sales_label',
            color='Region',
            color_discrete_map = region_colors,
            title = f'Pink Morsels Sales Over Time - {selected_region.capitalize()}  Region',
            labels = {"Date": "Date", "Sales": "Sales (Pounds)", "Region": "Region"},
        )
    else:
        plot_df = df.sort_values(['Region', 'Date'])
        fig = px.line(
            plot_df,
            x='Date',
            y='Sales',
            color='Region',
            markers=True,
            line_shape='spline',
            text='Sales_label',
            title='Pink Morsels Sales Over Time - All Regions',
            labels={'Date': 'Date', 'Sales': 'Sales (Pounds)', 'Region': 'Region'}
        )

    fig.add_vline(x=datetime(2021, 1, 15), line_color="green", line_dash="dash")
    fig.update_xaxes(range=["2021-01-01", "2021-02-28"])

    fig.update_layout(
        plot_bgcolor = colors['panel_bg'],
        paper_bgcolor = colors['background'],
        font_color = colors['text'],
        font_family = font_family,
        title_font = dict(size = 24, color = colors['text']),
        margin = dict(l=50, r=30, t=50, b=40),
        hovermode = 'x'
    )  
    fig.update_traces(textposition='top center', line=dict(width=3), marker=dict(size=7))
    return fig 
    
server = app.server

if __name__ == "__main__":
    app.run.server(debug=True)
