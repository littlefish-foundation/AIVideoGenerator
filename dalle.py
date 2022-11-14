import os
import openai
import mytoken
from PIL import Image
import requests
openai.organization = mytoken.AOPENAI_ORG
openai.api_key = mytoken.OPENAI_API_KEY
##openai.Model.list()


#defines
tmp_folder = 'tmp'
os.makedirs(tmp_folder, exist_ok=True)
# load/show image from disk
filename = input("Enter existing filename (ex: image02.png): ")
while True:
    if os.path.isfile(filename):
        # when valid input given
        print(f'available filename is found: {filename}')
        break
    else:
        print("Please retry to enter a valid image filename that exist:", os.path.isfile(filename))
        filename = input("Enter existing filename image02.png: ")
        continue
print("")

# load/show image from disk
image = Image.open(filename)
# save the original image with the watermark, include size: image02_1024px_origin.png
#image.save("{0}_{1}px_origin.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
#print("original file with watermark '{0}_{1}px_origin.{2}' written...".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
#print("")
# remove watermark by removing 16px from all sides to preserve symmetry
# this will result in an image 992x992 instead of 1024x1024

#image_cropped = image.crop((0+16,0+16,1024-16,1024-16))

#new_image = Image.new(mode="RGBA", size=(1024,1024))

#new_image.putalpha(0)
#image_cropped.resize((1056,1056))
#new_image.paste(image_cropped)

#image = image.resize((1056,1056))
#image = image.crop((0+16,0+16,1056-16,1056-16))




# save the removed watermark original image: image02_1008px_nowatermark.png

path_nowatermark = filename.split('.')[0] + "_no_watermark.png"

#image.save(os.path.join(tmp_folder, path_nowatermark))



print("Creating Mask...")

### here


#downscaled = Image.open("{0}_{1}px_nowatermark.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))

mask = Image.new(mode="RGBA", size=(1024,1024), color=(255,0,0,0))


image = image.resize((256,256))
#image512 == image.resize((512,512))


mask.putalpha(0)
mask.paste(image, (384,384))
path_mask = "{0}_{1}px_mask.{2}".format(filename.split('.')[0], mask.size[0], filename.split('.')[1])
mask.save(os.path.join(tmp_folder, path_mask))
print("mask '{0}' written...".format(path_mask))

print("")


print("Creating DALLE...")
print("with image: {0} and mask:{1}".format(path_nowatermark, path_mask))
print("")
print("")

samples = 10

prompt_input = input("Enter prompt: ")


res = openai.Image.create_edit(
  image=open(os.path.join(tmp_folder, path_mask), "rb"),
  mask=open(os.path.join(tmp_folder, path_mask), "rb"),
  prompt=prompt_input,
  n=samples,
  size="1024x1024"
)


image_folder = 'Dall-e'

os.makedirs(image_folder, exist_ok=True)

for(i, image) in enumerate(res['data']):
    print("Downloading image {0} of {1}".format(i+1, samples))
    # save the generated image: image02_1024px_generated.png
    path_generated = "{0}_sample_{1}_{2}.png".format(filename.split('.')[0], i+1, image['url'].split('/')[-1])
    r = requests.get(image['url'], stream=True)
    with open(os.path.join(image_folder, path_generated), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    print("generated image '{0}' written...".format(path_generated))
    print("")
    print("")

     


# image_url = res['data'][0]['url']

def download_image(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


#download_image(image_url)




print("Done..")
