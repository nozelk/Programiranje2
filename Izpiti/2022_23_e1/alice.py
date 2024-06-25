import requests
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

nltk.download('punkt')

# Preberemo vsebino spletne strani
url = "https://www.gutenberg.org/files/11/11-h/11-h.htm"
response = requests.get(url)
html_content = response.text

# Očistimo HTML oznake in posebne znake
clean_text = re.sub(r'<[^>]+>', '', html_content)
clean_text = re.sub(r'[^\x00-\x7F]+', ' ', clean_text)  # Odstranimo ne-ASCII znake
clean_text = re.sub(r'\"', '', clean_text)
clean_text = re.sub(r'\s+', ' ', clean_text)

# Razbijemo besedilo na stavke
sentences = sent_tokenize(clean_text)

# Najdemo imenske entitete, ki niso na začetku stavka
entities = []
for sentence in sentences:
    words = word_tokenize(sentence)
    for i in range(1, len(words)):
        if words[i][0].isupper() and words[i-1] not in '.!?;':
            entity = words[i]
            # Združevanje besed, ki so del iste imenske entitete (npr. "Mock Turtle")
            while i+1 < len(words) and words[i+1][0].isupper():
                i += 1
                entity += ' ' + words[i]
            entities.append(entity)

# Preštejemo število pojavitev vsake imenske entitete
# Izločimo neželene entitete, kot so samostojne velike začetnice
filtered_entities = [entity for entity in entities if len(entity) > 1]

entity_counts = Counter(filtered_entities)

# Prikažemo 15 najpogostejših entitet
most_common_entities = entity_counts.most_common(15)
for entity, count in most_common_entities:
    print(f"{entity}\t({count}x)")
