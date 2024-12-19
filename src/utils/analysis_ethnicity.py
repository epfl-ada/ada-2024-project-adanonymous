import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def map_continent(movie_country, continent_data_frame):
    label = continent_data_frame[continent_data_frame['Entity'] == movie_country]['World regions according to OWID']
    if len(label) > 0:
        return label.values[0]
    else:
        return None
    

def map_dataset(character):
    character.reset_index(drop=True, inplace=True)
    #Association for each character to two continent corresponding to First and Second country name (isolated during preprocessing)
    for i in range(len(character)):
        labels = map_continent(character['FirstCountry_Name'].iloc[i], continent_mapping_df)
        labels2 = map_continent(character['SecondCountry_Name'].iloc[i], continent_mapping_df)
        character.at[i, 'Continent'] = labels
        character.at[i,'Second_Continent'] = labels2
    return character


def plot_all_eth(regions):
    plt.figure(figsize=(15, 10))

    for i, (region, data) in enumerate(regions.items(), 1):
        plt.subplot(2, 3, i)
        data.plot(kind='bar', color='skyblue')
        plt.title(f"Top 10 Ethnicity in {region}")
        plt.xlabel("Ethnicity")
        plt.ylabel("Number of Actors")
        plt.xticks(rotation=45, ha='right')

    plt.subplots_adjust(wspace=0.5, hspace=1.5)
    plt.show()


def extract_top_10(df):

    list_ethnicities = list(set(character['Ethnicity_Label']))

    distribution = []

    for eth in list_ethnicities:
        count = df['Ethnicity_Label'].apply(lambda x: 1 if eth in x else 0).sum()
        distribution.append(count)

    ethnicities_dict = {
        'Ethnicity' : list_ethnicities,
        'Occurences' : distribution
    }

    ethnicities_distribution = pd.DataFrame(ethnicities_dict)
    sorted_df = ethnicities_distribution.sort_values(by='Occurences', ascending=False).head(10)
    ethnicity_top10 = sorted_df['Ethnicity'].head(10)

    return ethnicities_distribution, ethnicity_top10


def eth_per_year(data,year):
    data_new = data.loc[data['Movie_Release_Year'] == year]
    distribution, top_10 = extract_top_10(data_new)

    return distribution, top_10


def plot_10_ethnicties(counts,year):
    """
    Plots the top 10 ethnicities for a given year based on occurrence counts.
    
    Parameters:
        counts (DataFrame): A DataFrame containing 'Ethnicity' and 'Occurences' columns.
        year (int): The year for which the plot is generated.
    """
    df_2010 = pd.DataFrame({ 
        'Ethnicity': counts['Ethnicity'],
        'year': counts['Occurences'],
    })  
    # Plot for 2010
    df_2010.set_index('Ethnicity').plot(kind='bar', color='skyblue', legend=False)
    plt.title(f'Top 10 Ethnicities in {year}')
    plt.ylabel('Occurences')
    plt.xlabel('Ethnicity')
    plt.tight_layout()
    plt.show()


