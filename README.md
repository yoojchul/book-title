# book-title

This program recognizes all characters of titles, authors and publisher on books in shelves using Google OCR. Just Google OCR understands letters of book covers well. 

![fig1](https://user-images.githubusercontent.com/15276052/99383632-7dff5380-2911-11eb-9f67-ce7b2a81d9ae.png)

But there is no distinction between results of Google OCR. We see outputs of an OCR program like this. 

A Thousand Plateaus: \
Capitalism and Schizophrenia \
DELEUZE GUATTARI \
Anthlone Press \
Head First Python \
Paul Barry \
O’REILLY

Based on lines between books, this program groups titles, authors and publisher of the same book. 

A Thousand Plateaus: /Capitalism and Schizophrenia / DELEUZE GUATTARI / Anthlone Press \
Head First Python / O’REILLY / Paul Barry

Firstly, the program finds out the lines between books using Hough Line Transform(opencv). Then, it selects lines which don’t touch any titles, authors and publishers. Because Hough Line Transform supplied by opencv is not perfect, there are many spurious lines across letters. 


![fig4](https://user-images.githubusercontent.com/15276052/99384139-53fa6100-2912-11eb-9812-3b1c911973c7.PNG)

If expression L is 0,  (x, y) is on the line which is represented with theta and rho. 

Expression L : x * cos(theta) / rho + y * sin(theta) / rho – 1 

If the sign of expression L is different from the other point, they are opposite. 

The next step is to merge bounding_ploly into a phrase. For example,  “A Thousand Plateaus:” is presented together in the first element of Google OCR. 

taps[0].description = “A Thousand Plateaus:\n Capitalism and Schizophrenia\n….” 
taps[1].description = “A”
taps[2].description = “Thousand”
taps[3].description = “Plateaus:”
…

But they can be given separately from the second element.   They need to be merged according to the first element. 

Finally if there is no red line between recognized letters, that is, the sign of expression L is the same,  they are considered to be at the same book. 

![fig5](https://user-images.githubusercontent.com/15276052/99384176-5f4d8c80-2912-11eb-91db-763ab616d569.PNG)

The real is as follows. 

![fig2](https://user-images.githubusercontent.com/15276052/99384184-62e11380-2912-11eb-8b97-982782f40079.PNG)
