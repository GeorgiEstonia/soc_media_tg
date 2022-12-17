import scraper
import data_cleaner
import lda
import sd
import twitter_scraper
from flask import Flask, jsonify, request
import twitter_scraper

from flask_cors import cross_origin

#from six.moves import http_client

app = Flask(__name__)

def twitter_to_pics(handle="elonmusk"):

    #twitter scraper
    return


def insta_to_pics(instagram_username="georgi.so"):

    # scraper instance
    scraper_inst = scraper.Scraper(instagram_username)
    instagram_data = scraper_inst.continuous_run() 
    #instagram_data = scraper_inst.test_method_no_API() # test function

    # data cleaner instance
    data_cleaner_inst = data_cleaner.DataCleaner()
    #cleaned_data = sample_texts # for testing
    cleaned_data = data_cleaner_inst.get_text_from_insta(instagram_data) # uncoment in prod
    formatted_data = data_cleaner_inst.remove_stuff(cleaned_data)

    # LDA instance
    lda_inst = lda.LDA(formatted_data)
    model, corpus = lda_inst.build_model()
    sentences = lda_inst.format_topics_sentences(model, corpus)

    # Stable Diffusion
    sd_inst = sd.SD(sentences)
    print(sd_inst.gen_imgs_api())
    return sd_inst.gen_imgs_api()
    #return ['https://replicate.delivery/pbxt/y7R1d2I0UbY1PZe7z5r1KTbdez9rZ5Dnj6luOYPmbrmKGdCQA/out-0.png', 'https://replicate.delivery/pbxt/SL3lAmCgkfQfKUz1Bp798sKHtlSR0UfF0je9frw8E5fCkRnAE/out-0.png', 'https://replicate.delivery/pbxt/3DWH0ORTeTyZaqGFOIwXFOkkR2bT7Qa9kuzLP86e570VGdCQA/out-0.png']

def twitter_to_pics(twitter_handle="elonmusk"):

    # scraper instance
    ts = twitter_scraper.TwitterSceaper("elonmusk")
    tweet_data = ts.get_tweets()
    print(tweet_data)

    # data cleaner instance
    data_cleaner_inst = data_cleaner.DataCleaner()
    formatted_data = data_cleaner_inst.remove_stuff(tweet_data)

    # LDA instance
    lda_inst = lda.LDA(formatted_data)
    model, corpus = lda_inst.build_model()
    sentences = lda_inst.format_topics_sentences(model, corpus)

    # Stable Diffusion
    sd_inst = sd.SD(sentences)
    print(sd_inst.gen_imgs_api())
    return sd_inst.gen_imgs_api()

@app.route('/')
def test():
    return jsonify({"message": "Hey! The API is working :)"})


# entry point for instagram scraping
@app.route('/echo', methods=['POST', 'GET'], endpoint='echo2')
def echo2():
    message = request.get_json().get('message', '')
    print(f"message: {message}")
    
    #pics_test = ['https://replicate.delivery/pbxt/y7R1d2I0UbY1PZe7z5r1KTbdez9rZ5Dnj6luOYPmbrmKGdCQA/out-0.png', 'https://replicate.delivery/pbxt/SL3lAmCgkfQfKUz1Bp798sKHtlSR0UfF0je9frw8E5fCkRnAE/out-0.png', 'https://replicate.delivery/pbxt/3DWH0ORTeTyZaqGFOIwXFOkkR2bT7Qa9kuzLP86e570VGdCQA/out-0.png']
    #return "hi"
    #return jsonify({"pictures": pics_test})
    #return jsonify({"pictures": insta_to_pics(message)})
    return jsonify({"pictures": twitter_to_pics(message)})


# entry point for twitter sceaping
#@app.route('/twitter', methods=['POST', 'GET'])
#def twitter():
#    message = request.get_json().get('message', '')
#    print(f"message: {message}")
#    return jsonify({"pictures": insta_to_pics(message)})

if __name__ == "__main__":
    app.run()

#@app.errorhandler(http_client.INTERNAL_SERVER_ERROR)
#def unexpected_error(e):
#    """Handle exceptions by returning swagger-compliant json."""
#    logging.exception('An error occured while processing the request.')
#    response = jsonify({
#        'code': http_client.INTERNAL_SERVER_ERROR,
#        'message': 'Exception: {}'.format(e)})
#    response.status_code = http_client.INTERNAL_SERVER_ERROR
#    return response