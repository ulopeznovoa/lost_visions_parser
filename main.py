
from bs4 import BeautifulSoup
from rect_overlap import *

# Load the hOCR XML
with open('/home/osboxes/Documents/Lost_visions/sandbox/test005.xml', 'r') as file:
    data = file.read().replace('\n', '')
soup = BeautifulSoup(data, 'lxml-xml')

# Compute the img area with the information from the parent div
parent_div = soup.find_all('div', attrs={"class": "ocr_page"})[0]
img_area_info = parent_div['title'].split(";")[1].split()

img_width = int(img_area_info[3]) - int(img_area_info[1])
img_height = int(img_area_info[4]) - int(img_area_info[2])
img_area = img_width * img_height

# This loop does two things:
# 1) If there is any div (bounding box) as 95% big as the image, remove it
# 2) Find the largest
largest_bbox_area = 0
for div in soup.find_all('div', attrs={"class": "ocr_carea"}):
    bbox = div['title'].split()
    bbox_width = int(bbox[3]) - int(bbox[1])
    bbox_height = int(bbox[4]) - int(bbox[2])
    bbox_area = bbox_width * bbox_height
    if bbox_area >= (img_area * 0.95):
        div.decompose()
    else:
        if(bbox_area > largest_bbox_area):
            largest_bbox_area = bbox_area
            largest_bbox_div = div

# Remove any bounding box overlapping with the largest one
bbox = largest_bbox_div['title'].split()
largest_bbox_rect = Rect(Point(int(bbox[1]), img_height - int(bbox[2])), Point(int(bbox[3]), img_height - int(bbox[4])))
for div in soup.find_all('div', attrs={"class": "ocr_carea"}):
    if(div != largest_bbox_div):
        bbox = div['title'].split()
        rect = Rect(Point(int(bbox[1]), img_height - int(bbox[2])), Point(int(bbox[3]), img_height - int(bbox[4])))
        if overlap(rect, largest_bbox_rect):
            div.decompose()

# Find the box beneath the largest one and get the caption
caption = ""
next = False
for div in soup.find_all('div', attrs={"class": "ocr_carea"}):
    if(div == largest_bbox_div):
        next = True
    else:
        if next:
            for span in div.p.span:
                caption += span.string
            break

print(caption)
