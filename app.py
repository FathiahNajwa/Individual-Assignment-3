# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests

# Import the CSV file
df = pd.read_csv(r'C:\Users\user\Desktop\assignment3\poslaju_sla.csv')

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Handle 'SLA Performance' column with percentages
# Remove '%' and convert to numeric
df['SLA Performance'] = pd.to_numeric(df['SLA Performance'].str.rstrip('%'), errors='coerce')

# Drop rows with NaN values after conversion
df = df.dropna(subset=['SLA Performance'])

# Group by 'Date' and find the mean of 'SLA Performance'
df_grouped_day = df.groupby(df['Date'].dt.date)['SLA Performance'].mean().reset_index()
df_grouped_day['Date'] = pd.to_datetime(df_grouped_day['Date'])

# Group by 'Month' for Bar Chart
df['Month'] = df['Date'].dt.to_period('M')
df_grouped_month = df.groupby(df['Month'])['SLA Performance'].mean().reset_index()
df_grouped_month['Month'] = df_grouped_month['Month'].dt.to_timestamp()

# Group by 'Year' for Pie Chart
df['Year'] = df['Date'].dt.to_period('Y')
df_grouped_year = df.groupby(df['Year'])['SLA Performance'].mean().reset_index()
df_grouped_year['Year'] = df_grouped_year['Year'].dt.to_timestamp()

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1('Average SLA Performance'),
    html.Div([
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Time Series Line Chart', 'value': 'line'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Pie Chart', 'value': 'pie'},
                {'label': 'Heatmap', 'value': 'heatmap'}
            ],
            value='line'
        )
    ]),
    dcc.Graph(id='chart'),
])

# Define callback to update chart
@app.callback(
    Output('chart', 'figure'),
    [Input('chart-type', 'value')]
)
def update_chart(selected_chart):
    if selected_chart == 'line':
        return px.line(df_grouped_day, x='Date', y='SLA Performance')
    elif selected_chart == 'bar':
        return px.bar(df_grouped_month, x='Month', y='SLA Performance')
    elif selected_chart == 'pie':
        return px.pie(df_grouped_year, names='Year', values='SLA Performance')
    elif selected_chart == 'heatmap':
        df_heatmap = df.pivot_table(index=df['Date'].dt.month, columns=df['Date'].dt.year, values='SLA Performance', aggfunc='mean')
        return px.imshow(df_heatmap)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
