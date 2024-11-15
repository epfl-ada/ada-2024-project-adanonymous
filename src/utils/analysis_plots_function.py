
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import math

def count_key_words(movies_and_plots_df, key_words):
    # Count the number of occurences of key words in plot summary for each movie 
    df_plots = movies_and_plots_df[['Wikipedia_movie_ID', 'Freebase_movie_ID', 'Movie_name', 'Movie_release_date', 'Plot']]
    col_name_of_key_words = ['Count_of_' + '_'.join(word.split(' ')) for word in key_words]
    pd.options.mode.chained_assignment = None  # default='warn'

    for i in range(len(key_words)):
        df_plots[col_name_of_key_words[i]] = df_plots['Plot'].apply(lambda x: x.count(key_words[i]))

    pd.options.mode.chained_assignment = 'warn'

    df_key_words_occ = df_plots.groupby(by=df_plots['Movie_release_date'].dt.year)[col_name_of_key_words].sum()

    df_key_words_occ = df_plots.groupby(by=df_plots['Movie_release_date'].dt.year)[col_name_of_key_words].sum()
    df_key_words_occ['Count_movies'] = movies_and_plots_df.groupby(by=movies_and_plots_df['Movie_release_date'].dt.year)['Wikipedia_movie_ID'].count()

    return df_key_words_occ


def plot_key_words_occ(key_words_occ_df, key_words):
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


def percentage_key_words_before_after(key_words_occ_df):
    df_key_words_occ_i = key_words_occ_df.reset_index()
    df_key_words_occ_before = df_key_words_occ_i[(1992 <= df_key_words_occ_i['Movie_release_date']) * (df_key_words_occ_i['Movie_release_date'] < 2003) == 1]
    df_key_words_occ_after = df_key_words_occ_i[(2003 <= df_key_words_occ_i['Movie_release_date'])  * (df_key_words_occ_i['Movie_release_date'] <= 2013) == 1]

    df_key_words_occ_comp = pd.DataFrame(data={
        '1992-2002': df_key_words_occ_before.sum() / df_key_words_occ_before['Count_movies'].sum(),
        '2003-2013': df_key_words_occ_after.sum() / df_key_words_occ_after['Count_movies'].sum()
        })

    df_key_words_occ_before_after = df_key_words_occ_comp.drop(['Movie_release_date', 'Count_movies']).map(lambda x: str(round(x*100, 3)) + '%')
    
    return df_key_words_occ_before_after