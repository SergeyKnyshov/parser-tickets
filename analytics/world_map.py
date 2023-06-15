import plotly.graph_objects as go

class Map:
    def __init__(self):
        self.fig = go.Figure(go.Scattermapbox())

    def show_map(self):
        self.fig.update_layout(

            mapbox={
                'center': {'lon': 10, 'lat': 10},
                'style': "stamen-terrain",
                'center': {'lon': 60, 'lat': 60},
                'zoom': 2})

        self.fig.show()

    def add_way(self, longitude, latitude, dict_of_route):
        route = dict_of_route['origin_city'] + '-' + dict_of_route['destination_city']
        price = dict_of_route['price']
        duration = dict_of_route['duration']
        types = dict_of_route['types']
        
        color_dict = {'Plane': 'steelblue', 'Train': 'tomato'}
        way_color = color_dict[types]
        
        info = f'Рейс:{route}<br>Стоимость:{price}<br>Продолжительность:{duration}'


        self.fig.add_trace(go.Scattermapbox(
            mode="markers+lines",
            lon=longitude,
            lat=latitude,
            marker={'size': 20},
            hoverinfo='text+name',
            hovertext=info,
            name=route,
            textposition='middle center',
            line=dict(color = way_color, width = 2)))