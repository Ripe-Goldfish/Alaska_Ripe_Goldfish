import plotly.express as px
import pandas as pd

# Sample data
servers = ['Server 1', 'Server 2', 'Server 3', 'Server 4']
ping_times = [20, 25, 30, 15]  # Replace with actual ping times in miliseconds

# Bar graph
fig1 = px.bar(x=servers, y=ping_times, text=ping_times, labels={'x': 'Servers', 'y': 'Ping Time (ms)'},
             title='Ping Times for Servers')

# Add data labels above the bars
fig1.update_traces(texttemplate='%{text} ms', textposition='outside')

fig1.show()

# Sample data from USGS
data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

# Drop rows with missing or invalid values in the 'mag'('ping' in our case) column in csv
data = data.dropna(subset=['mag'])
data = data[data.mag >= 0]

# Scatter map
fig2 = px.scatter_geo(data, lat='latitude', lon='longitude', color='mag',
                     hover_name='place', #size='mag',
                     title='Earthquakes Around the World')

# center on Alaska
lat_foc = 63
lon_foc = -153
fig2.update_layout(
        geo = dict(
            projection_scale = 7, # zoom
            center=dict(lat = lat_foc, lon = lon_foc), # center on focus point
        ))

fig2.show()