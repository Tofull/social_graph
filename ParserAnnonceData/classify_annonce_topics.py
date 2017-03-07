#! /bin/python3
# Author : Loic Messal
# The goal of this script is to classify a csv file of sentences by regrouping topics.

# Classic modules
import time
import csv

# Machine learning modules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.externals import joblib


CSV_FILE = "extraction_data.csv" # input filename for unclassified data - replace by your own csv file
OUTPUT_FILENAME = "classified_data.csv" # output filename for data and their matching label - replace by your own csv file

NUMBER_OF_CATEGORIES = 15 # The number of clusters to form as well as the number of centroids to generate.

# Advanced algorithm parameters
MAX_ITER = 300 # Maximum number of iterations of the k-means algorithm for a single run.
N_INIT = 10 # Number of time the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia.

## French grammar (from https://github.com/explosion/spaCy/blob/master/spacy/fr/stop_words.py)
FRENCH_STOP_WORDS = ['ouverte', 'vif', 'jusque', 'aupres', 'absolument', 'cinquantième', 'dix-neuf', 'mêmes', 'anterieur', 'pan', 'ho', 'sauf', 'semblent', 'toi', 'directe', 'anterieures', 'très', 'avait', 'rendre', 'merci', 'semble', 'pure', 'parfois', 'bas', 'ni', 'sait', 'celui-ci', 'deuxième', 'deux', 'particulier', 'necessairement', 'nos', 'chut', 'premier', 'crac', 'quelconque', 'aux', 'eux', 'auront', 'peux', 'là', 'nouveau', 'quatorze', 'auraient', 'être', 'sept', 'ceux-ci', 'car', 'allons', 'hé', 'comparables', 'huit', 'a', 'uniformement', 'par', 'plein', 'sapristi', 'hou', 'quand', 'puis', 'aie', 'cent', 'miennes', 'parmi', 'lui', 'bah', 'diverse', 'près', 'pourrais', 'necessaire', 'differents', 'holà', 'beau', 'tu', 'devant', 'troisièmement', 'dont', 'neuf', 'suffit', 'auxquelles', 'certaine', 'concernant', 'tiens', 'ayant', 'moi-même', 'celles-ci', 'maint', 'as', 'passé', 'certain', 'celle-ci', 'quarante', 'étant', 'chers', 'allo', 'assez', 'rien', 'possessif', 'oust', 'un', 'pas', 'procedant', 'celui', 'pfut', 'sien', 'quel', 'restant', 'votre', 'surtout', 'tiennes', 'cinquième', 'une', 'quels', 'neanmoins', 'suffisante', 'neuvième', 'rares', 'notre', 'aucun', 'cela', 'desormais', 'malgre', 'quanta', 'vas', 'ci', 'dès', 'sont', 'elles-mêmes', 'ou', 'unes', 'ont', 'ouias', 'lors', 'mille', 'siennes', 'boum', 'quatre-vingt', 'meme', 'trente', 'pu', 'étaient', 'alors', 'ma', 'toutes', 'du', 'avant', 'debout', 'egale', 'reste', 'se', 'nous', 'lui-meme', 'après', 'touchant', 'vifs', 'seule', 'serait', 'vous-mêmes', 'euh', 'vingt', 'brrr', 'quelles', 'i', 'importe', 'eh', 'naturel', 'vu', 'pff', 'sa', 'eu', 'pres', 'sur', 'est', 'quoi', 'retour', 'pourrait', 'celles', 'fait', 'le', 'desquels', 'chiche', 'rarement', 'quatrièmement', 'pendant', 'plusieurs', 'dehors', 'nul', 'abord', 'quatrième', 'cependant', 'clic', 'olé', 'houp', 'sent', 'doivent', 'quant', 'basee', 'pfft', 'ô', 'dessus', 'hop', 'toujours', 'va', 'à', 'bien', 'et', 'partant', 'psitt', 'specifique', 'derrière', 'dixième', 'comme', 'multiple', 'auxquels', 'celle-là', 'tel', 'flac', 'sera', 'telles', 'tend', 'que', 'tres', 'comment', 'doit', 'etais', 'maximale', 'seul', 'hélas', 'possible', 'hi', 'non', 'ces', 'remarquable', 'soixante', 'différent', 'te', 'hue', 'certains', 'son', 'dedans', 'ainsi', 'compris', 'toute', 'tienne', 'onzième', 'voilà', 'elle', 'anterieure', 'prealable', 'moi-meme', 'cinquante', 'lorsque', 'naturelles', 'treize', 'contre', 'combien', 'relativement', 'derriere', 'tente', 'via', 'trois', 'attendu', 'cher', 'tels', 'nombreuses', 'ouste', 'vives', 'notamment', 'vos', 'si', 'même', 'deuxièmement', 'possessifs', 'celle', 'hep', 'durant', 'vivat', 'nôtre', 'vont', 'feront', 'extenso', 'nous-mêmes', 'semblaient', 'nombreux', 'peu', 'auquel', 'tac', 'moins', 'afin', 'dessous', 'floc', 'paf', 'tant', 'possibles', 'siens', 'ouvert', 'restrictif', 'uniques', 'malgré', 'dernier', 'aura', 'effet', 'plus', 'bigre', 'septième', 'probante', 'excepté', 'sacrebleu', 'suit', 'ton', 'etait', 'differentes', 'couic', 'certes', 'suivante', 'ta', 'deja', 'dix-sept', 'où', 'vive', 'duquel', 'uns', 'personne', 'directement', 'premièrement', 'tic', 'etaient', 'celui-là', 'derniere', 'hors', 'pense', 'o', 'hein', 'tenir', 'parle', 'quatre', 'douzième', 'sinon', 'quiconque', 'chères', 'es', 'cet', 'envers', 'six', 'entre', 'parce', 'voici', 'toi-même', 'leur', 'avoir', 'tes', 'tellement', 'dit', 'gens', 'multiples', 'ai', 'hum', 'parlent', 'revoici', "aujourd'hui", 'avons', 'exterieur', 'seize', 'suivant', 'faisaient', 'outre', 'precisement', 'suivants', 'ceux', 'pouah', 'aucune', 'été', 'sienne', 'moi', 'peut', 'restent', 'mes', 'quoique', 'mien', 'longtemps', 'nôtres', 'plouf', 'las', 'première', 'ceci', 'superpose', 'dire', 'vlan', 'ne', 'avec', 'encore', 'mon', 'hormis', 'suffisant', 'ça', 'lequel', 'tout', 'environ', 'hurrah', 'subtiles', 'particulière', 'je', 'allaient', 'vé', 'lesquels', 'ès', 'ailleurs', 'étais', 'douze', "quelqu'un", 'celles-là', 'ceux-là', 'pur', 'tien', 'revoilà', 'vers', 'autre', 'té', 'donc', 'allô', 'clac', 'soi', 'différents', 'sein', 'sous', 'faisant', 'onze', 'soi-même', 'différente', 'miens', 'etant', 'vais', 'eux-mêmes', 'ses', 'cinquantaine', 'beaucoup', 'certaines', 'specifiques', 'na', 'probable', 'chacune', 'devra', 'semblable', 'stop', 'toc', 'qu', 'zut', 'moyennant', 'etre', 'jusqu', 'different', 'egales', 'dits', 'quelque', 'elle-même', 'il', 'â', 'puisque', 'lui-même', 'ha', 'pouvait', 'façon', 'suis', 'souvent', 'chaque', 'chez', 'seraient', 'ouverts', 'bravo', 'speculatif', 'cinq', 'de', 'soit', 'hem', 'naturelle', 'autrui', 'mince', 'tous', 'maintenant', 'ait', 'les', 'aujourd', 'minimale', 'leurs', 'on', 'chère', 'comparable', 'ce', 'suivre', 'ore', 'memes', 'mais', 'plutôt', 'qui', 'parseme', 'tsouin', 'lesquelles', 'exactement', 'sixième', 'me', 'suivantes', 'ollé', 'autrefois', 'font', 'toutefois', 'sans', 'était', 'rare', 'delà', 'des', 'devers', 'desquelles', 'juste', 'lès', 'la', 'quelle', 'huitième', 'selon', 'proche', 'laisser', 'da', 'enfin', 'particulièrement', 'dans', 'différentes', 'etc', 'mienne', 'vous', 'ouf', 'depuis', 'pire', 'moindres', 'ils', 'quinze', 'dix', 'trop', 'dite', 'relative', 'oh', 'seulement', 'bat', 'cette', 'fi', 'aussi', 'peuvent', 'tardive', 'dring', 'en', 'chacun', 'divers', 'dix-huit', 'désormais', 'vôtre', 'fais', 'vôtres', 'parler', 'quelques', 'pif', 'laquelle', 'avaient', 'rend', 'telle', 'ohé', 'elles', 'ah', 'au', 'seront', 'strictement', 'avais', 'egalement', 'autrement', 'aurait', 'pour', 'néanmoins', 'diverses', 'quant-à-soi', 'autres', 'tenant', 'tsoin', 'unique', 'hui', 'pourquoi', 'permet', 'troisième', 'apres']





