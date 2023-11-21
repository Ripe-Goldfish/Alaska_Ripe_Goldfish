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
    avg_rtt = round(avg_rtt, 4)

    return avg_rtt


# ping rtt heatmap with the dots
def create_scattermap(ping_msm_ids, ping_dsts, lats, longs):
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


# bar graphs
def create_remoteAK_bar_graph(ping_msm_ids, ping_dsts):
    ping_rtts = []
    for msm_id in ping_msm_ids:
        msm_data = import_measurements(msm_id)
        # get avg rtt for every ongoing ping measurement
        avg_rtt = get_avg_rtt(msm_data)
        ping_rtts.append(avg_rtt)

    fig = px.bar(x=ping_dsts, y=ping_rtts, text=ping_rtts, labels={'x':'Remote Alaska Destinations', 'y':'Ping Time (ms)'}, title='Ping Time for Remote Alaska Destinations')
    fig.update_traces(texttemplate='%{text} ms', textposition='outside')

    fig.show()


def create_urbanAK_bar_graph(ping_msm_ids, ping_dsts):
    ping_rtts = []
    for msm_id in ping_msm_ids:
        msm_data = import_measurements(msm_id)
        # get avg rtt for every ongoing ping measurement
        avg_rtt = get_avg_rtt(msm_data)
        ping_rtts.append(avg_rtt)

    fig = px.bar(x=ping_dsts, y=ping_rtts, text=ping_rtts, labels={'x':'Urban Alaska Destinations', 'y':'Ping Time (ms)'}, title='Ping Time for Urban Alaska Destinations')
    fig.update_traces(texttemplate='%{text} ms', textposition='outside')

    fig.show()


def extract_heatmap_data(msm_data):
    # get all night, morning, afternoon, evening rtts averaged
    
    pass

# squares heatmap
def create_heatmap(msm_id):
    msm_data = import_measurements(msm_id)
    heatmap_data = extract_heatmap_data(msm_data)

    x = ['Morning', 'Afternoon', 'Evening', 'Night']
    y = ['11/15', '11/16', '11/17', '11/18', '11/19', '11/20']
    # night: 0:00 - 6:00
    # morngin: 6:00 - 12:00
    # afternoon: 12:00 - 17:00
    # evning: 17:00 - 22:00
    pass



