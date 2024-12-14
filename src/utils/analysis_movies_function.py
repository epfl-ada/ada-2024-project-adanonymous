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


    

### function that extract if movies was created in US

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

###get the list of genre

def get_all_genre(data):
    genres_unique = []
    for j in data["Movie_genres"]:
        if j is not None:
            for genre in j:
                genres_unique.append(genre)
    genres_unique = np.unique(genres_unique)
    return genres_unique



###function to count the genre

def count_genre(data, genre):
    '''
    function that countes the occurence of a given genre in the data 
    '''
    total = 0
    for j in data["Movie_genres"]:
        if j is not None:
            total += j.count(genre)
    return total

### plot time serie of a gerne evolution

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


### function that gives the genre that changed the most between two periods 

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


### plot of barplot for genre change before and after the event 

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

            
### a function that give the percentage of a genre between 2 time frame for each continent

def get_country_dataset(all_data,year_initial,year_end,focus_year,genre):
    '''
    input : 3 dataset one foor each continent (Europe, North America Asia)
            time period of the stidy (initial, middle end)
            genre to focus on
    output: a data frame with 3 columns giving the percentage of the genre for each continent
    '''
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

### associate a coutry to a continent and split the dataframe accordingly

def continent_data(movies):

    first_movies = movies.FirstCountry_Name.dropna().unique()
    second_movies = movies.SecondCountry_Name.dropna().unique()

    list_movies = np.concatenate((first_movies, second_movies))
    unique_countries = np.unique(list_movies) 

    #uploead the contry continent correspondence
    continents = pd.read_csv('continents.csv', sep =';')

    # set new column for continents
    movies['FirstContinent_name']= movies.FirstCountry_Name.apply(lambda x : continents.loc[continents.Entity == x, 'World regions according to OWID'].values[0])
    movies['SecondContinent_name']= movies.SecondCountry_Name.apply(lambda x : continents.loc[continents.Entity == x, 'World regions according to OWID'].values[0] if x is not None else None)

    # extract the continents
    Europe = movies.loc[(movies['FirstContinent_name'] == 'Europe') |(movies['SecondContinent_name'] == 'Europe')]
    Africa = movies.loc[(movies['FirstContinent_name'] == 'Africa') |(movies['SecondContinent_name'] == 'Africa')]
    Asia = movies.loc[(movies['FirstContinent_name'] == 'Asia') |(movies['SecondContinent_name'] == 'Asia')]
    Australia = movies.loc[(movies['FirstContinent_name'] == 'Oceania') |(movies['SecondContinent_name'] == 'Oceania')]
    South_America =  movies.loc[(movies['FirstContinent_name'] == 'South America') |(movies['SecondContinent_name'] == 'South America')]
    North_America =  movies.loc[(movies['FirstContinent_name'] == 'North America') |(movies['SecondContinent_name'] == 'North America')]

    #keep the one we focus on 
    world_data = [North_America, Europe, Asia]
    world = ['North_America', 'Europe', 'Asia']

    return world_data


 ### interactive plot per continent

def plot_per_continent(movies, initial_year, final_year, middle_year, genre):
    '''
    function that plot for each continent the evolution of the given genre a possible change of continent is made with a button
    input: focus period, dataset, genre
    output : interactive plot of percentage evolution
    '''
    # get per continent movies
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


### static plot per continent
def plot_continent(movies, initial_year, final_year, middle_year, genre):
    '''
    Function that plots for each continent the evolution of the given genre 
    Input: focus period, dataset, genre
    Output: Static plot of percentage evolution
    '''
    #get data
    world_data = continent_data(movies)
    df = get_country_dataset(world_data, initial_year, final_year, middle_year, genre)
 
    plt.figure(figsize=(10, 6))

    plt.plot(df['Year'], df['Asia'], label='Asia', color='#33CFA5', linewidth=2)
    plt.plot(df['Year'], df['North_America'], label='North America', color='#3b33cf', linewidth=2)
    plt.plot(df['Year'], df['Europe'], label='Europe', color='#F06A6A', linewidth=2)

    
    plt.axvline(x=middle_year, color='black', linestyle='--', linewidth=1.5, label=f'Year ({middle_year})')

    plt.xticks(df['Year'], rotation = 'vertical')
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Percentage evolution of {genre} in different continents')
    plt.legend(loc='best')
    plt.grid(True, linestyle='--') 

    plt.show()

