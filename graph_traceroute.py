import plotly.graph_objects as go
import numpy as np
import json

def import_measurements(msm_id):
    with open(f'data/traceroute_measurement_results/{msm_id}.json') as f:
        data = json.load(f)

    return data


def create_plot(data):
    fig = go.Figure()

    for probe in data:
        lat_list = []
        long_list = []
        ip_list = []

        # add src info to lists
        lat_list.append(probe["src_info"]["src_lat"])
        long_list.append(probe["src_info"]["src_long"])
        ip_list.append(probe["src_addr"])
        
        # add hop info to lists
        for hop in probe["result"]:
            # if the hop was successful AND geolocation was successfully obtained, maybe rework this later
            if hop["hop_info"]["hop_lat"] != -1:
                lat_list.append(hop["hop_info"]["hop_lat"])
                long_list.append(hop["hop_info"]["hop_long"])
                ip_list.append(hop["from"])


        # add dst  info to lists
        lat_list.append(probe["dst_info"]["dst_lat"])
        long_list.append(probe["dst_info"]["dst_long"])
        ip_list.append(probe["dst_addr"])

        # math on crossing meridian
        latitudes= np.array(lat_list)
        longitudes= np.array(long_list)

        # Math on longitude to cross 180-degree meridian
        diffs=np.diff(longitudes)

        crossings_plusminus=np.where(diffs<=-180)[0]
        crossing_minusplus=np.where(diffs>180)[0]

        for plusmin_crossing in crossings_plusminus:
            longitudes[plusmin_crossing+1:]+=360

        for minusplus_crossing in crossing_minusplus:
            longitudes[minusplus_crossing+1:]-=360

        # create trace for probe
        trace = go.Scattermapbox(
            text = ip_list,
            textposition='top right',
            hoverinfo='none',
            name = probe["prb_id"],
            mode = "markers+lines+text",
            lon = longitudes,
            lat = latitudes,
            marker = {'size': 10}
        )
        # add the probe trace to the plot
        fig.add_trace(trace)
    
    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'style': "open-street-map",
            'center': {'lon': -153, 'lat': 63},
            'zoom': 2
            },
        legend = {
            "x":0,
            "y":1,
            "xanchor" : "left",
            "yanchor" : "top"
        }
    )
    
    fig.show()
    
# # lat/lon hops of first traceroute
# data = [
#     {
#         "from": "65.74.66.47",
#         "lat": 55.3422,
#         "long": -131.6461,
#     },
#     {
#         "hop": 9,
#         "from": "152.44.129.1",
#         "lat": 47.6043,
#         "long": -122.3298,
#         "avg_rtt": 37.8
#     },
#     {
#         "hop": 10,
#         "from": "65.50.198.63",
#         "lat": 37.3230,
#         "long": -122.0322,
#         "avg_rtt": 37.8
#     },
#     {
#         "hop": 11,
#         "from": "174.127.136.155",
#         "lat": 47.6043,
#         "long": -122.3298,
#         "avg_rtt": 41
#     },
#     {
#         "hop": 12,
#         "from": "174.127.136.151",
#         "lat": 47.6043,
#         "long": -122.3298,
#         "avg_rtt": 42
#     },
#     {
#         "hop": 13,
#         "from": "174.127.149.90",
#         "lat": 47.6043,
#         "long": -122.3298,
#         "avg_rtt": 43
#     },
#     {
#         "hop": 14,
#         "from": "192.175.30.30",
#         "lat": 37.3230,
#         "long": -122.0322,
#         "avg_rtt": 50
#     },
#     {
#         "hop": 16,
#         "from": "206.223.117.66",
#         "lat": 37.5324,
#         "long": -122.2488,
#         "avg_rtt": 51.5
#     },
#     {
#         "hop": 17,
#         "from": "103.200.13.248",
#         "lat": -31.9522,
#         "long": 115.8614,
#         "avg_rtt": 203
#     },
#     {
#         "hop": 18,
#         "from": "103.200.13.64",
#         "lat": -31.9522,
#         "long": 115.8614,
#         "avg_rtt": 200
#     },
#     {
#         "hop": 19,
#         "from": "203.153.18.241",
#         "lat": -33.8678,
#         "long": 151.2070,
#         "avg_rtt": 300
#     }
# ]

# lat = np.array([d['lat'] for d in data])
# lon = np.array([d['long'] for d in data])
# ip = [d['from'] for d in data]

# # Math on longitude to cross 180-degree meridian
# diffs=np.diff(lon)

# crossings_plusminus=np.where(diffs<=-180)[0]
# crossing_minusplus=np.where(diffs>180)[0]

# for plusmin_crossing in crossings_plusminus:
#     lon[plusmin_crossing+1:]+=360

# for minusplus_crossing in crossing_minusplus:
#     lon[minusplus_crossing+1:]-=360

# fig = go.Figure(go.Scattermapbox(
#     hovertext = ip,
#     mode = "markers+lines",
#     lon = lon,
#     lat = lat,
#     marker = {'size': 10}))

# # sample fig to add a second traceroute
# fig.add_trace(go.Scattermapbox(
#     hovertext = "sample text",
#     mode = "markers+lines",
#     lon = [-50, -60,40],
#     lat = [30, 10, -20],
#     marker = {'size': 10}))

# # Alaska lat/lon in degrees N and E: 66/-153

# fig.update_layout(
#     margin ={'l':0,'t':0,'b':0,'r':0},
#     mapbox = {
#         'style': "open-street-map",
#         'center': {'lon': -153, 'lat': 63},
#         'zoom': 2})

# fig.show()



if __name__ == "__main__":
        
        # probes used in measurements
        traceroute_measurements = [
            {63715139: "Sao Paulo"}, 
            {63715140: "Santiago de Chile"}, 
            {63715141 : "Quito"}, 
            # {63715142 : "New York City"}, # ip-api thinks nyc is germany
            {63715143 : "Montreal"}, 
            {63715144 : "Cape Town"}, 
            {63715145 : "Nairobi"}, 
            {63715146 : "Berlin"}, 
            {63715147 : "Moscow"}, 
            {63715148 : "Khabarovsk"}, 
            {63715149 : "Astana"}, 
            {63715150 : "Tokyo"}, 
            {63715151 : "Sydney"},
            {63715152 : "Wellington"}, 
            {63715153 : "Delhi"}, 
            # {63715154 : "Singapore" } # not a success
        ]

        # for now, focus on creating one plot per traceroute measurement, every measurement will have 4 probes, 4 traces
        data = import_measurements(msm_id = 63715147)
        create_plot(data)

