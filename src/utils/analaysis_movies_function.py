import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn import linear_model
import plotly.graph_objects as go
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

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
    genre = genre  

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





def get_country_dataset(all_data,year_initial,year_end,focus_year,genre):
    data_percentage = []
    for i in range(3):
        data = all_data[i]
        movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
        movies_year.columns = ["year", "count"]

        # get the total number of genre for a given year, a movies with 5 genres will add 5 to the total count  
        #if we want to divise by the total number of movies, change by sum by count 
        yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')

        #percentage of a given genre
        percentage = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index < year_end)].values*100
        percentage_before = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<=focus_year)]["count"]/yearly_movies[(yearly_movies.index >year_initial) & (yearly_movies.index <= focus_year)].values*100
        percentage_after = movies_year.loc[(movies_year.year>=focus_year) & (movies_year.year<year_end)]["count"]/yearly_movies[(yearly_movies.index >=focus_year) & (yearly_movies.index < year_end)].values*100

        data_percentage.append(percentage.values)
        
    data_percentage.append(movies_year.loc[(movies_year.year > year_initial  )&( movies_year.year < year_end)]["year"].values)
    

    df = pd.DataFrame(np.array(data_percentage).T, columns = ['North_America', 'Europe', 'Asia', 'Year'])
    return df

    
def continent_data(movies):
    first_movies = movies.FirstCountry_Name.dropna().unique()
    second_movies = movies.SecondCountry_Name.dropna().unique()
    list_movies = np.concatenate((first_movies, second_movies))
    unique_countries = np.unique(list_movies) 


    continents = pd.read_csv('continents.csv', sep =';')

    movies['FirstContinent_name']= movies.FirstCountry_Name.apply(lambda x : continents.loc[continents.Entity == x, 'World regions according to OWID'].values[0])
    movies['SecondContinent_name']= movies.SecondCountry_Name.apply(lambda x : continents.loc[continents.Entity == x, 'World regions according to OWID'].values[0] if x is not None else None)

    Europe = movies.loc[(movies['FirstContinent_name'] == 'Europe') |(movies['SecondContinent_name'] == 'Europe')]
    Africa = movies.loc[(movies['FirstContinent_name'] == 'Africa') |(movies['SecondContinent_name'] == 'Africa')]
    Asia = movies.loc[(movies['FirstContinent_name'] == 'Asia') |(movies['SecondContinent_name'] == 'Asia')]
    Australia = movies.loc[(movies['FirstContinent_name'] == 'Oceania') |(movies['SecondContinent_name'] == 'Oceania')]
    South_America =  movies.loc[(movies['FirstContinent_name'] == 'South America') |(movies['SecondContinent_name'] == 'South America')]
    North_America =  movies.loc[(movies['FirstContinent_name'] == 'North America') |(movies['SecondContinent_name'] == 'North America')]

    world_data = [North_America, Europe, Asia]
    world = ['North_America', 'Europe', 'Asia']

    return world_data

    
def plot_per_continent(movies, initial_year, final_year, middle_year, genre):
    '''
    function that plot for each continent the evolution of the given genre 

    a possible change of continent is made with a button

    input: focus period - dataset -genre
    output : interactive plot of percentage evolution
    '''
    # get per continent data
    world_data = continent_data(movies)
    df = get_country_dataset(world_data, initial_year, final_year, middle_year, genre)

    fig = go.Figure()

    #  max and min per continent
    max_asia = df['Asia'].max()
    max_north_america = df['North_America'].max()
    max_europe = df['Europe'].max()

    min_asia = df['Asia'].min()
    min_north_america = df['North_America'].min()
    min_europe = df['Europe'].min()

    # plot
    fig.add_trace(
        go.Scatter(x=list(df.Year),
                   y=list(df.Asia),
                   name="Asia",
                   visible=True,  # Make Asia visible initially
                   line=dict(color="#33CFA5")))

    fig.add_trace(
        go.Scatter(x=list(df.Year),
                   y=list(df.North_America),
                   name="North_America",
                   visible=False,
                   line=dict(color="#3b33cf")))

    fig.add_trace(
        go.Scatter(x=list(df.Year),
                   y=list(df.Europe),
                   name="Europe",
                   visible=False,
                   line=dict(color="#F06A6A")))

    # Add vertical lines for 2001
    asia_line = dict(type="line",
                     x0=middle_year, x1=middle_year,
                     y0=min_asia, y1=max_asia,
                     xref="x", yref="y",
                     line=dict(color="#33CFA5", dash="dot"))

    north_america_line = dict(type="line",
                              x0=middle_year, x1=middle_year,
                              y0=min_north_america, y1=max_north_america,
                              xref="x", yref="y",
                              line=dict(color="#3b33cf", dash="dot"))

    europe_line = dict(type="line",
                       x0=middle_year, x1=middle_year,
                       y0=min_europe, y1=max_europe,
                       xref="x", yref="y",
                       line=dict(color="#F06A6A", dash="dot"))


    fig.update_layout(
        shapes=[asia_line],  # Initially show only Asia's line
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Asia",
                         method="update",
                         args=[{"visible": [True, False, False]},
                               {"title": "Asia",
                                "shapes": [asia_line]}]),
                    dict(label="Europe",
                         method="update",
                         args=[{"visible": [False, False, True]},
                               {"title": "Europe",
                                "shapes": [europe_line]}]),
                    dict(label="North_America",
                         method="update",
                         args=[{"visible": [False, True, False]},
                               {"title": "North America",
                                "shapes": [north_america_line]}]),
                    dict(label="All",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "All",
                                "shapes": [asia_line, europe_line, north_america_line]}]),
                ]),
            )
        ])

    fig.update_layout(title_text=genre)

    fig.show()



   
