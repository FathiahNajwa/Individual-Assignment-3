import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load your data (replace this with your data loading logic)
df = pd.read_csv(r'C:\Users\user\Desktop\assignment3\poslaju_sla.csv')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Dropdown for selecting months
    dcc.Dropdown(
        id='month-dropdown',
        options=[
            {'label': month, 'value': month} for month in df['Date'].dt.strftime('%B').unique()
        ],
        value=df['Date'].dt.strftime('%B').unique()[0],  # Set default value to the first month
        multi=False,
        style={'width': '50%'}
    ),
    # Combined Bar and Line chart
    dcc.Graph(id='combined-chart'),
])

# Define callback to update the combined chart based on the selected month
@app.callback(
    Output('combined-chart', 'figure'),
    [Input('month-dropdown', 'value')]
)
def update_combined_chart(selected_month):
    selected_month_df = df[df['Date'].dt.strftime('%B') == selected_month]

    # Sort DataFrame by 'Date'
    selected_month_df = selected_month_df.sort_values(by='Date')

    # Create subplots with two vertical subplots
    fig = make_subplots(rows=2, cols=1, subplot_titles=['Combined Bar Chart', 'Time Series Line Chart'])

    # Bar chart for 'SLA Performance' and 'Total Expected Delivery'
    fig.add_trace(go.Bar(x=selected_month_df['Date'], y=selected_month_df['SLA Performance'],
                         name='SLA Performance', marker_color='purple'), row=1, col=1)

    fig.add_trace(go.Bar(x=selected_month_df['Date'], y=selected_month_df['Total Expected Delivery'],
                         name='Total Expected Delivery', marker_color='orange', opacity=0.7), row=1, col=1)


    # Sort DataFrame by 'SLA Performance' for the line chart
    selected_month_df_line = selected_month_df.sort_values(by='SLA Performance')

    # Scatter plot for 'SLA Performance'
    fig.add_trace(go.Scatter(x=selected_month_df_line['Date'], y=selected_month_df_line['SLA Performance'],
        mode='markers', name='SLA Performance', marker=dict(color='green', size=8)), row=2, col=1)


    fig.update_layout(
        title_text=f'Combined Chart for {selected_month}',
        height=800,  # Adjust the height of the entire figure
        showlegend=False,  # Hide the legend for the combined chart
        xaxis_title='Date',
        yaxis_title='Values'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
