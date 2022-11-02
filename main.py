import scraper
import data_cleaner
import lda
import sd

instagram_username = "georgi.so"

# scraper instance
scraper_inst = scraper.Scraper(instagram_username)
#instagram_data = scraper_inst.continuous_run() # Uncoment when in prod
instagram_data = scraper_inst.test_method_no_API() # test function

# data cleaner instance
data_cleaner_inst = data_cleaner.DataCleaner()
cleaned_data = data_cleaner_inst # TODO remove
#cleaned_data = data_cleaner_inst.get_text_from_insta(instagram_data) # uncoment in prod
formatted_data = data_cleaner_inst.remove_stuff(cleaned_data)

# LDA instance
lda_inst = lda.LDA(formatted_data)
model, corpus = lda_inst.build_model()
sentences = lda_inst.format_topics_sentences(model, corpus)

# Stable Diffusion
sd_inst = sd.SD(sentences)
sd_inst.generate_images()