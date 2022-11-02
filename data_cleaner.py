import re
import numpy
import nltk
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess

class DataCleaner():

    def __init__ (self):
        print("Init")

    def get_text_from_insta(self, instagram_data):
        """
        Extracts text from instagram post raw JSON.        
        """
        processed_posts = []
        for i in range(len(instagram_data)):
            text = instagram_data[i]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            text.replace("\n", "")
            processed_posts.append(text)
        
        return processed_posts


    def sent_to_words(self, sentences):
        for sentence in sentences:
            # deacc=True removes punctuations
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def remove_stopwords(self, texts, stop_words):
        return [[word for word in simple_preprocess(str(doc)) 
                if word not in stop_words] for doc in texts]

    def remove_stuff(self, data):
        """removes punctuation, stopwords, capitalization"""
        # Convert the titles to lowercase
        data = [x.lower() for x in data]
        # Remove punctuation
        for i in range(len(data)):
            data[i] = re.sub('[,\.!?]', '', data[i])

        # VM might need stopwords downloaded manually?
        nltk.download("stopwords")

        stop_words = stopwords.words('english') + stopwords.words('spanish') + stopwords.words('russian')

        data_words = list(self.sent_to_words(data))
        
        
        # remove stop words
        data = self.remove_stopwords(data_words, stop_words)


        return data

                

    def test_output(self):
        # TODO delete later
        print("test output")

lil_test = DataCleaner()
text = ["adah  AJKDHAdhajsdh and hello he stop a A akk a ,, ! :)", "Hello there!", "Anot ! Ajk na na nn kk", ""] 
new_text = lil_test.remove_stuff(text)
print(new_text)