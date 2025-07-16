import csv
from datetime import datetime
from dash import Dash, html, dcc
import plotly.express as px
import os

def get_data(file_path):
    dates, sales = [], []
    if not os.path.exists(file_path):
        return dates, sales
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dates.append(datetime.strptime(row["Date"], "%Y-%m-%d"))
                sales.append(float(row["Sales"]))
            except:
                continue
    return dates, sales

dates, sales = get_data("data_file.csv")

fig = px.line(x=dates, y=sales, title="Pink Morsels Sales Over Time", labels={"x": "Date", "y": "Sales ($)"})
fig.add_vline(x=datetime(2021, 1, 15), line_color="red", line_dash="dash")

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Pink Morsels Sales Report"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)