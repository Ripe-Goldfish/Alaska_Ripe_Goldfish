import plotly.express as px
import pandas as pd
import json

def import_measurements(msm_id):
    with open(f'data/ping_measurement_results/{msm_id}.json') as f:
        data = json.load(f)

    return data

def get_avg_rtt(data):
    # this function sums up the rtt of every hourly measurement and returns the average of the rtts
    all_rtts = []
    for msm in data:
        all_rtts.append(msm["avg"])
    
    avg_rtt = sum(all_rtts)/len(all_rtts)

    return avg_rtt


def create_plot(ping_msm_ids, ping_dsts, lats, longs):
    ping_rtts = []
    for msm_id in ping_msm_ids:
        msm_data = import_measurements(msm_id)
        # get avg rtt for every ongoing ping measurement
        avg_rtt = get_avg_rtt(msm_data)
        ping_rtts.append(avg_rtt)


    
    df = pd.DataFrame({'name':ping_dsts, 'msm_id':ping_msm_ids, 'avg_rtt': ping_rtts, 'lats':lats, 'longs':longs})
    fig = px.scatter_mapbox(
        data_frame=df, 
        lat='lats', 
        lon='longs', 
        color='avg_rtt', 
        text='name',
        hover_name='name', 
        title='Average Packet Round-Trip Time in Urban and Remote Alaska', 
        size=[10]*len(df),
        mapbox_style="open-street-map"
    )

    lat_foc = 63
    lon_foc = -153
    fig.update_layout(
            mapbox = dict(
            center=dict(lat = lat_foc, lon = lon_foc), # center on focus point
            zoom=3
            ))
    fig.show()


# def sample():
#     # Sample data
#     servers = ['Server 1', 'Server 2', 'Server 3', 'Server 4']
#     ping_times = [20, 25, 30, 15]  # Replace with actual ping times in miliseconds

#     # Bar graph
#     fig1 = px.bar(x=servers, y=ping_times, text=ping_times, labels={'x': 'Servers', 'y': 'Ping Time (ms)'},
#                 title='Ping Times for Servers')

#     # Add data labels above the bars
#     fig1.update_traces(texttemplate='%{text} ms', textposition='outside')

#     fig1.show()

#     # Sample data from USGS
#     data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

#     # Drop rows with missing or invalid values in the 'mag'('ping' in our case) column in csv
#     data = data.dropna(subset=['mag'])
#     data = data[data.mag >= 0]

#     # Scatter map
#     fig2 = px.scatter_geo(data, lat='latitude', lon='longitude', color='mag',
#                         hover_name='place', #size='mag',
#                         title='Earthquakes Around the World')

#     # center on Alaska
#     lat_foc = 63
#     lon_foc = -153
#     fig2.update_layout(
#             geo = dict(
#                 projection_scale = 7, # zoom
#                 center=dict(lat = lat_foc, lon = lon_foc), # center on focus point
#             ))

#     fig2.show()

if __name__ == "__main__":
        
    remote_ping_measurements = [
        {63671154 : {'name':"Kotzebue", 'lat':66.9007, 'long':-162.6058}},
        {63671155 : {'name':"Kotzebue", 'lat':66.5, 'long':-162.3}},
        {63671156: {'name':"Nome", 'lat':64.5002, 'long':-165.4222}},
        {63671157: {'name':"Bethel", 'lat':60.7902, 'long':-161.7515}},
        {63671158: {'name':"Alakanuk", 'lat':62.6914, 'long':-164.6493}},
        {63671159: {'name':"Metlakatla", 'lat':55.1221, 'long':-131.5744}},
        {63671160: {'name':"Dillingham", 'lat':59.8666, 'long':-158.5996}},
        {63671161: {'name':"Chevak", 'lat':61.5278, 'long':-165.5786}},
        {63671162: {'name':"Unalaska", 'lat':53.8941, 'long':-166.542}},
        {63671163: {'name':"Nunapitchuk", 'lat':62.5092, 'long':-164.4532}},
        {63671164: {'name':"Utqiagvik", 'lat':71.2346, 'long':-156.8174}}
    ]
    urban_ping_measurements = [
        {63671165 : {'name':"Anchorage", 'lat':61.1704, 'long':-149.88}},
        {63671166 : {'name':"Anchorage", 'lat':61.4, 'long':-149.5}},
        {63671167 : {'name':"Fairbanks", 'lat':64.8575, 'long':-147.849}},
        {63671168 : {'name':"Fairbanks", 'lat':64.5, 'long':-147.5}},
        {63671169 : {'name':"Juneau", 'lat':58.6, 'long':-134.2}},
        {63671170 : {'name':"Juneau", 'lat':58.3699, 'long':-134.589}},
    ]

    # for now, focus on creating one plot per traceroute measurement, every measurement will have 4 probes, 4 traces
    ping_msm_ids = []
    ping_dsts = []
    lats = []
    longs = []

    for msm in remote_ping_measurements:
        (key,value), = msm.items()
        ping_msm_ids.append(key)
        ping_dsts.append(value["name"])
        lats.append(value["lat"])
        longs.append(value["long"])

    for msm in urban_ping_measurements:
        (key,value), = msm.items()
        ping_msm_ids.append(key)
        ping_dsts.append(value["name"])
        lats.append(value["lat"])
        longs.append(value["long"])


    create_plot(ping_msm_ids, ping_dsts, lats, longs)
