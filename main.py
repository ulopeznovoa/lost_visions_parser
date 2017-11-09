
from bs4 import BeautifulSoup
from rect_overlap import *
import sys
import os.path

### ----------- SUPPORT FUNCTIONS -----------

def get_text_from_p(p):
    text = ""
    for span in p:
        if(len(span) > 1):
            for s in span:
                text += s.string
    return text

### ----------- CONSTANTS -----------

CONSIDER_AS_BIG_AS_IMG_THRESHOLD=0.95
CONSIDER_OVERLAPPING_IMG_THRESHOLD=0.8
CAPTION_KEYWORDS={"Fig","Fic"}

### ----------- MAIN PROGRAM -----------


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

# Variable that will hold the caption
caption = ""

# Find all the p blocks in the XML
p_list = soup.find_all('p', attrs={"class": "ocr_par"})

if (len(p_list) == 0):
    sys.stderr.write("No bounding box found")
elif (len(p_list) == 1):
    caption = get_text_from_p(p_list[0])
else:
    # This loop does three things:
    # 1) If any p contains a text with the words in CAPTION_WORD_HINTS, keep it
    # 2) If there is any bounding box (p) almost as big as the image, remove it
    # 3) Find the largest bounding box (p)
    captions_with_keywords=[]
    largest_bbox_area = 0
    for p in p_list:
        bbox = p['title'].split()
        bbox_width = int(bbox[3]) - int(bbox[1])
        bbox_height = int(bbox[4]) - int(bbox[2])
        bbox_area = bbox_width * bbox_height

        text = get_text_from_p(p)
        for word in CAPTION_KEYWORDS:
            if word in text:
                captions_with_keywords.append(text)

        if bbox_area >= (img_area * CONSIDER_AS_BIG_AS_IMG_THRESHOLD):
            p.decompose()
        else:
            if(bbox_area > largest_bbox_area):
                largest_bbox_area = bbox_area
                largest_bbox_p = p


    # Check if any text with "caption keywords" has been detected
    if (len(captions_with_keywords) > 0):
        # TO-DO: Decide what happens if multiple candidate captions are detected
        for text in captions_with_keywords:
            caption += text

    else:
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
        next = False
        for p in soup.find_all('p', attrs={"class": "ocr_par"}):
            if(p == largest_bbox_p):
                next = True
            else:
                if next:
                    caption = get_text_from_p(p)
                    if(len(caption) > 0):
                        break

# Detected caption
print(caption)
