import scraper
import data_cleaner
import lda
import sd
from flask import Flask, jsonify, request
import logging

from flask_cors import cross_origin

#from six.moves import http_client

app = Flask(__name__)


def insta_to_pics(instagram_username="georgi.so"):

    # scraper instance
    scraper_inst = scraper.Scraper(instagram_username)
    instagram_data = scraper_inst.continuous_run() # Uncoment when in prod
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


@app.route('/echo', methods=['POST'])
def echo():
    message = request.get_json().get('message', '')
    return jsonify(insta_to_pics(message))

#@app.errorhandler(http_client.INTERNAL_SERVER_ERROR)
#def unexpected_error(e):
#    """Handle exceptions by returning swagger-compliant json."""
#    logging.exception('An error occured while processing the request.')
#    response = jsonify({
#        'code': http_client.INTERNAL_SERVER_ERROR,
#        'message': 'Exception: {}'.format(e)})
#    response.status_code = http_client.INTERNAL_SERVER_ERROR
#    return response