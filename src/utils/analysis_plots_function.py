import matplotlib.pyplot as plt
import pandas as pd 
import math
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from itertools import chain

def expected_number_before_after(df_plots, mid_value, without_n_most_common=None):
    df_plots_after = df_plots[df_plots['Movie_release_date'].dt.year > mid_value]
    df_plots_before = df_plots[df_plots['Movie_release_date'].dt.year <= mid_value]

    plots_before = df_plots_before['Plot'].apply(lambda x: x.lower().strip("',.{[}]!?|").split()).to_list()
    plots_after = df_plots_after['Plot'].apply(lambda x: x.lower().strip("',.{[}]!?|").split()).to_list()

    text_before = list(chain.from_iterable(plots_before))
    text_after = list(chain.from_iterable(plots_after))
    
    counter_all = Counter(text_before)
    counter_all.update(text_after)
    
    counter_before = Counter(text_before)
    counter_after = Counter(text_after)

    dict_all, dict_before, dict_after = dict(counter_all), dict(counter_before), dict(counter_after)

    for k, v in dict_all.items():
        dict_all[k] = v / len(df_plots)

    for k, v in dict_before.items():
        dict_before[k] = v / len(df_plots_before)

    for k, v in dict_after.items():
        dict_after[k] = v / len(df_plots_after)

    for key in dict_all.keys():
        if key not in dict_before:
            dict_before[key] = 0
        if key not in dict_after:
            dict_after[key] = 0
    
    if without_n_most_common is not None:
        for word, count in counter_all.most_common(without_n_most_common):
            dict_all.pop(word)
            dict_before.pop(word)
            dict_after.pop(word)

    dict_all = dict(sorted(dict_all.items()))
    dict_before = dict(sorted(dict_before.items()))
    dict_after = dict(sorted(dict_after.items()))

    return counter_all, dict_all, counter_before, dict_before, counter_after, dict_after


def ratios_before_after(dict_before, dict_after, min_expectation=1e-2):
    sorted_tuples = []

    for key, val_bef, val_aft in zip(dict_before.keys(), dict_before.values(), dict_after.values()):
        if val_bef < min_expectation or val_aft < min_expectation:
            ratio = 1
        else:
            ratio = val_aft / val_bef

        sorted_tuples.append((key, ratio))

    sorted_tuples = sorted(sorted_tuples, key=lambda item: item[1], reverse=True)

    sorted_words = [el[0] for el in sorted_tuples]
    sorted_ratios = [el[1] for el in sorted_tuples]

    return sorted_words, sorted_ratios


def plot_first_n(sorted_words, sorted_ratios, n):
    fig = px.bar(x=sorted_words[:n], y=sorted_ratios[:n], labels={'x':'word', 'y':'ratio'}, title=f'Plot of the first {n} biggest ratios before to after')
    return fig


def get_model_parameters(figure):
    model = px.get_trendline_results(figure)
    b = model.iloc[0]["px_fit_results"].params[0]
    m = model.iloc[0]["px_fit_results"].params[1]
    return model, m, b


def plot_regression(dict_before, dict_after):
    fig = px.scatter(x=dict_before.values(), y=dict_after.values(), labels={'x':'Expected number of word before event', 'y':'Expected number of word after event', 'hover_data_0':'word'}, hover_data=[dict_before.keys()], trendline='ols', trendline_color_override = 'red')
    model, m, b = get_model_parameters(fig)
    print(f'm = {m}, b = {b}')
    fig.update_layout(title='Regression plot of expected number of words before and after 9/11')

    return fig, model


def get_furthest_n(model, dict_before, dict_after, n):
    b = model.iloc[0]["px_fit_results"].params[0]
    m = model.iloc[0]["px_fit_results"].params[1]

    word_and_dist = []
    for word in dict_before.keys():
        dist = abs(dict_after[word] - m*dict_before[word] - b)
        word_and_dist.append((word, dist))

    sorted_word_and_dist = sorted(word_and_dist, key=lambda item: item[1], reverse=True)
    
    return sorted_word_and_dist[:n]


