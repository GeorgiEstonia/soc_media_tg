## What is this?
This project is an API that allows you to generate 3 images that describe what you write on Instagram.

## How does it work?
First, you call the API passing your Instagram handle as "message" parameter. 
Then, it scrapes the text from your most recent posts and determines the 3 most common topics using Latent Dirichlet allocation.
Further, it generates the most representative sentence for each topic and feeds them to Replicate implementation of Stable Diffusion, returning a list of 3 links to images that illustrate the topics of your Instagram.
