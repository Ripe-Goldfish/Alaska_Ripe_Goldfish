import plotly.graph_objects as go

# lat/lon hops of first traceroute
data = [
    {
        "lat": 55.3422,
        "long": -131.6461,
    },
    {
        "hop": 9,
        "from": "152.44.129.1",
                "lat": 47.6043,
                "long": -122.3298,
                "avg_rtt": 37.8
    },
    {
        "hop": 10,
        "from": "65.50.198.63",
                "lat": 37.3230,
                "long": -122.0322,
                "avg_rtt": 37.8
    },
    {
        "hop": 11,
        "from": "174.127.136.155",
                "lat": 47.6043,
                "long": -122.3298,
                "avg_rtt": 41
    },
    {
        "hop": 12,
        "from": "174.127.136.151",
                "lat": 47.6043,
                "long": -122.3298,
                "avg_rtt": 42
    },
    {
        "hop": 13,
        "from": "174.127.149.90",
                "lat": 47.6043,
                "long": -122.3298,
                "avg_rtt": 43
    },
    {
        "hop": 14,
        "from": "192.175.30.30",
                "lat": 37.3230,
                "long": -122.0322,
                "avg_rtt": 50
    },
    {
        "hop": 16,
        "from": "206.223.117.66",
                "lat": 37.5324,
                "long": -122.2488,
                "avg_rtt": 51.5
    },
    {
        "hop": 17,
        "from": "103.200.13.248",
                "lat": -31.9522,
                "long": 115.8614,
                "avg_rtt": 203
    },
    {
        "hop": 18,
        "from": "103.200.13.64",
                "lat": -31.9522,
                "long": 115.8614,
                "avg_rtt": 200
    },
    {
        "hop": 19,
        "from": "203.153.18.241",
                "lat": -33.8678,
                "long": 151.2070,
                "avg_rtt": 300
    }
]

lat = [d['lat'] for d in data]
lon = [d['long'] for d in data]

fig = go.Figure(go.Scattermapbox(
    hovertext = "sample text",
    mode = "markers+lines",
    lon = lon,
    lat = lat,
    marker = {'size': 10}))

fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = [-50, -60,40],
    lat = [30, 10, -20],
    marker = {'size': 10}))

# Alaska lat/lon in degrees N and E: 66/-153 zoom: 3

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'style': "open-street-map",
        'center': {'lon': -153, 'lat': 63},
        'zoom': 3})

fig.show()