def plot_furthest_n(model, dict_before, dict_after, n):
    sorted_word_and_dist = get_furthest_n(model, dict_before, dict_after, n)
    words = []
    dists = []
    for word, dist in sorted_word_and_dist:
        words.append(word)
        dists.append(dist)

    fig = px.bar(x=words, y=dists, labels={'x':'Word', 'y':'L2 distance'}, title='Plot of furthest words from the regression line')
    return fig


def flag_plot_movie(df, key_words):
    pd.options.mode.chained_assignment = None
    col_name_of_key_words = [word.lower() for word in key_words]

    def flag_count(plot_summary, key_word):
        return 1 if plot_summary.lower().count(key_word) > 0 else 0

    for i in range(len(key_words)):
        col_name = col_name_of_key_words[i][0].upper() + col_name_of_key_words[i][1:]
        df[col_name] = df['Plot'].apply(lambda x: flag_count(x, key_word=col_name_of_key_words[i]))

    pd.options.mode.chained_assignment = 'warn'
    return df


def occ_by_year(df, key_words):
    col_name_of_key_words = [word[0].upper() + word[1:] for word in key_words]
    df_key_words_occ = df.groupby(by=df['Movie_release_date'].dt.year)[col_name_of_key_words].sum()
    df_key_words_occ['Movies'] = df.groupby(by=df['Movie_release_date'].dt.year)['Wikipedia_movie_ID'].count()

    return df_key_words_occ.copy(deep=True)


def plot_occ_by_year(df, key_words):
    col_name_of_key_words = [word[0].upper() + word[1:] for word in key_words]
    fig, ax = plt.subplots(math.ceil(len(key_words)/2), 2, figsize= (math.ceil(len(key_words)/2)*6, 8), sharey = True, sharex = True, squeeze=False)

    for i in range(len(key_words)):
        sbplt = ax[i%math.ceil(len(key_words)/2), math.floor(i/math.ceil(len(key_words)/2))]
        col_name = col_name_of_key_words[i]

        sbplt.plot(df[col_name])
        sbplt.set_title(f'{col_name_of_key_words[i]}')
        
    if (len(key_words) % 2 != 0):
        fig.delaxes(ax[math.floor(len(key_words)/2), 1])

    fig.tight_layout()

    fig.text(0.48,0, "Year of release")
    fig.text(0,0.40, "Number of movie plots", rotation = 90)
    fig.suptitle("Number of movie plots with a certain key word", fontsize=10)


def plot_key_words_occ_zoomed(df, key_words, mid_value, horizon_years=10):
    """
    Plots the occurences of the key words by year of release of the movies from 1992 to 2013. Adds a grid for convenience

    Args:
        df (Dataframe): The dataframe of the key words occurences by year of release
        key_words (List[str]): The list of key words
    """
    before_horizon = mid_value - horizon_years
    after_horizon = mid_value + horizon_years

    df_key_words_occ_reset = df.reset_index()
    key_words_occ_df_zoomed = df_key_words_occ_reset[((before_horizon <= df_key_words_occ_reset['Movie_release_date']) * (df_key_words_occ_reset['Movie_release_date'] < after_horizon)) == 1]
    key_words_occ_df_zoomed = key_words_occ_df_zoomed.set_index(keys='Movie_release_date')

    col_name_of_key_words = [word[0].upper() + word[1:] for word in key_words]
    n_key_words = len(key_words)

    fig, ax = plt.subplots(math.ceil(n_key_words/2), 2, figsize= (math.ceil(n_key_words/2)*6, 8), sharey = True, sharex = True)

    for i in range(n_key_words):
        sbplt = ax[i%math.ceil(n_key_words/2), math.floor(i/math.ceil(n_key_words/2))]
        col_name = col_name_of_key_words[i]

        sbplt.plot(key_words_occ_df_zoomed[col_name])
        sbplt.set_title(f'{col_name_of_key_words[i]}')
        sbplt.grid()

        sbplt.tick_params(axis='both', which='major', labelsize=7)
        sbplt.set_xticks([int(ind) for ind in key_words_occ_df_zoomed.index])
        sbplt.set_xticklabels(sbplt.get_xticks(), rotation = 45)
        
    if (n_key_words % 2 != 0):
        fig.delaxes(ax[math.floor(n_key_words/2), 1])

    fig.tight_layout()

    fig.text(0.48,0, "Year of release")
    fig.text(0,0.38, "Number of movie plots", rotation = 90)