class Graph_Ping(): 
    # ping rtt heatmap with the dots
    def create_scattermap(self):
        remote_ping_measurements = [
            {63671154 : {'name':"Kotzebue 1", 'lat':66.9007, 'long':-162.6058}},
            {63671155 : {'name':"Kotzebue 2", 'lat':66.5, 'long':-162.3}},
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
            {63671165 : {'name':"Anchorage 1", 'lat':61.1704, 'long':-149.88}},
            {63671166 : {'name':"Anchorage 2", 'lat':61.4, 'long':-149.5}},
            {63671167 : {'name':"Fairbanks 1", 'lat':64.8575, 'long':-147.849}},
            {63671168 : {'name':"Fairbanks 2", 'lat':64.5, 'long':-147.5}},
            {63671169 : {'name':"Juneau 1", 'lat':58.6, 'long':-134.2}},
            {63671170 : {'name':"Juneau 2", 'lat':58.3699, 'long':-134.589}},
        ]

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

        return fig


    # bar graphs
    def create_remoteAK_bar_graph(self):
        remote_ping_measurements = [
            {63671154 : {'name':"Kotzebue 1", 'lat':66.9007, 'long':-162.6058}},
            {63671155 : {'name':"Kotzebue 2", 'lat':66.5, 'long':-162.3}},
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
    
        ping_msm_ids = []
        ping_dsts = []
        for msm in remote_ping_measurements:
            (key,value), = msm.items()
            ping_msm_ids.append(key)
            ping_dsts.append(value["name"])

        ping_rtts = []
        for msm_id in ping_msm_ids:
            msm_data = import_measurements(msm_id)
            # get avg rtt for every ongoing ping measurement
            avg_rtt = get_avg_rtt(msm_data)
            ping_rtts.append(avg_rtt)

        fig = px.bar(x=ping_dsts, y=ping_rtts, text=ping_rtts, labels={'x':'Remote Alaska Destinations', 'y':'Ping Time (ms)'}, title='Ping Time for Remote Alaska Destinations')
        fig.update_traces(texttemplate='%{text} ms', textposition='outside')

        return fig


    def create_urbanAK_bar_graph(self):
        urban_ping_measurements = [
            {63671165 : {'name':"Anchorage 1", 'lat':61.1704, 'long':-149.88}},
            {63671166 : {'name':"Anchorage 2", 'lat':61.4, 'long':-149.5}},
            {63671167 : {'name':"Fairbanks 1", 'lat':64.8575, 'long':-147.849}},
            {63671168 : {'name':"Fairbanks 2", 'lat':64.5, 'long':-147.5}},
            {63671169 : {'name':"Juneau 1", 'lat':58.6, 'long':-134.2}},
            {63671170 : {'name':"Juneau 2", 'lat':58.3699, 'long':-134.589}},
        ]

        ping_msm_ids = []
        ping_dsts = []
        for msm in urban_ping_measurements:
            (key,value), = msm.items()
            ping_msm_ids.append(key)
            ping_dsts.append(value["name"])

        ping_rtts = []
        for msm_id in ping_msm_ids:
            msm_data = import_measurements(msm_id)
            # get avg rtt for every ongoing ping measurement
            avg_rtt = get_avg_rtt(msm_data)
            ping_rtts.append(avg_rtt)

        fig = px.bar(x=ping_dsts, y=ping_rtts, text=ping_rtts, labels={'x':'Urban Alaska Destinations', 'y':'Ping Time (ms)'}, title='Ping Time for Urban Alaska Destinations')
        fig.update_traces(texttemplate='%{text} ms', textposition='outside')

        return fig





# if __name__ == "__main__":
        
#     # latlongs added manually
#     remote_ping_measurements = [
#         {63671154 : {'name':"Kotzebue 1", 'lat':66.9007, 'long':-162.6058}},
#         {63671155 : {'name':"Kotzebue 2", 'lat':66.5, 'long':-162.3}},
#         {63671156: {'name':"Nome", 'lat':64.5002, 'long':-165.4222}},
#         {63671157: {'name':"Bethel", 'lat':60.7902, 'long':-161.7515}},
#         {63671158: {'name':"Alakanuk", 'lat':62.6914, 'long':-164.6493}},
#         {63671159: {'name':"Metlakatla", 'lat':55.1221, 'long':-131.5744}},
#         {63671160: {'name':"Dillingham", 'lat':59.8666, 'long':-158.5996}},
#         {63671161: {'name':"Chevak", 'lat':61.5278, 'long':-165.5786}},
#         {63671162: {'name':"Unalaska", 'lat':53.8941, 'long':-166.542}},
#         {63671163: {'name':"Nunapitchuk", 'lat':62.5092, 'long':-164.4532}},
#         {63671164: {'name':"Utqiagvik", 'lat':71.2346, 'long':-156.8174}}
#     ]
#     urban_ping_measurements = [
#         {63671165 : {'name':"Anchorage 1", 'lat':61.1704, 'long':-149.88}},
#         {63671166 : {'name':"Anchorage 2", 'lat':61.4, 'long':-149.5}},
#         {63671167 : {'name':"Fairbanks 1", 'lat':64.8575, 'long':-147.849}},
#         {63671168 : {'name':"Fairbanks 2", 'lat':64.5, 'long':-147.5}},
#         {63671169 : {'name':"Juneau 1", 'lat':58.6, 'long':-134.2}},
#         {63671170 : {'name':"Juneau 2", 'lat':58.3699, 'long':-134.589}},
#     ]



#     ping_msm_ids = []
#     ping_dsts = []
#     lats = []
#     longs = []

#     for msm in remote_ping_measurements:
#         (key,value), = msm.items()
#         ping_msm_ids.append(key)
#         ping_dsts.append(value["name"])
#         lats.append(value["lat"])
#         longs.append(value["long"])

#     for msm in urban_ping_measurements:
#         (key,value), = msm.items()
#         ping_msm_ids.append(key)
#         ping_dsts.append(value["name"])
#         lats.append(value["lat"])
#         longs.append(value["long"])

#     # plot 1
#     create_scattermap(ping_msm_ids, ping_dsts, lats, longs)

#     # Making separate graphs for remote and urban ping measurements
#     remote_ping_msm_ids = []
#     remote_ping_dsts = []
#     for msm in remote_ping_measurements:
#         (key,value), = msm.items()
#         remote_ping_msm_ids.append(key)
#         remote_ping_dsts.append(value["name"])
#     urban_ping_msm_ids = []
#     urban_ping_dsts = []
#     for msm in urban_ping_measurements:
#         (key,value), = msm.items()
#         urban_ping_msm_ids.append(key)
#         urban_ping_dsts.append(value["name"])

#     # graphs
#     create_remoteAK_bar_graph(remote_ping_msm_ids, remote_ping_dsts)
#     create_urbanAK_bar_graph(urban_ping_msm_ids, urban_ping_dsts)

#     # heatmap TODO
#     for msm_id in ping_msm_ids:
#         create_heatmap(msm_id)
