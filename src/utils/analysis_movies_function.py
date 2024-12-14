import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn import linear_model
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# function that extract if movies was created in US

def count_country(data, country = "United States of America"):
    '''
    goal : count if a given country is in the list of countries
    input: the dataset and the country of interest
    output: the number of times a country is the data
    '''
    total = 0
    for j in data:
        if j is not None:
            total += j.count(country)
    return total

# we will apply the function count_country to divide US movies from non us movies
# a US movie is a movie where US appears once


def extract_us_nonus(data):
    us =  data["Movie_countries"].apply(lambda x: count_country(x))
    us_movies = data.copy()
    us_movies["count_us"] = us

    nonus_movies = us_movies.loc[us_movies["count_us"]==0]
    us_movies = us_movies.loc[us_movies["count_us"]>0]

    return us_movies,nonus_movies

#get the list of genre

def get_all_genre(data):
    genres_unique = []
    for j in data["Movie_genres"]:
        if j is not None:
            for genre in j:
                genres_unique.append(genre)
    genres_unique = np.unique(genres_unique)
    return genres_unique


### plot of barplot for genre change before and after the event 
#function to count the genre
def count_genre(data, genre):
    '''
    function that countes the occurence of a given genre in the data 
    '''
    total = 0
    for j in data["Movie_genres"]:
        if j is not None:
            total += j.count(genre)
    return total

def plot_percentage_movies_genre(data, genre, year_initial, year_end, focus_year,ax, fig):
    '''
    a function that plot the percentage of a given genre as a function of time
        the percentage is defined as the occurence the given genre divided by the total numbe of genres

    input 
        data: the dataset
        genre: the genre that we docus on
        year_initial: the beginning of the period we focus on 
        year_end: the end of the period we focus on
        focus_year: the year the event we study appears
        ax,fig: used later for subplots
    '''

    # count the number of movies that have the given genre per year 
    movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
    movies_year.columns = ["year", "count"]

    # get the total number of genre for a given year, a movies with 5 genres will add 5 to the total count  
    #if we want to divise by the total number of movies, change by sum by count 
    yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')

    #percentage of a given genre
    percentage = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index < year_end)].values*100

    #plot
    ax.plot(movies_year.loc[(movies_year.year > year_initial  )&( movies_year.year < year_end)]["year"], percentage, color ='b')
    ax.plot([focus_year,focus_year],[percentage.min(), percentage.max()], color = 'r' )
    ax.set_title(genre)
    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.set_xticks(np.arange(year_initial, year_end, 1))
    ax.set_xticklabels(ax.get_xticks(), rotation = 45)
    fig.text(0.04, 0.5, 'percentage of movies from given genre per year', ha='center', rotation='vertical')
    ax.grid()

def plot_percentage_movies_genre_all(data, genres, year_initial, year_end, focus_year,nrows,ncols):
    '''
    a function that wraps up the plots for various genres with a subplor with nrows and ncols 
    
    '''
    fig, axs = plt.subplots(nrows = nrows, ncols = ncols, figsize=(15,25))

    for i in range(nrows):
        for j in range(ncols):
            ax = axs[i][j]
            plot_percentage_movies_genre(data, genres[i*ncols+j], year_initial, year_end, focus_year, ax, fig)

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




