import nltk
import inflect
import os
import re

def compare_words(dictionary, cards):
    with open(dictionary, 'r') as d:
        words1 = set(clean_text(d.read()).split())

    inf_eng = inflect.engine()

    for card in cards:
        with open(card, 'r') as c:
            card_text = clean_text(c.read())
            words2 = set(card_text.split())

        words2_singular = set(inf_eng.singular_noun(word) or word for word in words2)
        absent_words = words2_singular.intersection(words1)

        file_name = "result/category/"+ os.path.splitext(os.path.basename(card)[0] + "_result.txt")

        with open(file_name, 'w') as output_file:
            output_file.write("\n".join(absent_words))
#lis le texte dont les lignes ne commencent par du texte parasite et réécris le fichier avec seulement les lignes filtrées

        with open(file_name, 'r') as f:
            lines = f.readlines()

        lines = [line for line in lines if not line.startswith("dataimage") and not line.startswith("safevalue")]

        with open(file_name, 'w') as g:
            g.write("".join(lines))
            print("".join(lines))

    print("Comparison over, list created in", file_name, "\n")

def clean_text(text):
    cleaned_text = re.sub(r"\d", "", text)
    cleaned_text = re.sub(r"[^\w\s]","", cleaned_text)
    return cleaned_text.lower()

dictionary = "dictionnary.txt"

folder = "cards/category/..."
cards = ["workcard_name1.txt","workcard_name2.txt", "..."]

cards = [os.path.join(folder, card) for card in cards]

compare_words(dictionary, cards)
print("Terminé")