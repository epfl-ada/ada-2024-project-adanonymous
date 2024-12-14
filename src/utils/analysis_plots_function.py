import matplotlib.pyplot as plt
import pandas as pd 
import math
import plotly.graph_objects as go


def count_key_words(movies_and_plots_df, key_words):
    """
    Count the given key words in the plot summaries and outputs a dataframe with the counts by year of release of the movies

    Args:
        movies_and_plots_df (Dataframe): The merge of the movies dataset and the plot_summaries dataset
        key_words (List[str]): The list of key words

    Returns:
        df_key_words_occ (Dataframe): A dataframe with the information
    """
    
    df_plots = movies_and_plots_df[['Wikipedia_movie_ID', 'Freebase_movie_ID', 'Movie_name', 'Movie_release_date', 'Plot']]
    col_name_of_key_words = ['Count_of_' + '_'.join(word.split(' ')) for word in key_words]
    pd.options.mode.chained_assignment = None  # default='warn'
    
    # Count the number of occurences of key words in plot summary for each movie 
    for i in range(len(key_words)):
        df_plots[col_name_of_key_words[i]] = df_plots['Plot'].apply(lambda x: x.count(key_words[i]))

    pd.options.mode.chained_assignment = 'warn'

    df_key_words_occ = df_plots.groupby(by=df_plots['Movie_release_date'].dt.year)[col_name_of_key_words].sum()

    df_key_words_occ = df_plots.groupby(by=df_plots['Movie_release_date'].dt.year)[col_name_of_key_words].sum()
    df_key_words_occ['Count_movies'] = movies_and_plots_df.groupby(by=movies_and_plots_df['Movie_release_date'].dt.year)['Wikipedia_movie_ID'].count()

    return df_key_words_occ


def plot_key_words_occ(key_words_occ_df, key_words):
    """
    Plots the occurences of the key words by year of release of the movies

    Args:
        key_words_occ_df (Dataframe): The dataframe of the key words occurences by year of release
        key_words (List[str]): The list of key words
    """
    col_name_of_key_words = ['Count_of_' + '_'.join(word.split(' ')) for word in key_words]
    n_key_words = len(key_words)

    fig, ax = plt.subplots(math.ceil(n_key_words/2), 2, figsize= (math.ceil(n_key_words/2)*6, 8), sharey = True, sharex = True)

    for i in range(n_key_words):
        sbplt = ax[i%math.ceil(n_key_words/2), math.floor(i/math.ceil(n_key_words/2))]
        col_name = col_name_of_key_words[i]

        sbplt.plot(key_words_occ_df[col_name])
        sbplt.set_title('Occurence of "' + key_words[i] + '" in plot summaries')
        
    if (n_key_words % 2 != 0):
        fig.delaxes(ax[math.floor(n_key_words/2), 1])

    fig.tight_layout()

    fig.text(0.48,0, "Year of release")
    fig.text(0,0.38, "Number of occurences of the word", rotation = 90)
    

    
def plot_key_words_occ_zoomed(key_words_occ_df, key_words):
    """
    Plots the occurences of the key words by year of release of the movies from 1992 to 2013. Adds a grid for convenience

    Args:
        key_words_occ_df (Dataframe): The dataframe of the key words occurences by year of release
        key_words (List[str]): The list of key words
    """

    df_key_words_occ_reset = key_words_occ_df.reset_index()
    key_words_occ_df_zoomed = df_key_words_occ_reset[((1992 <= df_key_words_occ_reset['Movie_release_date']) * (df_key_words_occ_reset['Movie_release_date'] <= 2013)) == 1]
    key_words_occ_df_zoomed = key_words_occ_df_zoomed.set_index(keys='Movie_release_date')

    col_name_of_key_words = ['Count_of_' + '_'.join(word.split(' ')) for word in key_words]
    n_key_words = len(key_words)

    fig, ax = plt.subplots(math.ceil(n_key_words/2), 2, figsize= (math.ceil(n_key_words/2)*6, 8), sharey = True, sharex = True)

    for i in range(n_key_words):
        sbplt = ax[i%math.ceil(n_key_words/2), math.floor(i/math.ceil(n_key_words/2))]
        col_name = col_name_of_key_words[i]

        sbplt.plot(key_words_occ_df_zoomed[col_name])
        sbplt.set_title('Occurence of "' + key_words[i] + '" in plot summaries')
        sbplt.grid()

        sbplt.tick_params(axis='both', which='major', labelsize=7)
        sbplt.set_xticks([int(ind) for ind in key_words_occ_df_zoomed.index])
        sbplt.set_xticklabels(sbplt.get_xticks(), rotation = 45)
        
    if (n_key_words % 2 != 0):
        fig.delaxes(ax[math.floor(n_key_words/2), 1])

    fig.tight_layout()

    fig.text(0.48,0, "Year of release")
    fig.text(0,0.38, "Number of occurences of the word", rotation = 90)



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

    
def percentage_key_words_before_after(key_words_occ_df):
    """
    Calculates the percentage of the key words occurence before 2002 (incl.) and after 2003 (incl.) separately.

    Args:
        key_words_occ_df (Dataframe): The dataframe of the key words occurences by year of release
    """

    df_key_words_occ_i = key_words_occ_df.reset_index()
    df_key_words_occ_before = df_key_words_occ_i[(1992 <= df_key_words_occ_i['Movie_release_date']) * (df_key_words_occ_i['Movie_release_date'] < 2003) == 1]
    df_key_words_occ_after = df_key_words_occ_i[(2003 <= df_key_words_occ_i['Movie_release_date'])  * (df_key_words_occ_i['Movie_release_date'] <= 2013) == 1]

    df_key_words_occ_comp = pd.DataFrame(data={
        '1992-2002': df_key_words_occ_before.sum() / df_key_words_occ_before['Count_movies'].sum(),
        '2003-2013': df_key_words_occ_after.sum() / df_key_words_occ_after['Count_movies'].sum()
        })

    df_key_words_occ_before_after = df_key_words_occ_comp.drop(['Movie_release_date', 'Count_movies']).map(lambda x: str(round(x*100, 3)) + '%')
    
    return df_key_words_occ_before_after