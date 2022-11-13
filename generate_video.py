import replicate
import mytoken
import os
import requests
import glob
import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# get all upscaled images and sort by numeric value
upscaled_image_files = glob.glob("image0*.png")
upscaled_image_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
# upscaled_image_files

for idx, upscaled_image in enumerate(upscaled_image_files):
    print("starting new batch of images")

    # load in the upscaled image one-at-a-time
    image = Image.open(upscaled_image)

    # parameters HD video 60 fps used for images crop and scale
    video_resolution_width  = 992   # 1280 
    video_resolution_height = 558   # 720
    fps = 50           # 60
    seconds_image = 3  # 6
    upscaled_image_width  = 3968
    upscaled_image_height = 3968
    nr_of_crops = fps * seconds_image
    image_folder = 'images'
    video_name = 'finalvideo.mp4'
    
    # left 1/4
    left_min = int((upscaled_image_width/2)-(video_resolution_width/2))
    left = [int(x/100) for x in range(left_min*100, -1, -int((left_min/(nr_of_crops-1))*100))]
    
    # upper 2/4
    upper_min  = int((upscaled_image_height/2)-(video_resolution_height/2))
    new_height = int((video_resolution_height/video_resolution_width)*upscaled_image_height)
    upper_max  = int((upscaled_image_height/2)-(new_height/2))
    upper = [int(x/100) for x in range(upper_min*100, int(upper_max*100)-1, -int((upper_min-upper_max)/(nr_of_crops-1)*100))]
    
    # right 3/4
    right_min = int((upscaled_image_width/2)+(video_resolution_width/2))
    right_max = int(upscaled_image_width)
    right = [int(x/100) for x in range(right_min*100, int(right_max*100)+1, int((right_max-right_min)/(nr_of_crops-1)*100))]
    
    # lower 4/4
    lower_min = int((upscaled_image_height/2)-(video_resolution_height/2)+video_resolution_height)
    lower_max = int((upscaled_image_height/2)+(new_height/2))
    lower = [int(x/100) for x in range(lower_min*100, int(lower_max*100)+1, int((upper_min-upper_max)/(nr_of_crops-1)*100))]
    
    # transpose all list data into a list of tuples with size 4 for the amount of images coordinate values
    image_coordinates = [(left[x+2], upper[x+2], right[x+2], lower[x+2]) for x in range(nr_of_crops-2)]
    
    # create/check a folder
    os.makedirs(image_folder, exist_ok=True)

    # create the images inside the folder
    for img_number in range(nr_of_crops-4):
        cropped_image = image.crop(image_coordinates[img_number])
        cropped_image.resize((1280, 720)).save(image_folder + "/movieImg_{0}.png".format(img_number+(idx*nr_of_crops)))
        print("cropped and rescaled image 'movieImg_{0}.png' written ({1}x{2}) - step {3}/{4}".format((img_number+(idx*nr_of_crops)), 1280, 720, (img_number+1)+(nr_of_crops*idx), nr_of_crops*len(upscaled_image_files)))

# get all the generated images *.png from the <image/> folder, sorted by numeric value
image_files = glob.glob(image_folder + "/movieImg_*.png")
image_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile(video_name, fps=50)