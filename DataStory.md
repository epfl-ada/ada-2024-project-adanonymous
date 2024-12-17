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

You wish to look at the plot summaries of movies. You think to yourself : "Surely having a world war has changed not only the types of movies produced but the content of the movies itself too..." You then try to compute some statistics over the plot summaries. 

You first try to look at the expected number of words before and after the second world war.
You filter out words that have an expected number of appearences less than 0.001, as they appear way too rarely. After some tedious computing, you obtain the first thirty biggest ratios :

(first 30 plot)

What does that mean ? We see that the word "tank" appeared ~11 times more afterwards, "japanese" ~10 times more and "terrorist" ~8 times more. You are a bit confused by some words that are too specific, such as "alex" or "sandy". You decide to filter more aggressively and take out words that have an expected number of appearences less than 0.01 now. Again you do some computing and you obtain this :

(second 30 plot)

You are happy to find more general words. You see that the words "phone" appears ~4 times more and camera appears ~3 times more. You approve these results as technology is more obviously more present after the begginning of WW2 than before. You notice that among the plot with more general words, the words "mission", "u.s.", and "killing" appear ~3 times more.  You can not say that WW2 is the cause of the more frequent usage of these words but we keep them in mind for later, when we will analyse the plot summaries in a more specific time period.

Okay, good. You try now to fit a scatter plot comparing the expected number of words before and after WW2 with a linear regression. It looks like this :

(scatter plot with regression)

The slope of the linear regression is ~1.37, suggesting that the expected number of a word tends to grow. This naively suggests that plot summaries got longer with time and should be ~1.37 longer in expectation, which makes sense but does not help us really here. We can however use this regression line to find interesting key words; you try to find the words that are the furthest from the regression line. This would allow for a more fair analysis for the biggest/smallest ratios, as it "normalizes" the fact that plot summaries got longer with time. You plot the ten furthest words :

(plot furthest words)

 You then think that the theme of killing got more popular after WW2 as you see the word "kill" is present again.

Instead of looking over statistics of all words, you try to focus on movies with certain key words. As key words, "Nazi", "Hitler", "Axis", "Allied" and "Jew" come first in your mind. You try to look at the number of movies that contain these key words. 

(plot of number of movies per key word)

(plot of number of movies per key word zoomed)

It makes sense that the word nazi is used a lot between 1940-1950, but you notice that it then stays constant, oscillating between 3 and 10 movies per year after 1950. The key words "Hitler", "Axis" and "Allied" present the same pattern, altough smaller in magnitudes. The key word "Jew" is more interesting. We can see growth until the beginning of WW2, where it shrinks a bit and stays constant until 1960, where it grows again. We could understand that after the atrocities comitted towards the jewish people, the movie industry may have been more prudent.

You find it interesting but it would make more sense to focus on time periods. You do that in two ways. First, you plot the years before and after the beginning of the war. Second, the years during the war, some years beforhand and some years afterwards. You remember the words "mission", "u.s.", "killing" and "kill" and you quickly add them in the key words. You plot the percentages of movies that contain the key words with respect to these time periods :

(plot of percentage of movies before after)

(plot of percentage of movies before during after)

We see again that the word "Nazi" was very present during the war, surely in propaganda movies. The words "Hitler", "Axis" and "Allied" have the same pattern, as we have seen beforehand already. We see again that thw word "Jew" gets less frequent. You look at the newly added key words. The word "Mission" present the same pattern as we have discussed. The words "u.s." and "killing" just grow with time. "kill" is an interesting key word. It is a lot used during the war compared to beforehand and stays the same afterwards.

We have seen that the word "kill" comes back often in our analysis, telling us that the violence of the war and death surely changed/shocked all human beings and that it reflects in the movie industry. 


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

You now look at the plot summaries of the movies. Surely after an event like this, plot summaries of movies have changed. But how ? You try then to compute interesting stuff.

You first try to look at the expected number of words before and after 9/11.
You filter out words that have an expected number of appearences less than 0.001, as they appear way too rarely. After some tedious computing, you obtain the first thirty biggest ratios :

(first 30 plot)

Mmmmh, we do not see any interesting words, except maybe "shrek"; it made you chuckle. You try then to to filter more aggressively and take out words that have an expected number of appearences less than 0.01. You obtain this now : 

(second 30 plot)

You obtain more general words, altough some are still too specific, as "kim" or "patrick". You see the words "video", "web" and "phone" which makes a lot of sense, as these got more popular after the 2000's. You notice the word "terrorist" with a ratio of ~2, which means it appears twice more often in plot summaries than before.

Okay, that was not very concluant. You try now to fit a scatter plot comparing the expected number of words before and after 9/11 with a linear regression.

(scatter plot with regression)

The slope of the linear regression is ~1.14, suggesting that the expected number of a word tends to grow slighlty. This naively suggests that plot summaries got longer with time and should be ~1.14 longer in expectation, which makes sense but does not help us really here. We can however use this regression line to find interesting key words; you try to find the words that are the furthest from the regression line. This would allow for a more fair analysis for the biggest/smallest ratios, as it "normalizes" the fact that plot summaries got longer with time.

(plot furthest words)

You again find words that are not related to our case at hand, except for the word "war". 

Instead of looking over statistics of all words, you try to focus on movies with certain key words. As key words, "plane", "tower", "terrorism", "hijack" and "islam" come first in your mind. You try to look at the number of movies that contain these key words. 

(plot of number of movies per key word)

(plot of number of movies per key word zoomed)

We can see that the word "terrorist" and "tower" were more frequent after 2002 and grow, but drops in 2010. The word "terrorism" slightly grows after 2001 but then drops in 2008. There is a peak for the word "hijack" in 2006 and then drops a bit.

Okay but it would make more sense to focus on time periods. You plot the years before and after 9/11. 

(plot of percentage of movies before after)

It is interesting to see that for the word "plane", it is less used after 9/11 than before, even though you would expect to have more.

{% include_relative assets/figures/9_11_key_words_occurence_14_18_24.html %} 

<img src="assets/img/shrek.jpg" alt="drawing" width="200"/>
![image](assets/img/shrek.jpg){: style="float: left"}
Fun fact : aboutaaaaaaaaaaa shrek 
zfgzifhziufhizuhfuzf zufygzuefg uzyfggzfgzfgizf


# Conclusion
