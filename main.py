import plotly.graph_objects as go

class Map:
    def __init__(self):
        self.fig = go.Figure(go.Scattermapbox())

    def show_map(self):
        self.fig.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
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
        info = f'Рейс:{route}<br>Стоимость:{price}<br>Продолжительность:{duration}'

        self.fig.add_trace(go.Scattermapbox(
            mode="markers+lines",
            lon=longitude,
            lat=latitude,
            marker={'size': 20},
            hoverinfo='text',
            text=info))


# Пример использования
m = Map()
m.add_way([-74, -73.9, -73.75], [40.7, 40.7, 40.65], {'origin_city': 'New York', 'destination_city': 'Newark', 'price': 100, 'duration': '1 hour'})
m.show_map()