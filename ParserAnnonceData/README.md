# Problem

Our goal is to create relation between offer and receiver people. We have a table of proposed and requested services for each person signed in on a website. To make a match, we need to have a common point based on the topic of the shared service. We have to deal with a raw dataset like : 

| Title                                   | 
|-----------------------------------------| 
| cours français                          | 
| Cours de français - du Collège au Lycée | 
| Cours de Français                       | 
| Cours de français niveau collège        | 
| Cours de français jusqu'au BAC          | 
| COURS D'ANGLAIS                         | 
| Cours particuliers en Anglais           | 


where both "français" and "anglais" services could be joined.


## Solution 

Because of the dataset, we needed to uniformize the title field for each ad. We used machine learning algorithms to automatise the classification.

> python3 classify_annonce_topics.py


By the way, our solution is based on unsupervised classification (kmeans-clustering algorithm). 


## Openings
We would love to use syntax-logic algorithms to improve the performances and robustness of the classification. Why not deep learning...

# Inspirations 
- [Sentiment based on syntax-logic (Nlkt + Scikit)](http://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html)
- [Syntax language (Spacy)](https://github.com/explosion/spaCy/blob/master/spacy/fr/stop_words.py)
- [Text classification with bayesian classifier (TextBlob)](http://stevenloria.com/how-to-build-a-text-classification-system-with-python-and-textblob/)
- [Markov chain generator](https://github.com/jsvine/markovify)
- [Neural network (SyntaxNet - TensorFlow)](https://github.com/tensorflow/models/tree/master/syntaxnet#dependency-parsing-transition-based-parsing)
- [Convolutionnal neural networks (TensorFlow)](http://www.wildml.com/2015/11/understanding-convolutional-neural-networks-for-nlp/)
- [Text classification with a convolutionnal neural network (TensorFlow)](http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/)
- [Email classification (TensorFlow)](http://jrmeyer.github.io/tutorial/2016/02/01/TensorFlow-Tutorial.html)