# Parse csv file to machine learning format data
with open(CSV_FILE, 'r') as csv_file:
    reader = csv.reader(csv_file)
    data = []
    for row in reader:
        data.append(row[0])


# Vectorize the data list
vectorizer = TfidfVectorizer(stop_words=FRENCH_STOP_WORDS)
X = vectorizer.fit_transform(data)


# Classify the data
model = KMeans(n_clusters=NUMBER_OF_CATEGORIES, init='k-means++', max_iter=MAX_ITER, n_init=N_INIT)
model.fit(X)


## Save the model (for persistence)
modelFileName =  time.strftime("model-%Y%m%d-%H%M%S.pkl")
joblib.dump(model, modelFileName)


## Print best-matching words for each classification category
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(NUMBER_OF_CATEGORIES):
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :3]:
        print(' %s' % terms[ind])
    print()


# Save the classification matching into a csv file
with open(OUTPUT_FILENAME, 'w', newline='') as csv_file:
    spamwriter = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
    spamwriter.writerow(["# Resulting classification from model file : "+modelFileName])

    for index_doc in range(len(data)):
        thematique = []
        for index_keywords in order_centroids[model.labels_[index_doc],:3]:
            thematique.append(terms[index_keywords])

        spamwriter.writerow([data[index_doc], " ".join(thematique)])
