
import sys
import argparse
import string
import requests
import json
import nltk

API_URL = 'http://words.bighugelabs.com/api/2/f00bd31ac40db79c40caeb8cd7cccba5/{0}/json'
N = 0
VERBOSE = False

def lookup_word(word):
    url = API_URL.format(word)

    if VERBOSE:
        print url

    r = requests.get(url)
    j = json.loads(r.text)

    # return None if there are no noun synonyms
    if u'adjective' not in j or u'syn' not in j[u'adjective']:
        return None

    synonyms = j[u'adjective'][u'syn']
    n = N % len(synonyms)

    return synonyms[n]

def main(content):
    ''' content: String
    '''
    print content

    words = nltk.word_tokenize(content)
    tagged = nltk.pos_tag(words)

    if VERBOSE:
        print tagged

    for i, pair in enumerate(tagged):
        word, tag = pair
        # only substitute words that are nouns
        if tag == 'JJ' and word not in string.punctuation:
            new_word = lookup_word(word)
            if new_word != None:
                words[i] = new_word

    new_content = untokenize(words)
    print new_content

def untokenize(words):
    # sort of a hack

    result = ' '.join(words)
    for punc in string.punctuation:
        result = result.replace(' ' + punc, punc)

    return result


if __name__ ==  '__main__':
    parser = argparse.ArgumentParser(description='Play with synonyms.')
    parser.add_argument('file', help='file containing text')
    parser.add_argument('n', type=int, default=0, help='synonym number to choose')
    parser.add_argument('--verbose', "-v", action="store_true", help='verbosity')
    args = parser.parse_args()

    N = args.n
    VERBOSE = args.verbose

    f = open(args.file, 'r')
    content = f.read()
    f.close()

    main(content)
