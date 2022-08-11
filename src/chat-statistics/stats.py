import json
from collections import Counter
from importlib.resources import path
from pathlib import Path
from typing import Union

import arabic_reshaper
# from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from src.data import DATA_DIR
from wordcloud import WordCloud


class chatstatistics:
    def __init__(self, chat_json: Union[str, path]):
        with open(chat_json) as f:
            self.chat_data = json.load(f)
        self.normalizer = Normalizer()
        stopwords = open(DATA_DIR / 'stopwords.txt').readlines()
        stopwords = list(map(str.strip, stopwords))
        stopwords = list(map(self.normalizer.normalize, stopwords))


    def generate_word_cloud(self, output_dir: Union[str, path]):
        text_content = ''
        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list (filter(lambda item: item not in self.stopwords, tokens))
                text_content += f" {' '.join(tokens)}"
        
        text_content = self.normalizer.normalize(text_content)
        # Counter(word_tokenize(text_content)).most_common()
        wordcloud = WordCloud(
            font_path = DATA_DIR / 'B Homa_YasDL.com.ttf',
            background_color='white').generate(text_content)
        
        wordcloud.to_file(path(output_dir)/ 'wordcloud.png')
        
        
            
if __name__ == "__main__":
    chat_stats = chatstatistics(chat_json= DATA_DIR / 'result.json' )
    chat_stats.generate_word_cloud(output_dir= DATA_DIR)
    
print('done!')

             