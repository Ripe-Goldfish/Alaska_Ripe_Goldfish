import plotly.graph_objects as go
import numpy as np
import pandas as pd
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
        city_list = []
        isp_list = []

        # add src info to lists
        lat_list.append(probe["src_info"]["src_lat"])
        long_list.append(probe["src_info"]["src_long"])
        ip_list.append(probe["src_addr"])
        city_list.append(probe["src_info"]["src_city"])
        isp_list.append(probe["src_info"]["src_isp"])
        
        # add hop info to lists
        for hop in probe["result"]:
            # if the hop was successful AND geolocation was successfully obtained, maybe rework this later
            if hop["hop_info"]["hop_lat"] != -1:
                lat_list.append(hop["hop_info"]["hop_lat"])
                long_list.append(hop["hop_info"]["hop_long"])
                ip_list.append(hop["from"])
                city_list.append(hop["hop_info"]["hop_city"])
                isp_list.append(hop["hop_info"]["hop_isp"])

        # add dst info to lists
        lat_list.append(probe["dst_info"]["dst_lat"])
        long_list.append(probe["dst_info"]["dst_long"])
        ip_list.append(probe["dst_addr"])
        city_list.append(probe["dst_info"]["dst_city"])
        isp_list.append(probe["dst_info"]["dst_isp"])

        # math on longitude to cross 180-degree meridian
        longitudes= np.array(long_list) # turn list into np array for np.diff
        diffs=np.diff(longitudes)

        # create custom data dataframe
        custom_data = {
            'latitudes': lat_list,
            'longitudes': long_list,
            'ip': ip_list,
            'cities': city_list,
            'isp': isp_list
        }
        df = pd.DataFrame(custom_data)

        crossings_plusminus=np.where(diffs<=-180)[0]
        crossing_minusplus=np.where(diffs>180)[0]

        for plusmin_crossing in crossings_plusminus:
            longitudes[plusmin_crossing+1:]+=360

        for minusplus_crossing in crossing_minusplus:
            longitudes[minusplus_crossing+1:]-=360

        # create trace for probe
        trace = go.Scattermapbox(
            customdata = np.stack((df['latitudes'], df['longitudes'], df['ip'], df['cities'], df['isp']), axis=-1),
            hovertemplate='<b>Latitude</b>: %{customdata[0]}<br>' +
                          '<b>Longitude</b>: %{customdata[1]}<br>' +
                          '<b>IP Address</b>: %{customdata[2]}<br>' +
                          '<b>City</b>: %{customdata[3]}<br>' +
                          '<b>ISP</b>: %{customdata[4]}<br>' +
                          '<extra></extra>',
            name = probe["prb_id"],
            mode = "markers+lines+text",
            lat = lat_list,
            lon = longitudes,
            marker = {'size': 10}
        )
        # add the probe trace to the plot
        fig.add_trace(trace)
        fig.update_layout(
            title="Traceroutes to " + probe["dst_info"]["dst_city"],
            title_font_family="Times New Roman"
            )
    
    fig.update_layout(
        margin ={'l':30,'t':30,'b':30,'r':30},
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
        for msm in traceroute_measurements:
            (key,value), = msm.items()
            data = import_measurements(msm_id = key)
            create_plot(data)

