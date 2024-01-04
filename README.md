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

## Interface Overview

The first stage of the program is to create an Art object. Each source image has its own folder which is the first positional argument, and it also needs to be given the name of the image itself - this is to ensure that the source image is processed and not one of the output images. An example is given below.

```
my_art = Art("BirdImage", "BirdImage.png")
```

// Add in an example of folder structure here

The next stage is the image setup where the size and position of the image is defined relative to the circle of pins. This is run automatically if no configuration file can be read, but can be run manually if the `setup_position` method is called.