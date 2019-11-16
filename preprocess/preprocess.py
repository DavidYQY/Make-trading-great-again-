#!/usr/bin/env python
import re, json, emoji
from twokenize import tokenizeRawTweetText
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

URL_PATTERN = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
HASHTAG_PATTERN = re.compile(r'#\w*')
MENTION_PATTERN = re.compile(r'@\w*')
RESERVED_WORDS_PATTERN = re.compile(r'^(RT|FAV)')
STOPWORDS = set(stopwords.words('english'))

# Sort emojis by length to make sure mulit-character emojis are matched first
emojis = sorted(emoji.unicode_codes.EMOJI_UNICODE.values(), key=len, reverse=True)
EMOJIS_PATTERN = re.compile(u'(' + u'|'.join(re.escape(u) for u in emojis) + u')')

"""
try:
    # UCS-4
    EMOJIS_PATTERN = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
except re.error:
    # UCS-2
    EMOJIS_PATTERN = re.compile(
        u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
"""
SMILEYS_PATTERN = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", re.IGNORECASE)
NUMBERS_PATTERN = re.compile(r"(^|\s)(\-?\d+(?:\.\d)*|\d+)")
NUMBERS_WITH_COMMA = re.compile(r"(?:(?<!\d)\d{1,3},)+?\d{3}" + r"(?=(?:[^,\d]|$))")

def preprocessing(text):
    # clean MENTION (@someone), number (28,000)
    text = MENTION_PATTERN.sub("", text)
    text = NUMBERS_WITH_COMMA.sub("", text)
    text = NUMBERS_PATTERN.sub("", text)

    words = tokenizeRawTweetText(text)

    new_words = []

    # normalize
    lemmatizer = WordNetLemmatizer()
    for word in words:
        # Remove non-ASCII characters from list of tokenized words
        if (re.match(EMOJIS_PATTERN, word) != None):
            new_word = word
        elif (re.match(HASHTAG_PATTERN, word) != None):
            new_word = word
        elif(re.match(URL_PATTERN, word) != None):
            new_word = ""
        else:
            # Remove punctuation from list of tokenized words
            new_word = re.sub(r'[^\w\s]', '', word)
            # Convert all characters to lowercase from list of tokenized words
            new_word = new_word.lower()

        # Remove stop words from list of tokenized words
        if new_word != '' and new_word not in STOPWORDS:
            # lemmatization
            new_words.append(lemmatizer.lemmatize(new_word))
    return new_words

if __name__ == '__main__':
    with open('trumptwitterarchive.txt', 'r') as data_file:
        json_data = data_file.read()

    data = json.loads(json_data)

    for twitter in data:
        tokenized_text = tokenizeRawTweetText(twitter['text'])
        processed_text = preprocessing(twitter['text'])
        twitter['tokenized_text'] = tokenized_text
        twitter['processed_text'] = processed_text

    with open('processed_trumptwitterarchive.txt', 'w') as outfile:
        json.dump(data, outfile)

