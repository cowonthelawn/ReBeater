**ReBeater Project Proposal**

Robert Allen

Regis University

MSCC 696: Data Science Practicum II

John Koenig

May 1, 2022

**Introduction**

Virtual reality is finding a solid foothold in the gaming industry. With the introduction of lower cost entry points into this technology, such as the Meta Quest, more people are starting to experience this area of entertainment. However, a lot of popular virtual reality experiences assume that the user is abled-bodied. Virtual reality experiences tend to rely on the use of a controller in both hands. Traditional mechanical techniques to counter the need to use two hands for controls do not work in this virtual environment.

**Problem Statement**

An extremely popular virtual reality game is a rhythm game called Beat Saber. In this game, colored blocks travel towards the player in time with the beat of a song. These blocks are then slashed with virtual blades in a direction indicated on each block. The color of the block indicates which controller is used to slash the block. While Beat Saber does have a mode that uses only a single color and hand, it does not have a lot of official support in the game itself. It is also underrepresented in the custom beat mapping community such as Beast Saver.

**Research Question**

This project will attempt to determine if it is possible to convert two handed custom maps from Beast Saver into single handed maps that are accessible to those players that do not have full access to a two-handed range of bodily motion. There are a lot of factors that make a custom map enjoyable, and these factors need to be identified and considered to ensure the finished product is quality interpretation of the original beat map.

**Data Description**

The data collection used in this project is a very manual process. The custom beat maps themselves are publicly available and easily obtainable. However, they do not exist in a single downloadable database and are in a JSON file format with a schema that will have to be read and converted into a usable data source for analysis.

Once the data is formatted in a way that it can be analyzed, the actual fields to be analyzed will have to be engineered from a data set that primarily focuses on single frames of a beat map to one that provides general data about a collection of beat maps and beat map states.

**Methodology**

A total of 42 songs were processed into 34,611 individual beat states. Using this data, two dataframes were populated in Python. These consisted of the flow data frame and the beat states data frame.

The flow dataframe focused on the flow between individual notes. Since the songs were designed to use both hands, the right-hand notes and left-hand notes were separated. Since a beats state can contain multiple notes, an algorithm was designed to identify the start of each swing of the saber in relation to the notes and their direction. In addition, beat states for each side had a maximum amount of time allowed between them to be recognized as valid transitions since two-handed maps can have large distances between notes of the same side. The flow dataframe contained the side, magnitude, horizontal vector, vertical vector, start note direction, end note direction, direction delta between the start and end notes, time between notes, and a boolean determining if it came from a song with good or bad reviews as engineered fields.

The beat states dataframe focused on two complete beat states that transitioned from one to other. Like the flow dataframe, individual sides were separated and a maximum time between beat states implemented. This dataframe contained the side, unique ID for each beat state, grid coordinates with populated notes, and a boolean determining if it came from a song with good or bad reviews as engineered fields.

Once captured, the data had to be cleaned before use. The transition dataframe was analyzed for beat state transitions would cause a dead end if they were implemented. In addition, the unique beat state IDs were alpha-numeric, and were mapped to numeric IDs. This was done to create more flexibility in the prediction model since the output is a beat state and keeping it alpha-numeric would result in too many restrictions in model selection.

After cleaning, two new dataframes were created. A transition dataframe and a key translation table dataframe. The key translation dataframe contained the numeric key mapped to the alpha-numeric beat ID. The transition data frame only contained a previous and current numeric beat ID.

This project attempted two different models one to classify the flow score of a swing and the other to predict the next beat state when given details about the current beat state. The flow classification model could not be implemented. The worst rated songs had too many swings with good flow. This resulted in data overlap between swings with good flow and swings with bad flow. For example, a Naïve-Bayes model resulted in a model that purely guessed with an accuracy of 57% and a Cohen’s Kappa of 0.1. Fixing the data would require too much manual scoring for the scope of this current project.

![](media/7a147e87918d4dbeec70f2908a4199df.png)![](media/0d63f29b42b19638f2c5cad41b926901.png)![](media/959ba701d9f14eeeff2435eff8a1d39d.png)

The beat state data did not suit standard exploratory analysis, as it simply contained beat state IDs, mapped keys, and the grid of the beat state. The first modeling attempt used a Gaussian Naïve-Bayes model to predict the next state. The performance was abysmal, and the model was scrapped. The next model was a Support Vector Machine. This model had a 99.3% accuracy but caused a one-to one mapping that resulted quickly in an infinite loop of an individual beat state.

It was discovered that standard prediction models resulted in a one-to-one mapping that resulted in minimal beat states and infinite loops. A one-to-many prediction model was needed. A Markov chain was manually implemented, as it suited the needs of a one-to-many prediction model that needed a large variation in beat state predictions from each input beat state.

The resulting Markov chain took a total of 151 unique beat state transitions and ended up selecting 75 of them in its random walks. Out of those selected, 52 of them contained a high enough probability to be seen in a song that averaged around 800 transitions. It did not result in any infinite loops or dead-end states.

The Markov chain model performed well enough to be considered eligible for testing. Since the flow classification model failed, automatic scoring was impossible. As such, the resulting beat map was loaded onto BeatSaver.com and a preview of the song recorded. The resulting beat map contained mostly good flow between beat states. It did contain two beats that would be impossible to hit in one swing, which would have been detected and removed if the flow classifier had succeeded.

**Conclusion**

This project proved it is most likely possible to remap a two-handed beat map to a single-handed beat map. While missing the flow classification model hurt the results somewhat, the project showed that an algorithm that changed two-handed beat states to single-handed beat states can be successful.

It also showed that the Markov chain is effective at mapping the translated beat states onto an existing beat map. In the future, this model can be improved by implementing the following a manual flow classification data creation so a flow classifier can be implemented. This classification model could be used to eliminate states in the Markov chain that contain bad flow. In addition, Markov chains should be created for individual difficulty levels so more complex transitions do not appear in lower-level songs. The current version of this project used expert plus difficulty maps so that the maximum number of notes could be harvested per song.
