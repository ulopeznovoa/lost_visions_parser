
from bs4 import BeautifulSoup
from rect_overlap import *
import sys
import os.path

#Some threshold values
CONSIDER_AS_BIG_AS_IMG_THRESHOLD=0.95
CONSIDER_OVERLAPPING_IMG_THRESHOLD=0.8

# Load the hOCR XML, either from command line or hardcoded variable
if (len(sys.argv)>1):
    if os.path.isfile(sys.argv[1]):
        file_path=sys.argv[1]
    else:
        print('ERROR: File not found')
        exit(-66)
else:
    file_path='/tmp/img41.xml'
    #file_path='/home/osboxes/Documents/Lost_visions/sandbox/img514.xml'

with open(file_path, 'r') as file:
    data = file.read().replace('\n', '')
soup = BeautifulSoup(data, 'lxml-xml')

# Compute the img area with the information from the parent div
parent_div = soup.find_all('div', attrs={"class": "ocr_page"})[0]
img_area_info = parent_div['title'].split(";")[1].split()

img_width = int(img_area_info[3]) - int(img_area_info[1])
img_height = int(img_area_info[4]) - int(img_area_info[2])
img_area = img_width * img_height

# This loop does two things:
# 1) If there is any div (bounding box) almost as big as the image, remove it
# 2) Find the largest
largest_bbox_area = 0
for p in soup.find_all('p', attrs={"class": "ocr_par"}):
    bbox = p['title'].split()
    bbox_width = int(bbox[3]) - int(bbox[1])
    bbox_height = int(bbox[4]) - int(bbox[2])
    bbox_area = bbox_width * bbox_height
    if bbox_area >= (img_area * CONSIDER_AS_BIG_AS_IMG_THRESHOLD):
        p.decompose()
    else:
        if(bbox_area > largest_bbox_area):
            largest_bbox_area = bbox_area
            largest_bbox_p = p

# Remove any bounding box overlapping with the largest one
bbox = largest_bbox_p['title'].split()
largest_bbox_rect = Rect(Point(int(bbox[1]), img_height - int(bbox[2])), Point(int(bbox[3]), img_height - int(bbox[4])))
for p in soup.find_all('p', attrs={"class": "ocr_par"}):
    if(p != largest_bbox_p):
        bbox = p['title'].split()
        rect = Rect(Point(int(bbox[1]), img_height - int(bbox[2])), Point(int(bbox[3]), img_height - int(bbox[4])))
        if Rect.overlap(largest_bbox_rect, rect):
            if (Rect.overlap_percent(largest_bbox_rect,rect) > CONSIDER_OVERLAPPING_IMG_THRESHOLD):
                p.decompose()


# Find the box beneath the largest one and get the caption
caption = ""
next = False
for p in soup.find_all('p', attrs={"class": "ocr_par"}):
    if(p == largest_bbox_p):
        next = True
    else:
        if next:
            for span in p:
                if(len(span) > 1):
                    for s in span:
                        caption += s.string

            if(len(caption) > 0):
                break
print(caption)
