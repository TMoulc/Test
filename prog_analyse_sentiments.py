import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

# lire le fichier CSV
dataset = pd.read_csv("Restaurant_Reviews.csv", sep="\t", quoting=3)
# choisir la colonne qui contient les avis
reviews = dataset['Review'].values               

# importer le module nltk (installé avant)
import nltk
# télécharger les listes de mots les plus fréquents
#nltk.download('stopwords')
# importer ces listes
from nltk.corpus import stopwords
# récuperer la liste pour l'anglais
stoplist = set(stopwords.words('english'))

# importer le troncateur pour l'anglais
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# le premier avis:
avis = reviews[0]
#print(len(avis))

# liste de textes nettoyés
corpus = []
# pour chaque avis
for avis in reviews:
    # ne garder que des lettres et l'apostrophe
    avis = re.sub(r"[^a-zA-Z']", " ", avis)
    #print(avis)
    # mettre le texte en minuscule
    avis = avis.lower()
    #print(avis, avis.split())
    # tronquer chaque mot 'informatif' (pas dans stoplist)
    reviewL = [ps.stem(word) for word in avis.split() if not word in stoplist]
    #print(reviewL)
    # convertir la liste de mots en texte
    avis = " ".join(reviewL)
    #print(avis)
    # ajouter le texte à la liste de textes nettoyés
    corpus.append(avis)
    
#print(corpus)

# créer le vocabulaire et le modèle sac de mots

cv = CountVectorizer() #(max_features=5)
X = cv.fit_transform(corpus).toarray()
#print(X)

# identifier la classe dans CSV
y = dataset.iloc[:, 1].values

# dictionnaire vocabulary_ mot:position
#print(cv.vocabulary_) #...cv.vocabulary_['absolut']) permet de voir la position de "absolut" dans le classement
#for tvoc in cv.vocabulary_:
    #print(tvoc, cv.vocabulary_[tvoc]) #[tvoc] affiche la position des mots

# liste de mots du vocabulaire: get_feature_names()
#print(cv.get_feature_names_out()) #classer par ordre alphabétique
                                #[10] permet de voir quel mot est à la 10ème position
vocab = cv.vocabulary_
# séparer les données en train/test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
#print(X_train)
#print(y_train)


# importer la méthode de classification
from sklearn.naive_bayes import GaussianNB
classfr = GaussianNB()

# entrainer le modèle
classfr.fit(X_train, y_train)

# calculer la prévision à partir de X_test
y_pred = classfr.predict(X_test)
#for i in range (len(X_test)):
    #print("vrai classe:", y_test[i], "prédiction:", y_pred[i])

# matrice de confusion


# rapport de classification
from sklearn.metrics import classification_report
#print(classification_report(y_test, y_pred))

# fonction pour calculer la prévision pour un nouvel avis
def predict(new_review):  
    new_review = re.sub(r"\W|\d", " ", new_review) 
    new_review = new_review.lower()
    new_review = [ps.stem(word) for word in new_review.split() if word not in stoplist]   
    new_review = " ".join(new_review)
    # créer la liste qui contient le texte entier
    new_review = [new_review]
    # créer la matrice qui indique les mots du vocabulaire présents dans l'avis
    new_review = cv.transform(new_review).toarray()
    # print(new_review[0])
    # afficher les mots du vocabulaire utilisés pour la classification
    # i: position dans la matrice
    for i in range(len(new_review[0])):
        # pour chaque mot du vocabulaire
        for word in vocab:
            # si le mot est dans l'avis et sa fréquence n'est pas 0
            if i == vocab[word] and new_review[0][i] != 0:
                # afficher le mot et sa fréquence dans l'avis
                print(word, new_review[0][i])
    prediction = classfr.predict(new_review)
    sentiment = "L'évaluation est positive" if prediction == 1 else "L'évaluation est négative"
    # rendre la prévision du modèle
    return prediction, sentiment

# texte du nouvel avis
myOpinion = "Give me a refund, this food was atrocious, I will never come back again"
print(myOpinion)
print(predict(myOpinion))

# afficher l'avis et la prévision du modèle


