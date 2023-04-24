import argparse
import json
import math
import os
from tqdm import tqdm

# JUST CHANGE LINE 6, VALUES: 'val' or 'train'
parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, required=True)
args = parser.parse_args()
FILE_TYPE = args.type
# CAN CHANGE SAVE_PATH STRING
SAVE_PATH = f'data/labels/{FILE_TYPE}'

def give_new_format(box, width, height):
    return [
        (box[0]+math.floor(box[2]/2))/width,
        (box[1]+math.floor(box[3]/2))/height,
        box[2]/width, 
        box[3]/height
    ]


with open(f'data/images/{FILE_TYPE}/_annotations.coco.json', 'r') as f:
    data = json.load(f)
    cat = data['categories']
    images = data['images']
    ann = data['annotations']

    # sample item, this is supposed to be performed on a for-loop
    annotations = data['annotations']

    for item in tqdm(annotations, desc="Annotation data per image"):
        cat_id = item['category_id']

        # get the filename of item used list for future reference in case of repeating ids
        img_dict = [file for file in images if file.get('id') == item['image_id']]

        img_dict = img_dict[0]
        # get filename and remove '.jpg'
        filename = img_dict['file_name'][:-4]
        img_width = img_dict['width']
        img_height = img_dict['height']

        # manipulate bbox of json file to right format
        box = item['bbox']

        # bbox format changes, need to add an extra check
        bbox_contains_num = isinstance(box[0],int) or isinstance(box[0],float)
        bbox_contains_list = isinstance(box[0], list)

        # change bbox x and y and normalize values based on width and height
        new_box = []
        if bbox_contains_num:
            new_box.append(give_new_format(box, img_width, img_height))
        # elif bbox_contains_list:
        #     for b in box:
        #         new_box.append(give_new_format(b, img_width, img_height))
        else: 
            raise Exception('Improper bbox format!')
        
        # make a new txt file that will store needed data
        with open(f'{SAVE_PATH}/{filename}.txt', 'a' if os.path.isfile(f'{SAVE_PATH}/{filename}.txt') else 'w') as f:
            # Write some text to the file
            for nb in new_box:
                f.write(f'{cat_id} {nb[0]} {nb[1]} {nb[2]} {nb[3]}\n')