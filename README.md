# NLP-Movie_Scripts

This repo consists on the project by [PedroUria](https://github.com/PedroUria), [seanpili](https://github.com/seanpili) and [thekartikay](https://github.com/thekartikay) for our NLP class at GWU. The goal was to predict a movie's success based only on its script, before casting and production. We [scraped](Getting_the_data.py) [movie screenplays](scripts/) from the internet and matched them with [budget and box office data](get_success_data.py). Then, we [processed](script_processor_v2.py) the scripts into [individual character dialogues](diag_jsons/) and [extracted](feat_extraction/) [language features](data/) to [train machine learning models](modeling.ipynb) in order to predict a binary target (sucessful = positive ROI, unsuccessful = negative ROI). We did not get good results, but we were able to use the same features to [cluster](K-Means_Agglomerative_and_DbScan.ipynb) the characters into a few meaningful groups according to speech patterns. You can find out more in our [report](report/project_report.pdf) and [slides](slides/slides.pdf).


### Side Notes

Budget data is not going to be [very reliable](https://movies.stackexchange.com/questions/16774/is-there-a-way-to-find-out-about-movie-tv-budgets)...

Still, with [these numbers](https://www.the-numbers.com/movie/budgets/all) we can tell which movie succeeded and which movie didn't succeed, and the probability of being wrong is very low. However, the ROI we would get from the above source (or any source) is most likely [unrealistic](https://en.wikipedia.org/wiki/Hollywood_accounting).

Analyzing the actual screen direction too! Anything that doesn't fall into character dialogue and is not crap (would need some filtering) would fall under this category. Example from Braveheart:

> Hanging from the rafters of the barn are thirty Scottish noblemen and thirty pages, their faces purple and contorted by the strangulation hanging, their tongues protruding. Malcolm stabs the pitchfork into the ground in useless anger; John still grips the axe as he follows his father through the hanging bodies of the noblemen to the back row, to see the one man in commoner's dress, like theirs...

You can see how this kind of text could be quite relevant to model the movie.



