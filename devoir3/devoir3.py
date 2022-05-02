import os
import imageio.v2 as imageio
import numpy as np


directory = './lfw'
results_directory="./resultat/"
new_image = np.array([[[0] * 3] * 250] * 250)
folderNumber = 0
 
for folder in os.scandir(directory):
    if folder.is_dir():
        number_of_pictures = len([picture for picture in os.scandir(folder) if os.path.isfile(picture)])
        if number_of_pictures>=2:
            folderNumber+=1
            for picture in os.scandir(folder):
                image=imageio.imread(directory+"/"+folder.name+"/"+picture.name, pilmode='RGB')
                height=image.shape[0]
                width=image.shape[1]
                for h in range(height):
                    for w in range(width):
                        red_color = int(image[h][w][0])
                        green_color = int(image[h][w][1])
                        blue_color = int(image[h][w][2])
                        new_image[h][w][0]+=red_color
                        new_image[h][w][1]+=green_color
                        new_image[h][w][2]+=blue_color
            for sum_img_height in range(250):
                for sum_img_width in range(250):
                    avg_red_color = int((new_image[sum_img_height][sum_img_width][0])/number_of_pictures)
                    avg_blue_color = int((new_image[sum_img_height][sum_img_width][1])/number_of_pictures)
                    avg_green_color = int((new_image[sum_img_height][sum_img_width][2])/number_of_pictures)
                    new_image[sum_img_height][sum_img_width][0] = avg_red_color
                    new_image[sum_img_height][sum_img_width][1] = avg_blue_color
                    new_image[sum_img_height][sum_img_width][2] = avg_green_color
                
            image_name=str(results_directory+str(folderNumber)+"image.png")   
            imageio.imwrite(image_name, new_image)
            new_image = np.array([[[0] * 3] * 250] * 250)
            