def percentage_of_movies_with_key_words_before_after(df, mid_value, horizon_years=10):
    df_occ= df.reset_index()
    before_horizon = mid_value - horizon_years
    after_horizon = mid_value + horizon_years

    df_occ_before = df_occ[(before_horizon <= df_occ['Movie_release_date']) * (df_occ['Movie_release_date'] < mid_value) == 1]
    df_occ_after = df_occ[(mid_value <= df_occ['Movie_release_date'])  * (df_occ['Movie_release_date'] < after_horizon) == 1]

    df_res = pd.DataFrame(data={
    f'{before_horizon}-{mid_value - 1}': df_occ_before.sum() / df_occ_before['Movies'].sum(),
    f'{mid_value}-{after_horizon - 1}': df_occ_after.sum() / df_occ_after['Movies'].sum()
    })

    df_res = df_res.drop(['Movie_release_date', 'Movies']).map(lambda x: round(x*100, 2))

    df_res.insert(0, 'Words', df_occ.columns[1:-1])

    s = pd.Series(range(len(df_res)))
    df_res.set_index(s, inplace=True)

    return df_res


def plot_percentage_before_after(df, mid_value, horizon_years=10):
    before_horizon = mid_value - horizon_years
    after_horizon = mid_value + horizon_years

    fig = px.bar(df,  x='Words', y=[f'{before_horizon}-{mid_value - 1}', f'{mid_value}-{after_horizon - 1}'], labels={'value':'Percentage of movies', 'Words':'Key word', 'variable':'Time period'}, barmode='group', title='Change of percentage of movies that contain certain key words')
    return fig


def percentage_of_movies_with_key_words_before_during_after(df, first_year=1940, last_year=1946, horizon_years=10):
    df_occ= df.reset_index()
    before_horizon = first_year - horizon_years
    after_horizon = last_year + horizon_years

    df_occ_before = df_occ[(before_horizon <= df_occ['Movie_release_date']) * (df_occ['Movie_release_date'] < first_year) == 1]
    df_occ_during = df_occ[(first_year <= df_occ['Movie_release_date']) * (df_occ['Movie_release_date'] <= last_year) == 1]
    df_occ_after = df_occ[(last_year < df_occ['Movie_release_date'])  * (df_occ['Movie_release_date'] <= after_horizon) == 1]

    df_res = pd.DataFrame(data={
    f'{before_horizon}-{first_year - 1}': df_occ_before.sum() / df_occ_before['Movies'].sum(),
    f'{first_year}-{last_year}': df_occ_during.sum() / df_occ_during['Movies'].sum(),
    f'{last_year + 1}-{after_horizon}': df_occ_after.sum() / df_occ_after['Movies'].sum()
    })

    df_res = df_res.drop(['Movie_release_date', 'Movies']).map(lambda x: round(x*100, 2))

    df_res.insert(0, 'Words', df_occ.columns[1:-1])

    s = pd.Series(range(len(df_res)))
    df_res.set_index(s, inplace=True)

    return df_res


def plot_percentage_before_during_after(df, first_year, last_year, horizon_years=10):
    before_horizon = first_year - horizon_years
    after_horizon = last_year + horizon_years

    fig = px.bar(df,  x='Words', y=[f'{before_horizon}-{first_year - 1}', f'{first_year}-{last_year}', f'{last_year + 1}-{after_horizon}'], labels={'value':'Percentage of movies', 'Words':'Key word', 'variable':'Time period'}, barmode='group', title='Change of percentage of movies that contain certain key words')
    return fig
