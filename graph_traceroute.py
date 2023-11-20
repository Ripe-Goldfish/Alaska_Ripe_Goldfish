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
        self.trace_fig = go.Figure()
        self.traceroute_hops_graph = go.Figure()
        self._create_plot()
        self.create_hop_graph()
    
    def _create_dataframe(self):
        data = []
        for measurement_id in self.traceroute_measurements:
            measurement_id = list(measurement_id.keys())[0]
            data.extend(import_measurements(measurement_id))
        df = pd.DataFrame(data)
        return df


    def create_hop_graph(self):
        df = self.df # get the dataframe
        df['total_hops'] = df['result'].apply(lambda x: len(x))
        df['total_private_hops'] = df['result'].apply(lambda x: sum([1 for hop in x if hop['hop_info']['hop_lat'] == -1]))
        df['source']= df['src_info'].apply(lambda x: x['src_city'])
        df['destination']= df['dst_info'].apply(lambda x: x['dst_city'])
        df['x_label'] = df.apply(lambda x: f"Src: {x['source']}  Dst: {x['destination']}  Probe: {x['prb_id']}", axis=1)
        grouped_data = df[['msm_id','prb_id','source','destination','total_hops']]
        msm_ids = df['msm_id'].unique()
        for msm_id in msm_ids:
            filtered_df = df[df['msm_id'] == msm_id]
            
            # Trace for total_hops
            self.traceroute_hops_graph.add_trace(
                go.Bar(x=filtered_df['x_label'], y=filtered_df['total_hops'], name=f'Total Hops',
                    visible=False, offsetgroup=1),
            )
            
            # Trace for total_private_hops
            self.traceroute_hops_graph.add_trace(
                go.Bar(x=filtered_df['x_label'], y=filtered_df['total_private_hops'], name=f'Private Hops',
                    visible=False, offsetgroup=2),
            )

        # Dropdown buttons for toggling visibility
        dropdown_buttons = []
        for msm_id in msm_ids:
            button = dict(
                label=f'{msm_id}',
                method='update',
                args=[{'visible': [msm_id == msm for msm in msm_ids] * 2},  # Multiply by 2 because there are two sets of traces per msm_id
                    {'title': f'Data for MSM ID: {msm_id}'}]
            )
            dropdown_buttons.append(button)

        self.traceroute_hops_graph.update_layout(
                updatemenus=[
                dict(buttons= dropdown_buttons,
                     visible=False,
                    direction= "down",
                    showactive=False,
                    xanchor="left",
                    yanchor="top",
                    x=0,
                    y=1,
                    bgcolor = 'rgba(255, 255, 255, 0.5)',
                    bordercolor = 'rgba(255, 255, 255, 0.5)',
                    font=dict(color="white", size=11),
                    )
            ],
            paper_bgcolor='black',   # Sets the background color for the entire figure
            plot_bgcolor='black',    # Sets the background color for the plot area
            font_color='white', 
            title='Hops and Private Hops per Traceroute Measurement',
            title_x=0.5,
            xaxis_type='category',
            barmode='group'  # Grouped bar mode
        )

        # Show first set of traces by default
        self.traceroute_hops_graph.data[0].visible = True
        self.traceroute_hops_graph.data[1].visible = True


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

                # add dst  info to lists
                lat_list.append(probe["dst_info"]["dst_lat"])
                long_list.append(probe["dst_info"]["dst_long"])
                ip_list.append(probe["dst_addr"])
                city_list.append(probe["dst_info"]["dst_city"])
                isp_list.append(probe["dst_info"]["dst_isp"])
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
                custom_data = {
                    'latitudes': lat_list,
                    'longitudes': long_list,
                    'ip': ip_list,
                    'cities': city_list,
                    'isp': isp_list
                }
                df = pd.DataFrame(custom_data)
                # create trace for probe
                trace = go.Scattermapbox(
                    customdata = np.stack((df['latitudes'], df['longitudes'], df['ip'], df['cities'], df['isp']), axis=-1),
                    hovertemplate='<b>Latitude</b>: %{customdata[0]}<br>' +
                                '<b>Longitude</b>: %{customdata[1]}<br>' +
                                '<b>IP Address</b>: %{customdata[2]}<br>' +
                                '<b>City</b>: %{customdata[3]}<br>' +
                                '<b>ISP</b>: %{customdata[4]}<br>' +
                                '<extra></extra>',
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
                self.trace_fig.add_trace(trace)
                traces_by_measurement_id[id_num].append(trace)
            
        dropdown_options = []
        for measurement_id, traces in traces_by_measurement_id.items():
            option = dict(
                label=str(measurement_id),
                method='update',
                args=[{'visible': [t in traces for t in self.trace_fig.data]}]  # Set visibility based on whether the trace belongs to the selected measurement ID
            )
            dropdown_options.append(option)

        self.trace_fig.update_layout(
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
        self.trace_fig.data[0].visible = True
        self.trace_fig.data[1].visible = True
        self.trace_fig.data[2].visible = True
        self.trace_fig.data[3].visible = True
    def get_plot(self):
        return self.trace_fig
    def get_df(self):
        return self.df