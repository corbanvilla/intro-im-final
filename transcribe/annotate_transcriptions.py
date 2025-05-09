import os
import json
import string

def get_nltk_stopwords():
    try:
        from nltk.corpus import stopwords
    except ImportError:
        raise ImportError("Please install nltk: pip install nltk")
    try:
        stopwords.words('english')
    except LookupError:
        import nltk
        nltk.download('stopwords')
    return set(stopwords.words('english'))


def annotate_stopwords_in_json_dir(directory, stopwords=None):
    """
    Annotate each word in JSON files in the directory with 'is_stopword'.
    """
    if stopwords is None:
        stopwords = get_nltk_stopwords()
    for fname in os.listdir(directory):
        if fname.endswith('.json'):
            fpath = os.path.join(directory, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for entry in data:
                word = entry.get('text', '').strip(string.punctuation).lower()
                entry['is_stopword'] = word in stopwords
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Annotated stopwords in {fpath}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client/assets/transcripts"))
    annotate_stopwords_in_json_dir(directory)
