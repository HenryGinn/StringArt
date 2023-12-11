# StringArt
Toolkit for converting pictures into instructions on how to draw it by threading string between nails

This program should be able to do the following
- Show a pixelated version of the input picture
- Show the black and white version of the input picture
- Show the decomposition of the input picture into RGB
- Show the distribution of nails around the input picture
- Show the region being optimised
- Calculate and show a sequence for a single colour thread
- Calculate and show a sequence for two colours with no weaving
- Calculate and show a sequence for two colours with symmetric weaving
- Calculate and show a sequence for two colours with general weaving

## How to define the image region

I want this to be able to take in a rectangular image and allow the user to control the size and location of circle of pins relative to the image. They should also be able to define a circle of interest that has the same centre as the circle of pins, and this is the region that will be optimised over.

To do this I will have a square window on the left taking up the full height of the screen and the shell will be on the right. It will give them options such as moving the image in each direction by some number of pixels, change the radius of the pin circle, and change the radius of the interest circle.