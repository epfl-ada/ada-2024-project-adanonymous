import plotly.graph_objects as go
from plotly.subplots import make_subplots




def plotly_key_words_occ_zoomed(key_words_occ_df, key_words):
    colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
    ]
      
    df_key_words_occ_reset = key_words_occ_df.reset_index()
    key_words_occ_df_zoomed = df_key_words_occ_reset[((1992 <= df_key_words_occ_reset['Movie_release_date']) * (df_key_words_occ_reset['Movie_release_date'] <= 2013)) == 1]
    key_words_occ_df_zoomed = key_words_occ_df_zoomed.set_index(keys='Movie_release_date')

    col_name_of_key_words = ['Count_of_' + '_'.join(word.split(' ')) for word in key_words]
    n_key_words = len(key_words)

    # fig, ax = plt.subplots(math.ceil(n_key_words/2), 2, figsize= (math.ceil(n_key_words/2)*6, 8), sharey = True, sharex = True)
    fig = go.Figure()
    show = [False for i in range(n_key_words)]
    buttons = []
    show = [False for i in range(n_key_words)]
    r = dict(label = "All", method = "update", args = [{"visible": [True for i in range(n_key_words)], "title": "All"}])
    buttons.append(r)
    for i in range(n_key_words):
        #sbplt = ax[i%math.ceil(n_key_words/2), math.floor(i/math.ceil(n_key_words/2))]
        col_name = col_name_of_key_words[i]
        fig.add_trace(go.Scatter(x=key_words_occ_df_zoomed.index, y=key_words_occ_df_zoomed[col_name], name=key_words[i], showlegend=True,line=dict(color=colors[i])))
        show_this_genre = show.copy()
        show_this_genre[i] = True
    
        r = dict(label = key_words[i], method = "update", args = [{"visible": show_this_genre, "title": key_words[i]}])
        buttons.append(r)

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list(buttons),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                y = 1.2,
                x = 1,
                xanchor="left",
                yanchor="top",
            ),
        ]
    )
    fig.update_layout(title_text="Occurence of key words in plot summaries")
    fig.update_xaxes(title_text="Year of release")
    fig.update_yaxes(title_text="Number of occurences of the word")
    fig.show()
    fig.write_html("src/figures/9_11_key_words_occurence.html")


def ploltly_percentage_movies(data,data2, genres, year_initial, year_end, focus_year,nrows,ncols):
    colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]
    fig = make_subplots(rows=2, cols=1,subplot_titles=("US movies", "Non US Movies"))
    show = [False for i in range(nrows*ncols*2)]
    buttons = []
    r = dict(label = "All", method = "update", args = [{"visible": [True for i in range(nrows*ncols)], "title": "All"}])
    buttons.append(r)
    for i in range(nrows):
        for j in range(ncols):
            genre = genres[i*ncols+j]

            movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
            movies_year.columns = ["year", "count"]
            yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')
            x = movies_year.loc[(movies_year.year > year_initial  )&( movies_year.year < year_end)]["year"]
            y = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index < year_end)].values*100
            fig.add_trace(
                go.Scatter(x = x, y = y, mode = 'lines', name = genre,legendgroup=genre,showlegend=True,line=dict(color=colors[i*ncols+j])),
                row = 1, col = 1
                )
    

            movies_year2 = data2.groupby(data2.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
            movies_year2.columns = ["year", "count"]
            yearly_movies2 = data2.groupby(data2.Movie_release_date.dt.year)['nb_genre'].agg('sum')
            x = movies_year2.loc[(movies_year2.year > year_initial  )&( movies_year2.year < year_end)]["year"]
            y = movies_year2.loc[(movies_year2.year>year_initial) & (movies_year2.year<year_end)]["count"]/yearly_movies2[(yearly_movies2.index >year_initial) & (yearly_movies2.index < year_end)].values*100
            fig.add_trace(
                go.Scatter(x = x, y = y, mode = 'lines', name = genre,legendgroup=genre,showlegend=False,line=dict(color=colors[i*ncols+j])),
                row = 2, col = 1,
            )



            show_this_genre = show.copy()
            show_this_genre[(i*ncols+j)*2] = True
            show_this_genre[(i*ncols+j)*2+1] = True
            #show_this_genre[i*ncols+j+nrows*ncols] = True
            print(show_this_genre)
            r = dict(label = genre, method = "update", args = [{"visible": show_this_genre, "title": genre}])
            buttons.append(r)
    
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list(buttons),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                y = 1.2,
                x = 1,
                xanchor="left",
                yanchor="top",
            ),
        ]
    )
    fig.add_vline(x=focus_year, line_dash="dash", line_color="red", line_width=1)
    fig.update_layout(title_text="Genre distribution")
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Percentage of movies")
    fig.show()
    fig.write_html("src/figures/movie_genre_us.html")




def ploltly_percentage_movies_ww2(data, genres, year_initial, year_end, focus_year,nrows,ncols):
    colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]
    fig = go.Figure()
    show = [False for i in range(nrows*ncols)]
    buttons = []
    r = dict(label = "All", method = "update", args = [{"visible": [True for i in range(nrows*ncols)], "title": "All"}])
    buttons.append(r)
    for i in range(nrows):
        for j in range(ncols):
            genre = genres[i*ncols+j]

            movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
            movies_year.columns = ["year", "count"]
            yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')
            x = movies_year.loc[(movies_year.year > year_initial  )&( movies_year.year < year_end)]["year"]
            y = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index < year_end)].values*100
            fig.add_trace(
                go.Scatter(x = x, y = y, mode = 'lines', name = genre,legendgroup=genre,showlegend=True,line=dict(color=colors[i*ncols+j]))
                )


            show_this_genre = show.copy()
            show_this_genre[(i*ncols+j)] = True
            #show_this_genre[i*ncols+j+nrows*ncols] = True
            print(show_this_genre)
            r = dict(label = genre, method = "update", args = [{"visible": show_this_genre, "title": genre}])
            buttons.append(r)
    
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list(buttons),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                y = 1.2,
                x = 1,
                xanchor="left",
                yanchor="top",
            ),
        ]
    )
    fig.add_vline(x=focus_year, line_dash="dash", line_color="red", line_width=1)
    fig.update_layout(title_text="Genre distribution")
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Percentage of movies")
    fig.show()
    fig.write_html("src/figures/movie_genre_us_ww2.html")


def plotly_plot_movie_genre(df1,df2):
    color1 = 'blue'
    color2 = 'orange'
    fig = make_subplots(rows=2, cols=1,subplot_titles=("US movies", "Non US Movies"))
    fig.update_layout(height=800,width = 800, title_text="Genre distribution before and after event")

    fig.add_trace(go.Bar(x=df1.genre, y=df1['count_before'], name='Before event', marker_color=color1), row=1, col=1)
    fig.add_trace(go.Bar(x=df1.genre, y=df1['count_after'], name='After event', marker_color=color2), row=1, col=1)    
    fig.add_trace(go.Bar(x=df2.genre, y=df2['count_before'], name='Before event', marker_color=color1,showlegend =  False), row=2, col=1)
    fig.add_trace(go.Bar(x=df2.genre, y=df2['count_after'], name='After event', marker_color=color2,showlegend =  False), row=2, col=1)
    fig.update_yaxes(title_text="Percentage (%)", row=1, col=1)
    fig.update_yaxes(title_text="Percentage (%)", row=2, col=1)
    fig.show()
    fig.write_html("src/figures/movie_genre_us_bar.html")