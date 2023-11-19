import plotly.graph_objects as go
import numpy as np
import json
import pandas as pd


def import_measurements(msm_id):
    with open(f'data/traceroute_measurement_results/{msm_id}.json') as f:
        data = json.load(f)
    return data

class Graph_Traceroute:
    def __init__(self) -> None:
        self.traceroute_measurements = [
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
        self.df = self._create_dataframe()
        self.fig = go.Figure()
        self._create_plot()
    
    def _create_dataframe(self):
        data = []
        for measurement_id in self.traceroute_measurements:
            measurement_id = list(measurement_id.keys())[0]
            data.extend(import_measurements(measurement_id))
        df = pd.DataFrame(data)
        return df

    def _create_plot(self):
        data = None
        traces_by_measurement_id = {}
        for measurement_id in self.traceroute_measurements:

            id_num = list(measurement_id.keys())[0]

            data = import_measurements(id_num)
            traces_by_measurement_id[id_num] = []

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
                    marker = {'size': 10},
                    visible=False
                )
                # add the probe trace to the plot
                self.fig.add_trace(trace)
                traces_by_measurement_id[id_num].append(trace)
            
        dropdown_options = []
        for measurement_id, traces in traces_by_measurement_id.items():
            option = dict(
                label=str(measurement_id),
                method='update',
                args=[{'visible': [t in traces for t in self.fig.data]}]  # Set visibility based on whether the trace belongs to the selected measurement ID
            )
            dropdown_options.append(option)

        self.fig.update_layout(
            updatemenus=[
                dict(buttons= dropdown_options,
                    direction= "down",
                    showactive=True,
                    xanchor="left",
                    yanchor="top",
                    x=0.95,
                    y=0.93,
                    bgcolor = 'rgba(255, 255, 255, 0.5)',
                    bordercolor = 'rgba(255, 255, 255, 0.5)',
                    font=dict(color="black", size=11)
                    )
            ],
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
    def get_plot(self):
        return self.fig
    def get_df(self):
        return self.df



