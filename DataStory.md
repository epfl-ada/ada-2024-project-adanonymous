---
layout: home
title: World changing event
subtitle: Did you see the impact from your sofa 
---
# Introduction
Point initial, pk on choisit ces 2 event

Plot : evolution du nombre total avec bar vertical a cahque event 

[Go to World War 2](#ww2)

[Go to 9/11](#911)

# WW2 

 ## Genre anaylisis WW2


Imagine you’re relaxing on your sofa, ready to watch an old movie from the 1940s. Out of curiosity, you type "best movie 1942" into Google — the year of your grandfather's birth. To your surprise, the top three highest-rated films from that year, according to IMDb, are about crime and death.

This sparks your interest: could it be a coincidence, or was there a broader trend in movie genres at that time?


{% include_relative assets/figures/movie_genre_us_ww2_12_00_01.html %} 

To investigate, you look at the percentage of film genres with significant variation in a five-year range before and after 1942. The results reveal that genres like war films, propaganda films, and combat films increased in their occurence in the cinema. The data even highlights a peak, reflecting a rise in these types of films around this period.

Considering that World War II took place from 1939 to 1945, it becomes linked that the war influenced cinematic themes. The shift in genres appears to have started around 1940 and continued until around 1948.
You want to understand this trend a bit more, so you decide to focus on the "war film" genre across each of the main included continents: North America, Europe, and Asia.

{% include_relative assets/figures/War_film.html %} 

In 1943, war films represented more than 11% of films in Europe — a percentage that had doubled compared to 1941. A similar doubling occurred in the United States, while Asia experienced a significant increase as well. By 1946, the percentage of war films in all three continents had nearly returned to its original level.
Looking further back, an earlier peak is noticeable in Asia in 1938 and 1939, which is not observed in Europe or the United States. Intrigued by this anomaly, you consult a history book and discover a possible explanation: the Second Sino-Japanese War, which began in 1937 and ended in 1945. The start of this conflict may have induced the initial surge in war films in Asia.


## Ethniciy anaylisys 
Plot :  Ethncicity distribution bar avant après : interactif par continent 
Texte : analyse 
Plot jews german evolution before / après 

## Plot analysis 

You now want to look at the plot summaries of movies. You think to yourself, "Surely the impact of a world war must have influenced not only the types of movies produced but also their content..." So, you decide to compute some statistics based on the plot summaries.

First, you look at the expected number of words before and after World War II. To ensure the analysis is meaningful, you filter out words that appear too infrequently, removing those with an expected frequency of less than 0.001. After some calculations, you obtain the top thirty words with the largest ratio of occurrences.

(First 30 plot)

What does that tell us ? You observe that certain words have become significantly more frequent after the war. For example, "tank" appears roughly 11 times more often, "japanese" about 10 times more, and "terrorist" roughly 8 times more. Some words, such as "alex" or "sandy," are too specific and we would want more general words. So, you decide to filter more aggressively, removing words with an expected frequency lower than 0.01. 

(Second 30 plot)

Now, you are pleased to see more general terms. For instance, "phone" appears approximately 4 times more frequently, and "camera" about 3 times more often. These results seem reasonable, as technology is used a lot more after WWII. Among the more general terms, you also find words like "mission," "u.s.," and "killing" appearing about 3 times more often. While you cannot definitively attribute these shifts to WWII, you keep these findings in mind for future analysis when you focus on specific time periods.

Okay, good. Now, you decide to fit a scatter plot comparing the expected number of words before and after WWII with a linear regression.

(Scatter plot with regression)

The slope of the linear regression is approximately 1.37, suggesting that the expected frequency of a word tends to increase over time. This is simply because that plot summaries have gotten longer, with an average increase of about 1.37 times, which makes sense but doesn't provide much insight for our current analysis. However, we can use this regression line to identify interesting keywords by focusing on those that deviate the most from the line. This approach helps "normalize" the analysis by accounting for the general trend of longer plot summaries over time. You plot the ten words that deviate most from the regression line.

(Plot of furthest words)

From this, you observe that the theme of "killing" seems to have gained more prominence after WWII, as the word "kill" appears more frequently.

Next, you shift your focus to movies containing specific keywords. You first think of terms like "Nazi," "Hitler," "Axis," "Allied," and "Jew." You examine the number of movies featuring these keywords over time.

(Plot of number of movies per keyword zoomed)

It’s not surprising that the word "Nazi" peaks in the middle of WWII, but you notice that its frequency goes down already in 1944. We can not see it in the plot but you find that after 1950, between 3 and 10 movies per year contain the key word "Nazi", making it a theme. Similarly, the keywords "Hitler," "Axis," and "Allied" show a similar pattern, although with smaller magnitudes. The keyword "Jew" is more intriguing. We see growth leading up to WWII, then a slight decline during the war. You look at the time afterwards and you see a resurgence after 1960. This suggests that, in response to the atrocities committed against Jewish people, the film industry may have initially been cautious but gradually returned to addressing the topic in the post-war years.

You find this pattern interesting but decide it would be more insightful to focus on specific time periods. You examine the years during the war along with the years just before and after. You recall the words "mission," "u.s.," "killing," and "kill" and add them to your keyword list. You then plot the percentages of movies containing these keywords within the defined time periods.

(Plot of percentage of movies before, during, and after)

Once again, we see that the word "Nazi" was heavily used during the war, likely in propaganda films. The terms "Hitler," "Axis," and "Allied" follow the same pattern as before. The word "Jew" shows a noticeable decline during the war. Turning to the newly added keywords, "Mission" follows the same pattern as previously observed, while "U.S." and "Killing" steadily increase over time. "Kill" is particularly interesting: it appears significantly more during the war compared to before and remains steady afterward.

You think to yourself that WWII darkly influenced the content of movie plot summaries. It becomes clear that certain terms, such as "tank," "japanese," or "terrorist," became much more common post-WWII, reflecting the impact of the war on film themes. Additionally, terms related to violence, such as "killing" and "kill," grew in prominence during and after the war, suggesting a shift in the narrative focus of films. These results provide insights into how WWII shaped cinematic storytelling, with evolving themes related to technology, violence, and historical reflection.

# 9/11

## Genre anaylisis : US vs rest of the world

{% include_relative assets/figures/movie_genre_us_10_23_34.html %} 

If we focus on some genre trends around 2001, shifts can be observed in genres such as social issues, political cinema, law and crime, and culture and society.

Among these, political cinema seems to have an important change . To better understand this shift, we apply a linear regression to analyze the overall trend before and after 2001. Furthermore, we separate the analysis into U.S. and non-U.S. movies to determine whether the change is a global phenomenon or specific to the U.S.

{% include_relative assets/figures/regression.html %} 

The analysis shows that, for U.S. movies, the percentage of political cinema is relatively constant before 2001 but shows an upward trend afterward. In contrast, for non-U.S. movies, no significant change in the trend is observed. This suggests that the shift is primarily driven by an event within the U.S. and more probably the 09/11 crisis.

If this shift is linked to the events of 9/11, we want to know whether the trend is consistent for non-U.S. regions. To do so, we focus on three key regions: Europe, Asia, and North America.

Plot :  evoluion du genre political cinema genre par continent 

Starting from 2001, there is a noticeable emergence of the political cinema genre in Asia, where it was previously absent. In Europe, we observe a small increase in the genre's presence, less pronounced than the significant rise seen in the U.S.
This suggests that while the impact of 9/11 on political cinema is most evident in the U.S., its influence can also be seen, to a lesser extent, in other regions, particularly in Asia. Some cofounders might also be under the change in the other continents. 


## Ethnicity analysis
![Crepe](/assets/figures/WW2_etchnicty_distribution.png){: .mx-auto.d-block :}
Plot : Bar plot distribution ethicnty avant après event et  US vs rest of world
Analyse discussion rien concluant 
Plot : changement de ratio 
Rien de concluant 


## Plot analysis 

You decide to examine the plot summaries of movies, thinking that an event as significant as 9/11 must have influenced their content. But how exactly did it impact the plots ? You set out to compute some interesting statistics to explore this.

First, you analyze the expected number of words before and after 9/11. To ensure meaningful results, you filter out words that appear too infrequently — those with an expected frequency of less than 0.001. After some extensive calculations, you identify the top thirty words with the largest ratios of occurrence:

(First 30 plot)

Mmmmh, these results don’t reveal much. You notice the word "shrek", which makes you chuckle.

You decide to refine your analysis further by filtering out words with an expected frequency lower than 0.01. The new results look like this:

(Second 30 plot)

This time, you notice more general words, though some — like "Kim" or "Patrick" — remain too still too specific. More relevant terms like "video," "web," and "phone" stand out, reflecting their rise in popularity after the 2000s. Additionally, the word "terrorist" appears with a ratio of about 2, meaning it appears twice as often in plot summaries after 9/11.

Although this provides some interesting insights, the findings are not particularly conclusive. You then decide to plot a scatter graph comparing the expected number of words before and after 9/11, along with a linear regression line.

(Scatter plot with regression)

The regression slope is approximately 1.14, suggesting that the expected frequency of words tends to increase slightly over time. This indicates that plot summaries have generally gotten longer, which makes sense but doesn’t provide much additional insight for this analysis. However, you can use this regression line to identify keywords that are furthest from it. This provides a more accurate comparison of the ratios, accounting for the general trend of increasing plot summary length over time.

(plot furthest words)

You find several words that are not directly related to the topic at hand, except for "war."

Rather than analyzing all words, you decide to focus on movies featuring specific keywords. The terms "plane," "tower," "terrorism," "hijack," and "islam" comes first to mind. You then examine the number of movies containing these keywords.

(Plot of number of movies per keyword zoomed)

Strangely, the word "plane" drops in 2008. The data reveals that the words "terrorist" and "tower" became more frequent after 2002, showing an increase, though they drop in 2010. The term "terrorism" experiences a slight rise after 2001, followed by a decline in 2008. There’s also a peak in 2006 for "hijack," after which its frequency decreases.

However, it seems more insightful to focus on specific time periods. You plot the number of movies before and after 9/11.

(Plot of percentage of movies before and after)

Interestingly, the term "plane" is used less frequently after 9/11 than before, despite the expectation that it would appear more often. It is surely not linked to 9/11 as we saw in the previous plot that it begins to drop in 2008. We see a slight drop for all key words except for "terrorism" and "islam". This plot being heavily influenced from the time after 2008, it may have been more insightful to have smaller time periods before and after 9/11. 

In conclusion, analyzing the plot summaries of movies before and after 9/11 reveals some notable shifts in terminology, but the results are not entirely conclusive. While the analysis provides some useful trends, a more refined approach with smaller time periods before and after 9/11 could yield deeper insights.

{% include_relative assets/figures/9_11_key_words_occurence_14_18_24.html %} 

<img src="assets/img/shrek.jpg" alt="drawing" width="200"/>
![image](assets/img/shrek.jpg){: style="float: left"}
Fun fact : aboutaaaaaaaaaaa shrek 
zfgzifhziufhizuhfuzf zufygzuefg uzyfggzfgzfgizf


# Conclusion
