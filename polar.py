#!/usr/local/bin/python3


from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import math
import numpy as np

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)

    filters.sobel(grayscale,0,filtered_y)

    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)




# Function to find the Boundaries through viterbi algorithm

def viterbi(image_array, edge_strength):

    viterbi_list = []

    viterbi_dict = {}

    # Here the probability values of the first column is calculated and appended in viterbi_dict

    for i in range(len(image_array)):

        viterbi_dict[i] = []

        if(image_array[i][0] == 0):
            viterbi_dict[i].append(0)
            viterbi_dict[i].append(0)

        else:

            viterbi_dict[i].append(edge_strength[i][0]/image_array[i][0])
            viterbi_dict[i].append(0)

    viterbi_list.append(viterbi_dict)

    # Looping through the rest of the columns the max probability is calculated for each pixel considering the transition and emission values

    for i in range(1,image_array.shape[1]):

        viterbi_dict = {}

        prev_dict = viterbi_list[i-1]
        
        for j in range(len(image_array)):


            cell_level_dict = {}
            
            for k in range(len(image_array)):

                # Here a threshold of 3 pixel above and below the current pixel is considered to get a continuous line without
                # being discrete

                if(abs(k-j) <= 3):

                    d = 1/((abs(k-j)+1)*2)

                    if(prev_dict[k][0] == 0 or image_array[j][i] == 0):

                        cell_level_dict[k] = 0
                    else:

                        cell_level_dict[k] =  prev_dict[k][0]*(edge_strength[j][i]/image_array[j][i])*d

            max_lev = dict(sorted(cell_level_dict.items(), key=lambda x:x[1], reverse = True))

            # The maximium value of each pixel is taken and also the transition pixel column number from which we get the high value

            cell_prob = cell_level_dict[list(max_lev.keys())[0]]

            prev_cell = list(max_lev.keys())[0]



            viterbi_dict[j] = []
            viterbi_dict[j].append(cell_prob)
            viterbi_dict[j].append(prev_cell)

        viterbi_list.append(viterbi_dict)



    final = []

    k = dict(sorted(viterbi_list[len(viterbi_list)-1].items(), key=lambda x:x[1][0], reverse = True))

    
    final.append(list(k.keys())[0])
    final.append(list(k.values())[0][1])

    current_node = final[1]

    
    # Backtracking is done from the last pixel columns 

    for each in range(len(viterbi_list)-1,0,-1):

        if(each == len(viterbi_list)-1):
            continue
        
        else:

            current_node = viterbi_list[each][current_node][1]

            final.append(current_node)

    # Backtracked elements are reversed 

    final.reverse()

    new_list = [x+1 for x in final]

    return new_list


# Function to perform viterbi from the coorinates provided

def viterbi_dict_back(viterbi_dict,point,i,edge_strength,image_array):

    viterbi_dict[i] = []

    if(i == point[1]-1):
        viterbi_dict[i].append(edge_strength[i][point[0]-1]/image_array[i][point[0]-1])
        viterbi_dict[i].append(0)
    else:
        viterbi_dict[i].append(0)
        viterbi_dict[i].append(0)

    return viterbi_dict

# Function to perform before the coordinates points provided

def viterbi_dict_front(viterbi_dict,point,i,edge_strength,image_array):

    viterbi_dict[i] = []

    if(image_array[i][0] == 0):
        viterbi_dict[i].append(0)
        viterbi_dict[i].append(0)

    else:

        viterbi_dict[i].append(edge_strength[i][0]/image_array[i][0])
        viterbi_dict[i].append(0)

    return viterbi_dict


# Function to perform viterbi with human feedback


def viterbi_with_feedback(image_array, edge_strength,point,plot):

    viterbi_list = []

    viterbi_dict = {}

    for i in range(len(image_array)):

    
        if(plot == 2):
            
            viterbi_dict = viterbi_dict_back(viterbi_dict,point,i,edge_strength,image_array)

        else:

            viterbi_dict = viterbi_dict_front(viterbi_dict,point,i,edge_strength,image_array)
            

        

    viterbi_list.append(viterbi_dict)

    index = 0

    if(plot == 2):

        x = point[0]
        y = image_array.shape[1]
    
    else:

        x = 1
        y = point[0]-1


    for i in range(x,y):
        

        viterbi_dict = {}

        prev_dict = viterbi_list[index]
        
        for j in range(len(image_array)):


            cell_level_dict = {}
            
            for k in range(len(image_array)):

                # A threshold of 3 pixels above and below is only considered for more smoothness of the line.

                if(abs(k-j) <= 3):

                    d = 1/((abs(k-j)+1)*2)

                    if(prev_dict[k][0] == 0 or image_array[j][i] == 0):

                        cell_level_dict[k] = 0
                    else:

                        cell_level_dict[k] =  prev_dict[k][0]*(edge_strength[j][i]/image_array[j][i])*d

            max_lev = dict(sorted(cell_level_dict.items(), key=lambda x:x[1], reverse = True))

            cell_prob = cell_level_dict[list(max_lev.keys())[0]]

            prev_cell = list(max_lev.keys())[0]



            viterbi_dict[j] = []
            viterbi_dict[j].append(cell_prob)
            viterbi_dict[j].append(prev_cell)

        viterbi_list.append(viterbi_dict)

        index +=1



    final = []

    k = dict(sorted(viterbi_list[len(viterbi_list)-1].items(), key=lambda x:x[1][0], reverse = True))


    if(plot == 2):
    
        final.append(list(k.keys())[0])
        final.append(list(k.values())[0][1])


    else:

        final.append(point[1]+2)
        final.append(k[point[1]+2][1])

    current_node = final[1]

    # Backtracking is done to get the list of elements.


    for each in range(len(viterbi_list)-1,0,-1):

        if(each == len(viterbi_list)-1):
            continue
        
        else:

            current_node = viterbi_list[each][current_node][1]

            final.append(current_node)


    final.reverse()

    new_list = [x+1 for x in final]

    return new_list


# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]


    gt_airice.reverse()
    gt_icerock.reverse()


    # load in image 
    input_image = Image.open(input_filename).convert('RGB')

    image_array = array(input_image.convert('L'))

    
    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)


    find_dict = {}
    min_value = min([ edge_strength[i][0] for i in range(edge_strength.shape[0])])

    # For better prediction through the simple bayes net method the first index and the second index of the two boundaries are taken

    for i in range(edge_strength.shape[0]):

        find_dict[i] = edge_strength[i][0]/image_array[i][0]


    select_bound =  dict(sorted(find_dict.items(), key=lambda x:x[1], reverse = True))
    select_list = list(select_bound.keys())
    first_set = select_list[0]

    for each in select_list:

        if(abs(each - first_set) >= 10):
            second_set = each
            break


    order = [first_set, second_set]


    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.


    air_ice_list = []

    ice_bedrock_list = []

    value_1 = 0
    value_2 = 0

    bound_min = min(order)
    bound_max = max(order)

    # Both the air-ice and ice-bedrock boundaries are found using the simple bayes net method here
    

    for i in range(image_array.shape[1]):
        
        tot_min_1 = edge_strength[0][i]/image_array[0][i]
        tot_min_2 = edge_strength[0][i]/image_array[0][i]


        for j in range(image_array.shape[0]):


            if(abs(j - bound_min) < 10):

                if(edge_strength[j][i]/image_array[j][i] > tot_min_1):

                    if(i == 0 or (abs(j - air_ice_list[-1]) < 10)):

                        value_1 = j+1
                        tot_min_1 = edge_strength[j][i]/image_array[j][i]

            elif(abs(j - bound_max) < 10):

                if(edge_strength[j][i]/image_array[j][i] > tot_min_2):

                    if(i == 0 or (abs(j - ice_bedrock_list[-1]) < 10)): 

                        value_2 = j+1
                        tot_min_2 = edge_strength[j][i]/image_array[j][i]


        
        air_ice_list.append(value_1)
        ice_bedrock_list.append(value_2)

        bound_min = value_1
        bound_max = value_2

    
    vit_array = [[0 for j in range(image_array.shape[1])] for i in range(image_array.shape[0])]

    vit_edge = [[0 for j in range(image_array.shape[1])] for i in range(image_array.shape[0])]


    
    viterbi_output_1 = viterbi(image_array, edge_strength)


    for i in range(image_array.shape[1]):

        for j in range(image_array.shape[0]):

            if(j > (viterbi_output_1[i] - 1)+11):

                vit_array[j][i] = image_array[j][i]

                vit_edge[j][i] = edge_strength[j][i]

    viterbi_output = viterbi(array(vit_array), array(vit_edge))

    # Function calls performe viterbi using human feedback 


    feetback_output_front_1 = viterbi_with_feedback(image_array, edge_strength, gt_airice,1)
    feetback_output_1 = viterbi_with_feedback(image_array, edge_strength, gt_airice,2)

    
    feetback_output_front_2 = viterbi_with_feedback(array(vit_array), array(vit_edge), gt_icerock,1)
    feetback_output_2 = viterbi_with_feedback(array(vit_array), array(vit_edge), gt_icerock,2)    

    feedback_first = feetback_output_front_1 + feetback_output_1
    feedback_second = feetback_output_front_2 + feetback_output_2


    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, air_ice_list, viterbi_output_1, feedback_first, gt_airice)
    write_output_image("ice_rock_output.png", input_image, ice_bedrock_list, viterbi_output, feedback_second, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (air_ice_list, viterbi_output_1, feedback_first, ice_bedrock_list, viterbi_output, feedback_second):
            fp.write(str(i) + "\n")
