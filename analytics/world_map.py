import plotly.graph_objects as go

class Map:
    def __init__(self):
        self.fig = go.Figure(go.Scattermapbox())

    def show_map(self):
        self.fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 10, 'lat': 10},
                'style': "stamen-terrain",
                'center': {'lon': 60, 'lat': 60},
                'zoom': 2})

        self.fig.show()
        
    def add_way(self, longitude, latitude):
        self.fig.add_trace(go.Scattermapbox(
            mode = "markers+lines",
            lon = longitude,
            lat = latitude,
            marker = {'size': 10}))



# fig = go.Figure(go.Scattermapbox())
    # mode = "markers+lines",
    # lon = [37.61492157, 61.39356613],
    # lat = [55.75654221, 55.16012573],
    # marker = {'size': 10}))