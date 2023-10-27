# Run this on a machine with more memory to generate the word list
import nltk
from nltk.corpus import reuters
from nltk import FreqDist

nltk.download('reuters')
words = [word.lower() for word in reuters.words() if word.isalpha()]
freq_dist = FreqDist(words)

common_words = [word for word, freq in freq_dist.most_common(3000) if len(word) >= 5]

with open('common_words.txt', 'w') as f:
    for word in common_words:
        f.write("%s\n" % word)