def ethnicity_count(regions):
    '''
    Analyzes ethnicity distribution for movie data across specified time periods and regions.

    Args:
        regions (dict): A dictionary where keys are region names and values are pandas DataFrames 
                        containing movie data. Each DataFrame must include 'Movie_Release_Year' 
                        and 'Ethnicity' columns.

    Returns:
         - ethnicity_counts_1937_1941 (dict): Counts of top 10 ethnicities for 1937–1941.
         - ethnicity_counts_1942_1948 (dict): Counts of top 10 ethnicities for 1942–1948.
         - data_1937_1948 (dict): Filtered data for 1937–1948 by region.
         - distribution_1937_1941 (dict): Ethnicity distribution for 1937–1941 by region.
         - distribution_1942_1948 (dict): Ethnicity distribution for 1942–1948 by region.
    '''
    # Initialize dictionaries to store results for each region
    # Initialize dictionaries to store results for each region
    ethnicity_counts_1937_1941 = {}
    ethnicity_counts_1942_1948 = {}
    data_1937_1948 = {}
    ethnicities_distribution = {}
    distribution_1937_1941 = {}
    distribution_1942_1948 = {}
    for region_name, region_data in regions.items():
    # Filter data for the year ranges
        data_1937_1941 = region_data[
            (region_data['Movie_Release_Year'] >= 1937) & 
            (region_data['Movie_Release_Year'] <= 1941)
        ]
        data_1942_1948 = region_data[
            (region_data['Movie_Release_Year'] >= 1942) & 
            (region_data['Movie_Release_Year'] <= 1948)
        ]
        data_1937_1948[region_name] = region_data[
            (region_data['Movie_Release_Year'] >= 1937) & 
            (region_data['Movie_Release_Year'] <= 1948)
        ]

        
        ethnicities_distribution[region_name], top_ethnicities = extract_top_10(data_1937_1948[region_name])

        #Extract top 10 for given time range
        distribution_1937_1941[region_name], _ = extract_top_10(data_1937_1941)
        distribution_1942_1948[region_name], _ = extract_top_10(data_1942_1948)
        #Isolate the one being in the top 10 ethnicities
        counts_1937_1941 = distribution_1937_1941[region_name][distribution_1937_1941[region_name]['Ethnicity'].isin(top_ethnicities)]
        counts_1942_1948 = distribution_1942_1948[region_name][distribution_1942_1948[region_name]['Ethnicity'].isin(top_ethnicities)]


        ethnicity_counts_1937_1941[region_name] = counts_1937_1941
        ethnicity_counts_1942_1948[region_name] = counts_1942_1948
    return ethnicity_counts_1937_1941,ethnicity_counts_1942_1948,data_1937_1948,distribution_1937_1941,distribution_1942_1948


def form_df(ethnicity_counts_1937_1941,ethnicity_counts_1942_1948):
    """
    Converts ethnicity counts for different regions into DataFrames for easier plotting and analysis.

    Returns:
        dict: A dictionary where each key is a region (e.g., 'North Americas', 'South America', 'Asia', 'Africa', 'Europe')
              and each value is a DataFrame containing ethnicity counts for two time periods: '1937-1941' and '1942-1948'.
    """
    # Convert ethnicity counts to DataFrames for easier plotting
    df_NA = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['NA']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['NA']['Occurences'],
        '1942-1948': ethnicity_counts_1942_1948['NA']['Occurences']
    })

    df_SA = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['SA']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['SA']['Occurences'],
        '1942-1948': ethnicity_counts_1942_1948['SA']['Occurences']
    })
    df_AS = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['AS']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['AS']['Occurences'],
        '1942-1948': ethnicity_counts_1942_1948['AS']['Occurences']
    })
    df_AF = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['AF']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['AF']['Occurences'],
        '1942-1948': ethnicity_counts_1942_1948['AF']['Occurences']
    })
    df_EU = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['EU']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['EU']['Occurences'],
        '1942-1948': ethnicity_counts_1942_1948['EU']['Occurences']
    })

    #We want to isolate the relevant continent, therefore we look at their ethnicity count and choose 50 as threshold for count in each continent
    regions = {'North Americas':df_NA,'South America': df_SA,'Asia': df_AS,'Africa': df_AF,'Europe': df_EU}
    return regions


def display_length_eth(regions):
    """
    Displays the total number of entries for the '1937-1941' and '1942-1948' columns for each region.

    Args:
        regions (dict): A dictionary where each key is a region name (e.g., 'North America', 'Europe') and each value 
                        is a DataFrame containing at least the columns '1937-1941' and '1942-1948', 
                        representing the counts of ethnicities in these time periods.

    Returns:
        None: Prints out the total count for each region and time period.
    """
    for region_name,region_df in regions.items():
        print(f"Region: {region_name} has {region_df['1937-1941'].sum()} entries in '1937-1941' and {region_df['1942-1948'].sum()} '1942-1948'.")


