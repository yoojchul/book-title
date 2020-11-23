import numpy as np 
import cv2 
import sys,io, os

def detect_text(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    return(texts)

# Reading image 
img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR) 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 100, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 300)

taps = detect_text(sys.argv[1]) # title, author and publisher

dividers = [] # to filter lines which not touch any titles 
for i in range(len(lines)):
    for rho, theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)

        cross = False
        for t in taps[1:]: 
            minus = 0
            for v in t.bounding_poly.vertices:
                m = v.x * a / rho + v.y * b / rho - 1
                if np.abs(m) < 0.0001: # actually zero
                    continue # borders area of of title 
                elif minus == 0: # first 
                    minus = m
                elif (minus > 0 and m > 0) or (minus < 0 and m < 0):
                    continue # same side and keep going 
                else: # other side 
                    cross = True
                    break
            if cross: # not need to check remaining 
                break
        if cross: # boarders area of title or passes 
            continue # throw away 

        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 10000*(-b)) # 10000 is for 4000x3000 picture 
        y1 = int(y0 + 10000 * a)
        x2 = int(x0 - 10000*(-b))
        y2 = int(y0 - 10000*a)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
        dividers.append([rho, theta])

merged = []
titles = taps[0].description.split("\n")
i = 1   # concat title in a word if possible
for title in titles:
    xs, ys = [], []
    while  i <  len(taps) and taps[i].description in title:
        for vertex in taps[i].bounding_poly.vertices:
            xs.append(vertex.x)
            ys.append(vertex.y)
        i += 1
    if xs == []:
        continue
    left_low = (min(xs), min(ys))
    left_high = (min(xs), max(ys))
    right_low = (max(xs), min(ys))
    right_high = (max(xs), max(ys))
    merged.append([title, left_low, left_high, right_low, right_high])
        
# prev_x and prev_y is center 
prev_x = (merged[0][1][0] + merged[0][2][0] + merged[0][3][0] + merged[0][4][0])/4.0
prev_y = (merged[0][1][1] + merged[0][2][1] + merged[0][3][1] + merged[0][4][1])/4.0
words = [merged[0][0]]

for t in merged[1:]:
    cross = False
    center_x = (t[1][0] + t[2][0] + t[3][0] + t[4][0])/4.0
    center_y = (t[1][1] + t[2][1] + t[3][1] + t[4][1])/4.0
    for divider in dividers:
        a = np.cos(divider[1])
        b = np.sin(divider[1])
        if (prev_x * a / divider[0] + prev_y * b / divider[0] - 1) * (center_x * a / divider[0] + center_y * b / divider[0] - 1) < 0:
            cross = True  # opposite sides means that there is a line between them 
            break
    if cross:
        print(' / '.join(words))
        words = [t[0]]
    else:
        words.append(t[0])
    prev_x = center_x
    prev_y = center_y
print(' / '.join(words))
    
resized = cv2.resize(img, dsize=(0,0), fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
cv2.imshow('img', resized)
resized_edges = cv2.resize(edges, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
cv2.imshow('canny', resized_edges)
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 
