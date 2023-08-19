import markdown
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re

nltk.download('popular')

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def process_markdown(content):
    md = markdown.Markdown()
    html_text = md.convert(content)
    plain_text = re.sub('<[^<]+?>', '', html_text)
    
    return plain_text

def generate_summary(text, num_sentences=3):
    sentences = sent_tokenize(text)
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    freq_dist = FreqDist(words)
    sorted_freq = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)

    top_sentences = []
    for sentence in sentences:
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [word.lower() for word in sentence_words if word.isalnum()]
        sentence_words = [word for word in sentence_words if word not in stop_words]

        score = sum(freq_dist[word] for word in sentence_words)
        top_sentences.append((sentence, score))

    top_sentences.sort(key=lambda x: x[1], reverse=True)
    summary_sentences = [sentence for sentence, _ in top_sentences[:num_sentences]]

    return ' '.join(summary_sentences)