def plot_eth(regions,titles):
    '''
    Plots ethnicity distribution for each region across two time periods (1937–1941 and 1942–1948).

    Args:
        regions (list): A list of pandas DataFrames, where each DataFrame contains:
                        - 'Ethnicity': A column for ethnicity names.
                        - Other columns for the time period counts (e.g., '1937–1941' and '1942–1948').
        titles (list): A list of titles corresponding to the regions, used for plot annotations.

    Returns:
        None: Displays the plots. 
    '''
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes = axes.flatten()
    #Plot each DataFrame
    for i, (df, title) in enumerate(zip(regions, titles)):
        df.set_index('Ethnicity').plot(
            kind='bar',
            ax=axes[i],  # Use flattened axis array
            color=['#4c72b0', '#55a868']
        )
        axes[i].set_title(f'{title}\n (1937-1941 vs 1942-1948)')
        axes[i].set_ylabel('Occurences')
        axes[i].set_xlabel('Ethnicity')
        axes[i].legend(title="Time Period")
        axes[i].set_xticklabels(df['Ethnicity'], rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def percentage_df(ethnicity_counts_1937_1941,ethnicity_counts_1942_1948):
    """
    Converts ethnicity counts for North America (NA) and Europe (EU) into percentage form
    for the years 1937-1941 and 1942-1948. This allows for easy comparison of the proportion 
    of different ethnicities in these two time periods.

    Args:
        ethnicity_counts_1937_1941 (dict): A dictionary containing ethnicity counts for the year 1937-1941. 
            - The dictionary keys should be 'NA' and 'EU', each containing a DataFrame with:
                - 'Ethnicity' column (the ethnicity names).
                - 'Occurences' column (the count of occurrences for each ethnicity).
        ethnicity_counts_1942_1948 (dict): A similar dictionary containing ethnicity counts for the years 1942-1948.

    Returns:
        list: A list containing two DataFrames:
            - One for North America (NA) showing the percentage of each ethnicity in the two time periods.
            - One for Europe (EU) showing the same.
    """
    # Convert ethnicity counts to DataFrames for easier plotting
    df_NA_percentage = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['NA']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['NA']['Occurences']/ethnicity_counts_1937_1941['NA']['Occurences'].sum(),
        '1942-1948': ethnicity_counts_1942_1948['NA']['Occurences']/ethnicity_counts_1942_1948['NA']['Occurences'].sum()
    })

    df_EU_percentage = pd.DataFrame({
        'Ethnicity': ethnicity_counts_1937_1941['EU']['Ethnicity'],
        '1937-1941': ethnicity_counts_1937_1941['EU']['Occurences']/ethnicity_counts_1937_1941['EU']['Occurences'].sum(),
        '1942-1948': ethnicity_counts_1942_1948['EU']['Occurences']/ethnicity_counts_1942_1948['EU']['Occurences'].sum()
    })
    df_percentage = [df_NA_percentage,df_EU_percentage]
    return df_percentage


def ratio(df_regions):
    """
    Computes the ratio of change between two time periods (1937-1941 and 1942-1948)
    for North America and Europe and identifies the 5 largest changes for each region.

    Args:
        df_regions (list): A list of DataFrames, where:
            - df_regions[0] is the DataFrame for North America.
            - df_regions[1] is the DataFrame for Europe.
            Each DataFrame must have columns: '1937-1941', '1942-1948', and 'Ethnicity'.

    Returns:
        list: The modified list of DataFrames (with 'Ratio' column added).
    """
    df_NA = df_regions[0]
    df_EU = df_regions[1]
    df_NA['Ratio'] = -(df_NA['1937-1941'] - df_NA['1942-1948']) / (df_NA['1937-1941'])
    df_EU['Ratio'] = -(df_EU['1937-1941'] - df_EU['1942-1948']) / (df_EU['1937-1941'])
    # Sort by the ratio to find the largest 
    largest_ratios_NA = df_NA.sort_values(by='Ratio', ascending=False).head(5)
    largest_ratios_EU = df_EU.sort_values(by='Ratio', ascending=False).head(5)

    print("North America: 5 Largest Ratios: \n \n", largest_ratios_NA)
    print("\n \n Europe: 5 Largest Ratios:\n \n", largest_ratios_EU)


