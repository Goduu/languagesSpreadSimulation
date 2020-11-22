# Languages Spread Simulation
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

> This study case aims to serve as a start point to think about how all this process happened and how nationalism interferes in the natural spread process that occurs throughout history. It doesn't have the goal of being exact and makes a lot of naive assumptions, but it could serve as a starting tool to a later project that has more variables and more interactions.


Thanks to https://github.com/julienbordet/ whoms code I use to have the base of the simulation. 

## OVERVIEW
It has always interested me how the languages naturally developed so differently across the centuries. Niebaum [ 1 ] describes an interesting concept about dialects. In german terminology ‘dialect’ could be a synonym for ‘Mundart’ which literally means the art of the mouth or the speaking art. This is an important definition when we think that before the national states established an hegemonic language in its territories, the languages were free to develop themselves just as the speaking art determines. According to Piller [ 2 ] at some point in history there was a ‘dialect chain’, when there wasn’t a single village or group of people who lived next to each other and couldn't understand each other's dialect. Quoting her: 

“These languages or language varieties formed a so-called dialect chain, that is, a continuum of mutually intelligible ways of speaking where people from one place understood the people from neighbouring villages or cities, and where it was impossible to ever find a point of non-intelligibility even if the people who lived on points of the chain that were removed from each other to various degrees could not understand each other. “ [ 2 ]

This study case aims to serve as a start point to think about how all this process happened and how nationalism interferes in the natural spread process that occurs throughout history. It doesn't have the goal of being exact and makes a lot of naive assumptions, but it could serve as a starting tool to a later project that has more variables and more interactions.

## METHODOLOGY
The simulation was developed in Python and took as base the code of ‘julianbordet’ at his Github page [ 3 ]. His model has the purpose to simulate a disease spread with some variables and its states like ‘Infected’, ‘Immune’ or in ‘Quarantine. The model idea used has the only common characteristic of treating a spread reaction. In this case we will see how three languages could spread across an área and try to test the Piller’s [ 2 ] idea. 

After the initial simulation it will be compared with a second one taking in consideration an action of a national state and how it will influence the final result. 

### The scenario
At the beginning there will be an empty squared area. It will be divided in smaller squares which represent a region, family or group of people.  An example is shown at Figure 1.

![](/images/figure1.png)

Figure 1 - initial space area

The empty squares are a representation of an empty area, or the assumption that the people at this area are very susceptible to learning another language. They will be labelled as “Susceptibles”. 

Three colored squares will then be carefully displaced in this area representing the ancient native speakers of those three languages like shown at Figure 2. The colors are very important at the simulation level, not just because it’s representing the languages but it was made so that it will apply the RGB pattern. RGB stands for red green and blue and it is a standard method to combine colors and make new ones. It has, as the name said, three hues of light and could create 16,777,216 colors combinations.

![](/images/figure2.png)

Figure 2 - Ancient Speakers Initial Positioning 

It works so that the color has 3 attributes (r,g,b) and each of them varies from 0 to 255 where 255 is the most presence of the referred light and 0 is the total absence of this light. That means that one mix of rgb(255,255,255) is equal to the color white and a rgb(0,0,0)  is equal to black like shown in Table 1. 

![](/images/table1.png)

 Table 1 - RGB example of colors

But why is it important to know those things to understand the simulation? It comes to the fact that when we mix the rgb hues we create another color, so that will represent exactly our language spread and mixture. For example, when the ancient red language meets the ancient green language they will create a new yellow language and a tons of its variances representing exactly what was told by Piller [ 2 ]. 

### The dynamic 
Each square area has some characteristics. The main one is a vector where it stores what we can see as the ‘proficiency level’ in each ancient language or the influences that their language has from each one of the ancient languages. It’s formatted as 3 numbers from 0 to 255 as the rgb scale.

Each area has a maximum learning level which represents its capacity to absolve another language and it is also important to avoid that at the end of the simulation everyone knows just every language that wouldn’t be realistic. This maximum learning level is a number from 300 to 650 and it limits the sum of proficiency vector numbers. 
There is a random probability in each square from 5 to 50% that the neighbors don’t learn in each round.

The Figure 3 shows the class diagram of the Squared Area.

![](/images/figure3.png)

Figure 3 - Class diagram with the squared area attributes

The simulation is divided in rounds where all the changes occur. At each round happens the following:

* The ones who have (Status ‘Learned’) a language start to influentiate their neighbours to learn their language.
* Those who are learning (Status ‘Learning’) a new language influentiate their neighbours less than the one who has already learned it.
* The neighbours only learn new languages if their maximum learning level was not achieved. 

The Learning Fluxogram ist represented by Figure 4. It starts creating the area and allocating the Ancient Speakers. Each ancient speaker teaches his neighbors. Firstly check the neighbors status. 

If it's Susceptible it changes the status to Learning and then learns the teachers language.
If the status is Learning, is checked if the max learning level was achieved, if not it learns, also is checked if the max amount of the language vector is 255, if so the status is changed to Learned. Those ones with status Learning teach their neighbors with less efficiency.
 
If the status is Learned it will learn with a smaller efficiency. Those ones with status learned teaches their neighbors with more efficiency. 
Everyone teaches their neighbors except the Susceptible ones. The process ends when the max round number is achieved. 

![](/images/figure4.png)

Figure 4 - Learning Fluxogram

At the second step of this work, it will consider the presence of a national state in the middle of the area, with a 4th language: the Black one. This last language will be represented by the absence of the other three and the force of this national state rules will be represented by each round having an extra step with a probability of 80% to reinforce the Black Language within that area.

