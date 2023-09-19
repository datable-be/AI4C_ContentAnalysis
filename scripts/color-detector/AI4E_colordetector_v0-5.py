# alternative with much faster extcolors module to reduce and define colors
# try with HSV color for better color detection?

import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import extcolors
import json


# STEP 0
# Set variables
path = 'examples/M.PL.0055.01.jpg'  #path to image
path_foreground = 'grabcutresult.png' #temp file with removed background
bckgrclr = (0,0,0) #background color temp file
tolerance = 10  #grouping of detected colors (smaller is better, but slower)
threshold = 5  #minimal percentage of color in image
objectdetect = 'Y' # apply objectdetection ('Y') or jump to step 3 ('')

# read image
image = cv.imread(path)
print('Start processing ',path)
print('Reducing file size')
# resize image with smallest dimension = 200 px
if image.shape[1] < image.shape[0]:
    scale_factor = 200 / image.shape[1]
else:
    scale_factor = 200 / image.shape[0]
W = int(image.shape[1] * scale_factor)
H = int(image.shape[0] * scale_factor)
dim = (W , H)

image = cv.resize(image, dim, interpolation = cv.INTER_LINEAR)

# STEP 1
# Detect objects if objectdetect = TRUE
if objectdetect == 'Y':
    print('Step 1: Detecting objects...')
    h = image.shape[0]
    w = image.shape[1]

    # path to the weights and model files
    weights = 'ssd_mobilenet/frozen_inference_graph.pb'
    model = 'ssd_mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'

    # load the MobileNet SSD model trained  on the COCO dataset
    net = cv.dnn.readNetFromTensorflow(weights, model)

    # load the class labels the model was trained on
    class_names = []
    with open('ssd_mobilenet/coco_names.txt', 'r') as f:
        class_names = f.read().strip().split('\n')

    # create a blob from the image
    blob = cv.dnn.blobFromImage(
        image, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
    # pass the blog through our network and get the output predictions
    net.setInput(blob)
    output = net.forward()  # shape: (1, 1, 100, 7)

    # make list of detected objects
    objects = []
    boxes = []

    # loop over the number of detected objects
    for detection in output[0, 0, :, :]:  # output[0, 0, :, :] has a shape of: (100, 7)
        # the confidence of the model regarding the detected object
        probability = detection[2]

        # if the confidence of the model is lower than 20%,
        # we do nothing (continue looping)
        if probability < 0.2:
            continue
        
        # perform element-wise multiplication to get
        # the (x, y) coordinates of the bounding box
        box = [int(a * b) for a, b in zip(detection[3:7], [w, h, w, h])]
        box = tuple(box)

        # calculate box size
        width = box[2] - box[0]
        height = box[3] - box[1]
        size = width * height
        
        # extract the ID of the detected object to get its name
        class_id = int(detection[1])

        # get the object label
        label = f'{class_names[class_id - 1].upper()}'
        print('detected: label: ',class_id,label)

        # add size to object to sublist
        detected_object = [size,box,label]

        # add to nested list
        objects.append(detected_object)

    # filter to keep only the biggest detected object
    biggest_object = max(objects)

    box = biggest_object[1]
    print('box of biggest object detected: ',box,' (',label,')')

    # STEP 2
    # remove background
    print('\nStep 2: Removing background...')

    # read box coordinates
    x = box[0]
    y = box[1]
    x2 = box[2]
    y2 = box[3]
    w = x2 - x
    h = y2 - y

    # create mask
    mask = np.zeros(image.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    # define box with object
    rect = (x, y, w, h)

    # remove background
    cv.grabCut(image,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    image = image*mask2[:,:,np.newaxis]

    foreground_img = image.copy()
    foreground_img[np.where((mask2==0))] = np.array([0,0,0]).astype('uint8') #this allows you to change the background color after grabcut

    # temp write image without backgound
    cv.imwrite(path_foreground, foreground_img)
    print('image background removed, foreground image written to /', path_foreground)

else:
    print('Step 1: no object detection applied...')
    print('\nStep 2: no background removal. Whole image will be analysed...')
    cv.imwrite(path_foreground, image)



# STEP 3
# Get main colors
print('\nStep 3: Searching main colors...')

detected_colors, pixel_count = extcolors.extract_from_path(path_foreground, tolerance = tolerance) # no limit set, this will be done after grouping

detected_colors = pd.DataFrame(detected_colors)   #convert to pd dataframe
detected_colors.columns = ['rgb','pixels']  #add column headers

# remove (0,0,0) bckgr color
detected_colors = detected_colors[~(detected_colors['rgb'] == (0, 0, 0))]

print('detected colors in foreground object:\n',detected_colors)

# STEP 4
# Match colors with EFT colors
# can be optimised by transforming to HSV color model
# (e.g. to avoid overrepresentation of gray color)
print('\nStep 4: Matching colors with EFT...\n')


#Reading csv file with pandas and giving names to rgb values
index=['color','color_name','hex','R','G','B','RGB','note']
csv = pd.read_csv('EFHAcolors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(rgb):
    R, G, B = rgb
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,'R'])) + abs(G- int(csv.loc[i,'G']))+ abs(B- int(csv.loc[i,'B']))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,'color_name']
    return cname


detected_colors['colorname'] = detected_colors['rgb'].apply(getColorName)
print(detected_colors)


# STEP 4b: merging identical color names
print('\nMerging colors and calculating percentages...\n')

#define how to aggregate various fields
agg_functions = {'pixels': 'sum'}
detected_colors_grouped = detected_colors.groupby(detected_colors['colorname']).aggregate(agg_functions)                     #group colors
detected_colors_grouped['percentage'] = (detected_colors_grouped['pixels'] / detected_colors_grouped['pixels'].sum()) * 100   #calculate percentage
print(detected_colors_grouped)

# STEP 4c: apply threshold to remove marginal colors
print('\nApplying threshold of',threshold,'%...\n')

detected_colors_grouped = detected_colors_grouped[detected_colors_grouped.percentage > threshold]
print(detected_colors_grouped)

# STEP 4d: add EFT URI
# todo...

# STEP : convert to json
detected_colors_json = detected_colors_grouped.to_json(orient='columns' )
print(type(detected_colors_json))
print(detected_colors_json)
with open("detected_colors_json.json", "w") as write_file:
    json.dump(detected_colors_json[0], write_file, indent=4)


print('\nFinished analysing ',path)
