# WW2

## plot summaries

Finally, you wish to look at the plot summaries of movies. You think to yourself : "Surely having a world war has changed not only the types of movies but the content of the movies itself..." You then try to compute some statistics over the plot summaries. 

You first try to look at the expected number of words before and after the second world war.
You filter out words that have an expected number of appearences less than 0.001 as they appear way too rarely. After some tedious computing, you obtain the thirst thirty biggest ratios :

(first 30 plot)

We see that the word "tank" appeared ~11 times more, "japanese" ~10 times more and "terrorist" ~8 times more. You are a bit confused by some words that are too specific, such as "alex" or "sandy". You filter more aggressively and take out words that have an expected number of appearences less than 0.01 now. The plot looks like this now :

(second 30 plot)

You are happy to find more general words. You see that the words "phone" appears ~4 times more and camera appears ~3 times more. You approve these results as technology is more referenced after the begginning of WW2 than before. However, the words "mission", "u.s.", and "killing" appears ~3 times more. 


You try now to fit a scatter plot comparing the expected number of words before and after WW2 with a linear regression. The slope of the linear regression is ~1.37, suggesting that the expected number of a word tends to grow bigger with a factor of ~1.37. This suggests that plot summaries got longer with time and should be ~1.37 longer in expectation. In order to find interesting key words, you try to find the words that are furthest from the linear regression line. Here are the results : 

(plot furthest words)

You then think that the theme of killing got more popular after WW2 as you see the word "kill" is present again.

Instead of looking over statistics of all words, you try to focus on movies with certain key words. As key words, "Nazi", "Hitler", "Axis", "Allied" and "Jew" come first in your mind.  You look at the number of movies that mention these key words : 

(plot of number of movies per key word)

It makes sense that the word nazi is used a lot between 1940-1950, but you notice that it then stays constant, oscillating between 3 and 10 movies per year after 1950. The key words "Hitler", "Axis" and "Allied" present the same pattern, altough smaller in magnitudes. The key word "Jew" is more interesting. We can see growth until the beginning of WW2, where it shrinks a bit and stays constant until 1960, where it grows again. We could understand that after the atrocities comitted towards the jewish people, the movie industry may have ...

You split the data into two time periods, 1930-1939 and 1940-1949, hoping to see some interesting things. You plot the percentages of movies that contain the key words with respect to these time periods :

(plot of percentage of movies)

# 9/11

## plot summaries
