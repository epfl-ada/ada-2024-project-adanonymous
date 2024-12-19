def map_continent(movie_country, continent_data_frame):
    label = continent_data_frame[continent_data_frame['Entity'] == movie_country]['World regions according to OWID']
    if len(label) > 0:
        return label.values[0]
    else:
        return None