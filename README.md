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