def create_world_map(movies, initial_year, final_year, middle_year, genres) :
    '''
    Function that create and interactive world map with genre percentage evolution for various genres

    '''
    app = Dash(__name__)
    
    
    world_data = continent_data(movies)
    
    continent_data_df = []

    # get an array with the selected genres and the continents
    
    for genre in genres:
        genre_data_df = get_country_dataset(world_data, initial_year, final_year, middle_year,genre)
        genre_data_df['Genre'] = genre
        continent_data_df.append(genre_data_df)
    df = pd.concat(continent_data_df, ignore_index=True)
    

    # transform the array shape
    long_df = pd.melt(df, id_vars=['Year', 'Genre'], value_vars=['North_America', 'Europe', 'Asia'],
                      var_name='Continent', value_name='Value')
    
    
    #world plot localization 

    continent_to_countries = {
        "North_America": ["CAN", "MEX", "USA", "BLZ", "CRI", "DMA", "GRD", "GTM", "HND", "JAM", 
        "KNA", "LCA", "VCT", "TTO", "BHS", "CUB", "BVI", "MSR", "SPM", "PRI"],
        "Europe": ["ALB", "AND", "AUT", "BLR", "BEL", "BIH", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", 
        "DEU", "GRC", "HUN", "ISL", "IRL", "ITA", "LVA", "LIE", "LTU", "LUX", "MLT", "MDA", "MCO", "MNE", "NLD", 
        "MKD", "NOR", "POL", "PRT", "ROU", "RUS", "SMR", "SRB", "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "UKR", "GBR", "VAT"],
        "Asia": ["AFG", "ARM", "AZE", "BGD", "BRN", "BTN", "KHM", "CHN", "CYP", "GEO", "IND", "IDN", "IRN", "IRQ", 
        "ISR", "JPN", "JOR", "KAZ", "KOR", "KWT", "KGZ", "LAO", "LBN", "MAC", "MYS", "NPL", "PAK", "PHL", "QAT", 
        "SAU", "SGP", "LKA", "SYR", "TWN", "TJK", "THA", "TUR", "TKM", "ARE", "UZB", "VNM", "YEM"]
    }
    
    expanded_rows = []
    for _, row in long_df.iterrows():
        continent = row["Continent"]
        if continent in continent_to_countries:
            for country in continent_to_countries[continent]:
                expanded_rows.append({
                    "Year": row["Year"],
                    "Genre": row["Genre"],
                    "Continent": row["Continent"],
                    "Value": row["Value"],
                    "iso_alpha": country
                })
    
    expanded_df = pd.DataFrame(expanded_rows)
    
    #interactive app
    app.layout = html.Div([
        html.H4('Political Candidate Voting Pool Analysis'),
        html.P("Select a Genre:"),
        dcc.RadioItems(
            id='genre', 
            options=[{'label': genre, 'value': genre} for genre in genres],
            value="War film",
            inline=True
        ),
        dcc.Graph(id="graph"),
    ])
    
    
    @app.callback(
        Output("graph", "figure"),
        Input("genre", "value")
    )
    def display_choropleth(genre):
    
        filtered_df = expanded_df[expanded_df['Genre'] == genre]
        
    
        fig = px.choropleth(
            filtered_df,
            locations="iso_alpha",
            color="Value",
            hover_name="Continent",
            animation_frame="Year",
            projection="natural earth",
            range_color=[filtered_df.Value.min(), filtered_df.Value.max()],
            title=f"Percentage of genre {genre} by continent"
        )
        
        return fig
    
    
    
    app.run_server(debug=True)


    