To finish the analyses it will be presented a third example with borders at each of the 3 languages influencing positively the learning of its mother language and negatively for the others. This influence will be modeled by decreasing the foreign language influence by 25% in each round with a 80% probability. There will also be “neutral zones”  where the language could be spread without the national limits for comparison effect. 

## RESULTS
The results will be qualitatively evaluated as the main purpose of the work is to lead a critical thinking about the relationship of Natural Language Spread and Nationalism. 

### Initial Simulation
The first simulation, as said, was made by just considering 3 Ancient Languages. They were placed where they should have around the same space to grow and then the simulation started. The steps are seen in Figure 5. 

![](/images/figure5.png)

Figure 5 - Simulation One at round 0, 35, 75 and 100

At the end we could see clearly how the languages interact with each other, creating new languages and new dialects throughout the time. The final result is seen in Figure 6.

![](/images/figure6.png)

Figure 6 - Simulation One Final Results

We could see that the Ancient Languages are still there. Mainly the Blue and Green ones have stayed unchanged at the bottom left and top right edges but as a whole is much more of a 3 new ones Pink, Light Blue and Yellow and some other variations from it.

It could represent how the languages spread without any border or rule. The people who interact with the others next to them need to somehow learn how to communicate. Even if they really learn a new language, as Mufwene [ 4 ] explains in his book, it should have some language related costs when a language spread happens. Even if this spread is being made by force as was the case in the colonialism expansion era, the new territory aggregates a lot of its own costumes in the language and it forms in some degree something new from the original one. 

This cost of changes is aligned with the Path Dependence idea of Prado [ 5 ] and how the choices that we made in the past influence our future decisions to reassure the path that we took. Adding to that North [ 6 ] defines the transactional costs of  change, how the humans are change resisten from an evolutive perspective and how it could have a lot of change costs supporting what was said by  Mufwene [ 4 ].

### The Nationalism Influence

In this second simulation we will think about a very specific case: the Luxembourg one. 

Luxembourg is a small Grand Duchy (funny to say a small grand when grand is big in french) surrounded by 3 bigger lands: France, Belgium and Germany and with a lot of immigrants. There are a lot of discussions about the use of Luxembourgish language  [ 7 ]  and the government gives some incentive to maintain it alive even though it’s only spoken there by around 350 thousand people. It’s not an extreme case of nationalism but it will illustrate perfectly our second case. Luxembourg will be represented in the middle of the map by a Black language as the other ones spread normally as seen in the first one. The Figure 7 shows the beginning and the result. 

![](/images/figure7.png)

Figure 7 - Luxembourg’s Simulation, beginning and end

In 2004 was established the Conseil Permanent de la Langue Luxembourgeoise for stabilizing materials, dictionaries and diffusing the Luxembourgish language, separating it from the standard German dialects [ 8 ]. But at this time, French and German were already very present there spoken by the majority of the native population. This case is interesting not just as an illustrative example of an institution  created to regulate a language but also for its representation of a real birth of a new language with a lot of elements in common with the other two ones presented there. Supporting even more the simulation idea that without previous regulations, the language is more influenced by the nearby ones in a very incisive way. 

The simulation shows that this influence could be seen as the Black area is still there at the end but it doesn’t eliminate the fact that at the borders the influence of others are present nevertheless. 

### Three National States

Now it will delimit three rectangular areas as shown in Figure 8, where there exists a higher influence from the national states and also some ‘neutral zones’ between them. Let’s see what will happen.

![](/images/figure8.png)

Figure 8 - Delimited Rectangle Areas of Nationalist Influence

The Figure 9 shows the final result and as expected the national regions delimited at figure 8 remain there as a picture of the actual nations where the nationalism together with the language rules make the natural process of language spread and development more static. 

![](/images/figure9.png)

Figure 9 - Simulation Three Final Result

It of course eases some problems of comprehension in the same country or establishes rules as a form of separate what is correct or what is not, but it is always good to realise how that influence really changes the natural path of language spread. It could also have its disadvantage in plurality terms and how some people who don't speak the perfect language could be seen as less capable even when it’s one second, third or sometimes fourth language. What is right or wrong in speaking terms? Is language not an evolving being? Wasn’t it ruled by what was most commonly practiced? If so, shouldn't it be more flexible and change faster as globalization brings more different languages together? 

## References 
[ 1 ] Einführung in die Dialektologie des Deutschen, by H. Niebaum, 2011, Page 5

[ 2 ] Piller, Ingrid. Intercultural communication: A critical introduction. Edinburgh University Press, 2017.

[ 3 ] JULIENBORDET, ‘spread’ Available at: <https://github.com/julienbordet/spread>. Access at: 28 oct. 2020.

[ 4 ] Mufwene, Salikoko. (2006). Language Spread. 10.1016/B0-08-044854-2/01291-8. 

[ 5 ] Prado, M., & Trebilcock, M. (2009). Path Dependence, Development, and the Dynamics of Institutional Reform. The University of Toronto Law Journal, 59(3), 341-379.

[ 6 ] North, D.C. 1993 “The New Institutional Economics and Development”, in EconWPA Economic History, No. 9309002.

[ 7 ] KING , ESTHER and SMITH-MEYER, BJARKE, Mind your language in Luxembourg. Available at: <https://www.politico.eu/article/migration-mind-your-language-petition-in-luxembourg/>. Access at: 28 oct. 2020.

[ 8 ] Loi du 25 juin 2004 portant réorganisation des instituts culturels de l’Etat