def plot_trend(eu_german_trend,na_german_trend,title1, title2,title3):
    '''
    Plots the trend of German characters in movies for Europe and North America over time,
    with a vertical line marking the end of World War II (1945).

    Args:
        eu_german_trend (list or array): The trend of German characters in European movies over time.
        na_german_trend (list or array): The trend of German characters in North American movies over time.
        title1 (str): The title label for the European trend.
        title2 (str): The title label for the North American trend.
        title3 (str): The overall plot title.

    Returns:
        None: Displays the plot.
    '''
    plt.plot(eu_german_trend, label=title1, marker='o')
    plt.plot(na_german_trend, label=title2, marker='o')

    plt.title(title3)
    plt.xlabel('Movie Release Year')
    plt.ylabel('Occurences')
    plt.axvline(x=1945, color='red', linestyle='--', label='End of WWII (1945)')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_absolute_trend_character(character_EU, character_NA):
    """
    This function plots the trends of German and Jewish characters' absolute character number in movies 
    before and after World War II for both Europe (EU) and North America (NA).

    Args:
        character_EU (DataFrame): DataFrame containing movie characters in Europe with columns:
            - 'Ethnicity_Label' (e.g., 'German', 'Jewish')
            - 'Movie_Release_Year' (release year of the movie)
        character_NA (DataFrame): DataFrame containing movie characters in North America with similar columns.
    
    Returns:
        None: Displays plots showing trends.
    """
    #Isolate European and North American character
    character_EU_German = character_EU[character_EU['Ethnicity_Label'].str.contains('German') ]
    character_EU_Jewish = character_EU[character_EU['Ethnicity_Label'].str.contains('Jewish')]
    character_NA_German = character_NA[character_NA['Ethnicity_Label'].str.contains('German')]
    character_NA_Jewish = character_NA[character_NA['Ethnicity_Label'].str.contains('Jewish')]


    #Look at the general trend of Jewish and German character before and after world war 2
    eu_german_trend = character_EU_German.groupby('Movie_Release_Year').size()
    eu_jewish_trend = character_EU_Jewish.groupby('Movie_Release_Year').size()
    na_german_trend = character_NA_German.groupby('Movie_Release_Year').size()
    na_jewish_trend = character_NA_Jewish.groupby('Movie_Release_Year').size()

    # Plot trends
    plt.figure(figsize=(12, 6))
    plt.subplot(1,2,1)
    plot_trend(eu_german_trend,na_german_trend,'EU German Characters','NA German Characters','Trends of German Characters (Before and After WWII)')
    plt.subplot(1,2,2)
    plot_trend(eu_jewish_trend,na_jewish_trend,'EU Jewish Characters','NA Jewish Characters','Trends of Jewish Characters (Before and After WWII)')
    plt.tight_layout()
    plt.show()


def plot_proportion_trend(character_EU,character_NA):
    """
    This function plots the trends of German and Jewish characters' proportions in movies 
    before and after World War II for both Europe (EU) and North America (NA).

    Args:
        character_EU (DataFrame): DataFrame containing movie characters in Europe with columns:
            - 'Ethnicity_Label' (e.g., 'German', 'Jewish')
            - 'Movie_Release_Year' (release year of the movie)
        character_NA (DataFrame): DataFrame containing movie characters in North America with similar columns.
    
    Returns:
        None: Displays plots showing trends.
    """
    #Isolate European and North American character
    character_EU_German = character_EU[character_EU['Ethnicity_Label'].str.contains('German') ]
    character_EU_Jewish = character_EU[character_EU['Ethnicity_Label'].str.contains('Jewish')]
    character_NA_German = character_NA[character_NA['Ethnicity_Label'].str.contains('German')]
    character_NA_Jewish = character_NA[character_NA['Ethnicity_Label'].str.contains('Jewish')]

    #Look at the general trend of Jewish and German character before and after world war 2
    eu_german_trend = character_EU_German.groupby('Movie_Release_Year').size()/character_EU.groupby('Movie_Release_Year').size()
    eu_jewish_trend = character_EU_Jewish.groupby('Movie_Release_Year').size()/character_EU.groupby('Movie_Release_Year').size()
    na_german_trend = character_NA_German.groupby('Movie_Release_Year').size()/character_NA.groupby('Movie_Release_Year').size()
    na_jewish_trend = character_NA_Jewish.groupby('Movie_Release_Year').size()/character_NA.groupby('Movie_Release_Year').size()

    # Plot trends
    plt.figure(figsize=(12, 6))
    plt.subplot(1,2,1)
    plot_trend(eu_german_trend,na_german_trend,'EU German Characters','NA German Characters','Trends of German Characters (Before and After WWII)')

    plt.subplot(1,2,2)
    plot_trend(eu_jewish_trend,na_jewish_trend,'EU Jewish Characters','NA Jewish Characters','Trends of Jewish Characters (Before and After WWII)')

    plt.tight_layout()
    plt.show()
