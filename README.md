# Title : 9/11 - Did you see the impact from your sofa

# Abstract:

On September 11, 2001, terrorist hijacked two planes into One and Two World Trade Center. In the space of two hours, the tower collapse. Nearly 2800 people died this day. This event marks the beginning of the war opposing the United States and terrorism. Recognizing cinema as mirror of society, our motivation is to explore how traumatic, world-altering events, like 9/11, influence storytelling in film, particularly in terms of themes of security, nationalism, fear, and resilience. Based on this assumption, we aim to identify shifts in genre preferences, character archetypes and plot structure. Our goal is to tell the story on how cinema is defined by the culture identity and the collective trauma. More importantly, we want to show how cinema evolves in response a pivotal event: 9/11. 
Our project is based on the analysis of racism and terrorism representation in the US production compared to the rest of the world before and after 9/11. 

# Research Questions: 
A list of research questions you would like to address during the project.
Questions: 

•	What is the impact on racism of 9/11? Do we observe a change in some ethnicities on actor representation? What ‘s their role, how are they describe? On a similar aspect, 9/11 attacks were claimed by Al-Qaeda, a group of extreme radicalized Muslims terrorist. Did it have an impact on the Muslim representation in movies? 

•	Cinema is often considered as a mirror of society. Therefore, was there an impact of 9/11 on cinema production, most importantly do we observe a shift in genre compared to the previous decade?

•	We assume the impact of 9/11 was greater in the United States compared to the rest of the world. But can we find other places where it had a great impact too on cinema? Those these places are known to have close relation with United States, or were they victim of similar attacks at the same time? 

•	Did this breakthrough event slow the cinema industry or on the contrary did we observe an increase?


# Additional datasets (if any): 

The datasets we already have at our disposal often use Freebase IDs to provide some useful information. Unfortunately, it is hard to work with Freebase IDs nowadays because the Google Freebase API that was used to get meaningful information from these IDs was removed a few years ago. In order to translate these IDs into meaningful information, we had to find an alternative. We use the freebase-wikidata-label dataset found here : https://www.kaggle.com/datasets/latebloomer/freebase-wikidata-mapping/data. This dataset consists of 3 columns : freebase_id, wikidata_id and label. From this dataset, we simply created a function that maps any freebase ID to its label. The dataset contains more than 2 000 000 lines so the mapping is not extremely fast, but it is really manageable (1 to 3 hours to call the function 100k times).

# Methods

## Preprocessing 

We'll start by performing necessary preprocessing steps, including:

- Discarding outliers
- Imputing missing values
- Creating more meaningful columns
- Transforming data types

We'll save the preprocessed datasets in our data folder.

## Analysis 
To investigate the impact of the 9/11 incident on the movie industry, we'll analyze our cleaned movie dataset in several ways:

### Discrimination Analysis
We'll examine if there's a noticeable difference in the representation of ethnicities of actors and villains in movies before and after 9/11, specifically looking for signs of racism and/or islamophobia.

### Genre Proportions Analysis
We'll compare the proportions of films in different genres, particularly the war genre, to see if there's a change in the number of films produced after 9/11.

### Plot Summary Analysis
We'll analyze the vocabulary in plot summaries to see if there's a difference in the frequency of words related to 9/11, such as terrorism, towers, and plane. We may use NLP models to quantify the differences.

### US vs. WRLD Analysis
We'll compare the impact of 9/11 on the US movie industry with its impact on the rest of the world, examining which regions were more or less affected.

# Proposed timeline
Week 1 : HW2 <br>
Week 2 : HW2 + Project focus discrimination, genres proportions, plot summary analysis <br>
Week 3 : Project focus US vs. WRLD and code reformatting <br>
Week 4 : Creation of the platform and upload primary findings <br>
Week 5 : Finish the platform and github for the submission

# Organization within the team: 
HW2 : ALL <br>
Discrimination : Louis <br>
Genre proportions : Ines <br>
Plot summary analysis : Mirco <br>
US vs WRLD : Justine <br>
Platform : Théodore

# Questions for TAs (optional): 
- We thought it would be more interesting to focus not only on one event but to three-four events to show better how major events imapct the movie industry. E.g. WW2. Our data story would then be about these major events.
- The Freebase ID for the ethnicities often do not map to anything. Do you know a way to either retrieve the ethnicities or why Wikidata does not have often something for a Freebase ID.