def get_movies_genre_change(data, genres_unique, nb_genres, year_initial, year_middle, year_end):
    '''
    a function that provides as an output a sorted dataset with a first column genre,
    a second count_before the percentage of occurence of the given genre between year_innitial and year_middle
    a third count_after the percentage of occurence of the given genre between year_middle and year_end
    a last columns with increase/ decrease in the occurence by evaluatinf the difference between the ones before and after divided by the percentage before 

    the function also take as input genres_uniques the list of genres in the dataset
    nb_genres  
            '''
    # total number of genres for movies before and after the specified year range
    before_yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum').reset_index()
    sum_before_yearly_movies = before_yearly_movies.loc[
        (before_yearly_movies.Movie_release_date > year_initial) & 
        (before_yearly_movies.Movie_release_date < year_middle)
    ]["nb_genre"].sum()

    after_yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum').reset_index()
    sum_after_yearly_movies = after_yearly_movies.loc[
        (after_yearly_movies.Movie_release_date >= year_middle) & 
        (after_yearly_movies.Movie_release_date < year_end)
    ]["nb_genre"].sum()

    movies_before = data.loc[
        (data.Movie_release_date.dt.year > year_initial) & 
        (data.Movie_release_date.dt.year < year_middle)
    ]
    movies_after = data.loc[
        (data.Movie_release_date.dt.year >= year_middle) & 
        (data.Movie_release_date.dt.year < year_end)
    ]
        

    genre_count_before = [0 for i in range(len(genres_unique))]
    genre_count_after = [0 for i in range(len(genres_unique))]
    genre_count_diff = [0 for i in range(len(genres_unique))]

    # Calculate the percentage of each genre before and after the
    for i in range(len(genres_unique)):
        sum = 0
        for j in movies_after["Movie_genres"]:
            if j is not None:
                sum += j.count(genres_unique[i])
        genre_count_after[i] = sum / sum_after_yearly_movies * 100

        sum= 0
        for j in movies_before["Movie_genres"]:
            if j is not None:
                sum += j.count(genres_unique[i])
        genre_count_before[i] = sum  / sum_before_yearly_movies * 100
        if genre_count_before[i] != 0:
            genre_count_diff[i] =  (genre_count_after[i] -   genre_count_before[i])/genre_count_before[i]
        else :
                genre_count_diff[i] = 0

            
    df = pd.DataFrame({
        'genre': genres_unique,
        'count_before': genre_count_before,
        'count_after': genre_count_after,
        'count_diff': genre_count_diff
    })
    df["abs_diff"] = df['count_diff'].apply(lambda x: np.abs(x))

    # top genres based on `count_diff`
    df = df.sort_values(by="abs_diff", ascending=False).head(nb_genres)
    genres = df['genre'].values  

    return df

def plot_movies_genre_change(df):
        '''
        a function that plots a barplots for before and after the middleyear 
        '''
        fig, ax = plt.subplots(figsize=(15, 8))
        width = 0.35
        x = np.arange(len(df.genre))  # 

        bars_before = ax.bar(x - width/2, df['count_before'], width, label='Before event', color='blue')
        bars_after = ax.bar(x + width/2, df['count_after'], width, label='After event', color='orange')

        ax.set_xticks(x)
        ax.set_xticklabels(df.genre, rotation=90)  
        ax.set_title("Genre distribution before and after event")
        ax.set_ylabel("Percentage (%)")
        #ax.set_yscale("log")  
        ax.legend()

        plt.tight_layout()
        plt.show()

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
        
def linear_regression_plot(data,year_initial,year_end,focus_year,genre):


    movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
    movies_year.columns = ["year", "count"]

    # get the total number of genre for a given year, a movies with 5 genres will add 5 to the total count  
    #if we want to divise by the total number of movies, change by sum by count 
    yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')

    #percentage of a given genre
    percentage = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index < year_end)].values*100
    percentage_before = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<=focus_year)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index <= focus_year)].values*100
    percentage_after = movies_year.loc[(movies_year.year>=focus_year) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >=focus_year) & (yearly_movies.index < year_end)].values*100

    x_before = percentage_before.index.values.reshape(-1, 1) 
    y_before = percentage_before.values
    reg = linear_model.LinearRegression()
    reg.fit(x_before,y_before)
    y_pred = reg.predict(x_before)

    x_after = percentage_after.index.values.reshape(-1, 1) 
    y_after = percentage_after.values
    reg = linear_model.LinearRegression()
    reg.fit(x_after,y_after)
    y_pred_after = reg.predict(x_after)

    plt.plot(movies_year.loc[(movies_year.year > year_initial  )&( movies_year.year <= focus_year)]["year"], y_pred,linestyle='dashed',color = "blue", alpha = 0.7)
    plt.plot(movies_year.loc[(movies_year.year >= focus_year  )&( movies_year.year < year_end)]["year"], y_pred_after,linestyle='dashed',color = "blue", alpha = 0.7)

    plt.plot(movies_year.loc[(movies_year.year > year_initial  )&( movies_year.year < year_end)]["year"], percentage, color ='b')
    plt.plot([focus_year,focus_year],[percentage.min(), percentage.max()], color = 'r' )
    plt.title(genre)
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.xticks(np.arange(year_initial, year_end + 1, 1), rotation=45) 
    plt.grid()
