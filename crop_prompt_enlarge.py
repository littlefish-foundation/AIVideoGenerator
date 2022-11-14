import replicate
import mytoken
import os
import requests
from PIL import Image

# edit mytoken.py with your API TOKEN
# example: REPLICATE_API_TOKEN = "f77b55967be209bc63a12038af9c09e0d3211996"
# here we load the OS variable with the python variable token API id
os.environ['REPLICATE_API_TOKEN']=mytoken.REPLICATE_API_TOKEN

# load/show image from disk
filename = input("Enter existing filename (ex: image02.png): ")
while True:
    if os.path.isfile(filename):
        # when valid input given
        print(f'available filename is found: {filename}')
        break
    else:
        print("Please retry to enter a valid image filename that exist")
        filename = input("Enter existing filename image02.png: ")
        continue
print("")

# load/show image from disk
image = Image.open(filename)
# save the original image with the watermark, include size: image02_1024px_origin.png
#image.save("{0}_{1}px_origin.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("original file with watermark '{0}_{1}px_origin.{2}' written...".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("")
# remove watermark by removing 16px from all sides to preserve symmetry
# this will result in an image 992x992 instead of 1024x1024

image = image.resize((1056,1056))
image = image.crop((0+16,0+16,1024-16,1024-16))

# save the removed watermark original image: image02_1008px_nowatermark.png
image.save("{0}_{1}px_nowatermark.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("watermark removed '{0}_{1}px_nowatermark.{2}' written...".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("")

'''
# load image to prompt pre-trained model
model = replicate.models.get("methexis-inc/img2prompt")
# call the API and predict a result stored in output variable
# this will take many seconds ~50sec to finish calculating
print("Calculating image to prompt... 30 sec")
output = model.predict(image=open("{0}_{1}px_nowatermark.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]), "rb"))
#  removes any leading and trailing space characters
result = output.strip()
# store the image2prompt string to a text file: image02_prompt.txt
open("{0}_prompt.txt".format(filename.split('.')[0]), 'w').write(result)
print("image2prompt file '{0}_prompt.txt' written...".format(filename.split('.')[0]))
# print the result to the console
print("\tPrompt:\n", result, "\n")

'''

## upscale and de-noise the image
## load the swinir enlarge and denoise model
model = replicate.models.get("jingyunliang/swinir")
# load/show image from disk (same image)
print("Calculating image enlargement + denoise... 60 sec")
nowatermark = "{0}_{1}px_nowatermark.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1])
output = model.predict(image=open(nowatermark, "rb"),
                       task_type="Real-World Image Super-Resolution-Large",
                       noise=15,
                       jpeg=40)
r = requests.get(output, allow_redirects=True, stream=True)
image = Image.open(r.raw)
# save the upscaled image: image02_3968px_upscaled.png
image.save("{0}_{1}px_upscaled.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("enlarged file for video '{0}_{1}px_upscaled.{2}' written...".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("")

## resize the image to 1/3 or 33.3% of 1024 pixels ~341
## image = image.resize((341, 341))
# resize the image to 1/4 or 25% of 1024 pixels more centerable 256
image = image.resize((256, 256))
# save the lower sized result: image02_341px_downscaled.png
image.save("{0}_{1}px_downscaled.{2}".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("downscaled file for next DALLE-2 generation '{0}_{1}px_downscaled.{2}' written...".format(filename.split('.')[0], image.size[0], filename.split('.')[1]))
print("")
