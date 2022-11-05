# import torch
# from torch import autocast
# from diffusers import StableDiffusionPipeline
import random
from decouple import config 

# stuff for API based generation
import os
import replicate
os.environ["REPLICATE_API_TOKEN"] = config('replicate_key', default="")

class SD():
    def __init__(self, sentences):
        self.sentences = sentences


    #def generate_images(self):
    #    """
    #    This function was supposed to generate images directly with stable diffusion but then Robert explained that my GPU won't handle it even on low settings. 
    #    """
    #    model_id = "CompVis/stable-diffusion-v1-4"
    #    device = "cuda"
    #    token = config('hf_key', default="")
#
    #    #fp16 - weak GPU settings
    #    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=token)
    #    pipe = pipe.to(device)
#
    #    for sentence in self.sentences:
    #        with autocast("cuda"):
    #            image = pipe(sentence, guidance_scale=7.5).images[0]  
#
    #        #Now to display an image you can do either save it such as:
    #        image.save(f"sd_{sentence[0]}_{random.randint(100, 999)}.png")

    def gen_imgs_api(self):
        model = replicate.models.get("stability-ai/stable-diffusion")
        images = []
        print("Starting stable diffusion")
        for sentence in self.sentences:
            print(f"Processing {sentence}")
            limit = 0
            img = None
            # if there is an error (e.g., NSFW content, run again)
            while not img:
                print(f"Limit = {limit}")
                img = model.predict(prompt=sentence)[0]
                limit += 1
                if limit > 3:
                    break
            
            # append error img if no img
            if img:
                images.append(img)
            else:
                images.append("https://learn.microsoft.com/es-es/windows/win32/uxguide/images/mess-error-image15.png")
        return images


# Test
# sentences = ['zero day exploits among dangerous types', 'meet new pixel pixel pro advanced', 'google pixel phone watch buds work']
# test = SD(sentences)
# print(test.gen_imgs_api())