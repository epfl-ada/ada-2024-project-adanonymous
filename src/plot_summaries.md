# WW2

## plot summaries

You wish to look at the plot summaries of movies. You think to yourself : "Surely having a world war has changed not only the types of movies produced but the content of the movies itself too..." You then try to compute some statistics over the plot summaries. 

You first try to look at the expected number of words before and after the second world war.
You filter out words that have an expected number of appearences less than 0.001, as they appear way too rarely. After some tedious computing, you obtain the first thirty biggest ratios :

(first 30 plot)

What does that mean ? We see that the word "tank" appeared ~11 times more afterwards, "japanese" ~10 times more and "terrorist" ~8 times more. You are a bit confused by some words that are too specific, such as "alex" or "sandy". You decide to filter more aggressively and take out words that have an expected number of appearences less than 0.01 now. Again you do some computing and you obtain this :

(second 30 plot)

You are happy to find more general words. You see that the words "phone" appears ~4 times more and camera appears ~3 times more. You approve these results as technology is more obviously more present after the begginning of WW2 than before. You notice that among the plot with more general words, the words "mission", "u.s.", and "killing" appear ~3 times more.  You can not say that WW2 is the cause of the more frequent usage of these words but we keep them in mind for later, when we will analyse the plot summaries in a more specific time period.

Okay, good. You try now to fit a scatter plot comparing the expected number of words before and after WW2 with a linear regression. It looks like this :

(scatter plot with regression)

The slope of the linear regression is ~1.37, suggesting that the expected number of a word tends to grow bigger with a factor of ~1.37. This naively suggests that plot summaries got longer with time and should be ~1.37 longer in expectation, which makes sense. We can however use this regression line to find interesting key words; you try to find the words that are the furthest from the regression line. This would allow for a more fair analysis for the biggest/smallest ratios, as it "normalizes" the fact that plot summaries got longer with time. You plot the ten furthest words :

(plot furthest words)

 You then think that the theme of killing got more popular after WW2 as you see the word "kill" is present again.

Instead of looking over statistics of all words, you try to focus on movies with certain key words. As key words, "Nazi", "Hitler", "Axis", "Allied" and "Jew" come first in your mind. You try to look at the number of movies that contain these key words. 

(plot of number of movies per key word)

It makes sense that the word nazi is used a lot between 1940-1950, but you notice that it then stays constant, oscillating between 3 and 10 movies per year after 1950. The key words "Hitler", "Axis" and "Allied" present the same pattern, altough smaller in magnitudes. The key word "Jew" is more interesting. We can see growth until the beginning of WW2, where it shrinks a bit and stays constant until 1960, where it grows again. We could understand that after the atrocities comitted towards the jewish people, the movie industry may have been more prudent.

You find it interesting but it would make more sense to focus on time periods. You do that in two ways. First, you plot the years before and after the beginning of the war. Second, the years during the war, some years beforhand and some years afterwards. You remember the words "mission", "u.s.", "killing" and "kill" and you quickly add them in the key words. You plot the percentages of movies that contain the key words with respect to these time periods :

(plot of percentage of movies 1)

(plot of percentage of movies 2)

We see again that the word "Nazi" was very present during the war, surely in propaganda movies. The words "Hitler", "Axis" and "Allied" have the same pattern, as we have seen beforehand already. We see again that thw word "Jew" gets less frequent. You look at the newly added key words. The word "Mission" present the same pattern as we have discussed. The words "u.s." and "killing" just grow with time. "kill" is an interesting key word. It is a lot used during the war compared to beforehand and stays the same afterwards.

We have seen that the word "kill" comes back often in our analysis, telling us that the violence of the war and death surely changed/shocked all human beings and that it reflects in the movie industry. 

# 9/11

## plot summaries