### interactive world map plot

def create_world_map(movies, initial_year, final_year, middle_year, genres):
    '''
    Function that creates an interactive world map with genre percentage evolution for various genres
    '''
    app = Dash(__name__)
    
    world_data = continent_data(movies)
    continent_data_df = []

    # to have a button for the gentes we want to focus on 
    for genre in genres:
        genre_data_df = get_country_dataset(world_data, initial_year, final_year, middle_year, genre)
        genre_data_df['Genre'] = genre
        continent_data_df.append(genre_data_df)
    df = pd.concat(continent_data_df, ignore_index=True)
    
    df2 = pd.melt(df, id_vars=['Year', 'Genre'], value_vars=['North_America', 'Europe', 'Asia'],
                        var_name='Continent', value_name='Value')
    
    #where the values will be plot on the map
    continent_to_countries = {
        "North_America": ["CAN", "MEX", "USA", "BLZ", "CRI", "DMA", "GRD", "GTM", "HND", "JAM", 
                            "KNA", "LCA", "VCT", "TTO", "BHS", "CUB", "BVI", "MSR", "SPM", "PRI"],
        "Europe": ["ALB", "AND", "AUT", "BLR", "BEL", "BIH", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", 
                    "DEU", "GRC", "HUN", "ISL", "IRL", "ITA", "LVA", "LIE", "LTU", "LUX", "MLT", "MDA", "MCO", "MNE", 
                    "NLD", "MKD", "NOR", "POL", "PRT", "ROU", "RUS", "SMR", "SRB", "SVK", "SVN", "ESP", "SWE", "CHE", 
                    "TUR", "UKR", "GBR", "VAT"],
        "Asia": ["AFG", "ARM", "AZE", "BGD", "BRN", "BTN", "KHM", "CHN", "CYP", "GEO", "IND", "IDN", "IRN", "IRQ", 
                    "ISR", "JPN", "JOR", "KAZ", "KOR", "KWT", "KGZ", "LAO", "LBN", "MAC", "MYS", "NPL", "PAK", "PHL", 
                    "QAT", "SAU", "SGP", "LKA", "SYR", "TWN", "TJK", "THA", "TUR", "TKM", "ARE", "UZB", "VNM", "YEM"]
    }
    
    expanded_rows = []
    for _, row in df2.iterrows():
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



## get the percentage of a genre 

def percentage_movies_genre(data, europe, genre, year_initial, year_end, focus_year):

    movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
    movies_year.columns = ["year", "count"]


    yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')
    europe_movies = europe.groupby(europe.Movie_release_date.dt.year)['nb_genre'].agg('sum')

    percentage = movies_year.loc[(movies_year.year>year_initial) & (movies_year.year<year_end)]["count"]/europe_movies[(europe_movies.index >year_initial) & (europe_movies.index < year_end)].values*100

    return percentage

# plot the propaganda movies percentage for Germany vs the rest of Europe

def get_propaganda_movies(movies, initial_year, final_year, middle_year, genre):

    ## 'Nazi Germany', 'Germany'
    
    world_data = continent_data(movies)
    data = world_data[1]
    europe = data.loc[(data.Movie_release_date.dt.year>1930) & (data.Movie_release_date.dt.year<=1950)]

    # get all german movies and rest of Europe
    german =  europe["Movie_countries"].apply(lambda x: count_country(['Germany' if item == 'Nazi Germany' else item for item in x], country = 'Germany'))

    german_movies = europe.copy()
    german_movies["count_us"] = german

    nongerman_movies = german_movies.loc[german_movies["count_us"]==0]
    german_movies = german_movies.loc[german_movies["count_us"]>0]


    percentage_german = percentage_movies_genre(german_movies, europe,'Propaganda film', 1930, 1950,1940)
    percentage_nongerman = percentage_movies_genre(nongerman_movies, europe,'Propaganda film', 1930, 1950,1940)

    plt.plot(np.arange(1931,1950,1),percentage_german, label = 'German', color = 'b')
    plt.plot(np.arange(1931,1950,1),percentage_nongerman, label = 'non German', color = 'green')
    plt.xticks(np.arange(1931,1950,1), rotation = 'vertical')
    plt.legend()
    plt.grid()


    
    
def process_data(data, genre, year_initial, year_end, focus_year):
    
    movies_year = data.groupby(data.Movie_release_date.dt.year).apply(lambda x: count_genre(x, genre)).reset_index()
    movies_year.columns = ["year", "count"]
    
    yearly_movies = data.groupby(data.Movie_release_date.dt.year)['nb_genre'].agg('sum')
    
    percentage = movies_year.loc[(movies_year.year > year_initial) & (movies_year.year < year_end)]["count"] / yearly_movies[(yearly_movies.index > year_initial) & (yearly_movies.index < year_end)].values * 100
    percentage_before = movies_year.loc[(movies_year.year > year_initial) & (movies_year.year <= focus_year)]["count"] / yearly_movies[(yearly_movies.index > year_initial) & (yearly_movies.index <= focus_year)].values * 100
    percentage_after = movies_year.loc[(movies_year.year >= focus_year) & (movies_year.year < year_end)]["count"] / yearly_movies[(yearly_movies.index >= focus_year) & (yearly_movies.index < year_end)].values * 100
    
    x_before = percentage_before.index.values.reshape(-1, 1) 
    y_before = percentage_before.values
    reg_before = linear_model.LinearRegression()
    reg_before.fit(x_before, y_before)
    y_pred_before = reg_before.predict(x_before)
    
    x_after = percentage_after.index.values.reshape(-1, 1) 
    y_after = percentage_after.values
    reg_after = linear_model.LinearRegression()
    reg_after.fit(x_after, y_after)
    y_pred_after = reg_after.predict(x_after)
    
    return movies_year, percentage, percentage_before, percentage_after, y_pred_before, y_pred_after
    
    
def linear_regression_plot(data1, data2, year_initial, year_end, focus_year, genre):
    
    movies_year1, percentage1, percentage_before1, percentage_after1, y_pred_before1, y_pred_after1 = process_data(data1, genre, year_initial, year_end, focus_year)
    movies_year2, percentage2, percentage_before2, percentage_after2, y_pred_before2, y_pred_after2 = process_data(data2, genre, year_initial, year_end, focus_year)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the percentage of movies for US
    ax.plot( movies_year1.loc[(movies_year1.year > year_initial) & (movies_year1.year < year_end)]["year"], 
        percentage1,  marker='o', linestyle='-', color='blue', label='US')
    
    # Plot the percentage of movies for Non-US
    ax.plot(movies_year2.loc[(movies_year2.year > year_initial) & (movies_year2.year < year_end)]["year"], 
        percentage2, marker='o', linestyle='-', color='green', label='Non US')
    
    # Plot the trend before focus year for US
    ax.plot(movies_year1.loc[(movies_year1.year > year_initial) & (movies_year1.year <= focus_year)]["year"], 
        y_pred_before1, linestyle='--',  color='blue',  linewidth=2, alpha=0.7, label='Trend before - US')
    
    # Plot the trend before focus year for Non-US
    ax.plot( movies_year2.loc[(movies_year2.year > year_initial) & (movies_year2.year <= focus_year)]["year"], 
        y_pred_before2, linestyle='--', color='green', linewidth=2, alpha=0.7, label='Trend before - Non US')
    
    # Plot the trend after focus year for US
    ax.plot(movies_year1.loc[(movies_year1.year >= focus_year) & (movies_year1.year < year_end)]["year"], 
        y_pred_after1, linestyle='--', color='blue', linewidth=2, alpha=0.7, label='Trend after - US')
    
    # Plot the trend after focus year for Non-US
    ax.plot(movies_year2.loc[(movies_year2.year >= focus_year) & (movies_year2.year < year_end)]["year"], 
        y_pred_after2, linestyle='--', color='green', linewidth=2, alpha=0.7, label='Trend after - Non US')
    
    # Draw the vertical line at the focus year
    ax.axvline(x=focus_year, color='red', linestyle='--', linewidth=2)
    
    # Add title and labels
    ax.set_title(f'{genre}', fontsize=16)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Percentage (%)', fontsize=14)
    
    # Customize ticks and grid
    ax.set_xticks(np.arange(year_initial, year_end + 1, 1))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Add legend
    ax.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.show()
