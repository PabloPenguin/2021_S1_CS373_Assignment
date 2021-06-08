
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png

import math


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    gray = createInitializedGreyscalePixelArray(image_width, image_height)
    
    
    for i in range(image_height):
        
        for j in range(image_width):
            
            calculation = round((0.299 * pixel_array_r[i][j]) + (0.587 * pixel_array_g[i][j]) + (0.114 * pixel_array_b[i][j]))
            gray[i][j] = calculation
            
    return gray

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    
    gray = createInitializedGreyscalePixelArray(image_width, image_height)
    
    maximumvalue = -256
    minimumvalue = 256
    
    
    for i in range(image_height):
        
        for j in range(image_width):
            
            if pixel_array[i][j] > maximumvalue:
                maximumvalue = pixel_array[i][j]
                
            if pixel_array[i][j] < minimumvalue:
                minimumvalue = pixel_array[i][j]
    
    zeroCalc = maximumvalue - minimumvalue
    
    if zeroCalc == 0:
        zeroCalc = 1
    
    for i in range(image_height):
        for j in range(image_width):
            
            gray[i][j] = round((pixel_array[i][j] - minimumvalue) * (255 / zeroCalc))
    
    return gray

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    gray = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for i in range(1, image_height - 1):
        for j in range(1, image_width-1):
        
            total = 0
            total = total - pixel_array[i - 1][j - 1]
            total = total - pixel_array[i + 1][j - 1] 
            total = total - (pixel_array[i][j - 1] * 2)
            
            total = pixel_array[i - 1][j + 1] + total
            total = pixel_array[i + 1][j + 1] + total
            total = (pixel_array[i][j + 1] * 2) + total
            
            
            gray[i][j] = (total) / 8   
    
    return gray

def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    gray = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for i in range(1, image_height - 1):
        
        for j in range(1, image_width - 1):
            total = 0
            
            total = total - pixel_array[i + 1][j - 1]
            total = total - pixel_array[i + 1][j + 1]
            total = total - (pixel_array[i + 1][j] * 2)
            
            total = pixel_array[i - 1][j - 1] + total
            total = pixel_array[i - 1][j + 1] + total
            total = (pixel_array[i - 1][j] * 2) + total
            
            
        
            gray[i][j] = (total) / 8   
    
    return gray

def computeEdgeMagnitude(horizontalArray, verticalArray, image_width, image_height):
    gray = createInitializedGreyscalePixelArray(image_width, image_height)

    for i in range(image_height):
        for j in range(image_width):
            calc = math.pow(horizontalArray[i][j], 2) + math.pow(verticalArray[i][j], 2)
            gray[i][j] = math.sqrt(calc)
    return gray

def computeGaussianAveraging3x3RepeatBorder(pixel_array, image_width, image_height):
    bordered = createInitializedGreyscalePixelArray(image_width + 2, image_height + 2)
    gray = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for i in range(0, image_height):
        for j in range(0, image_width):
            bordered[i + 1][j + 1] = pixel_array[i][j]
            
            if (j == 0):
                bordered[i + 1][j] = pixel_array[i][j]
            
            if (i == 0):
                bordered[i][j + 1] = pixel_array[i][j]
            
            if (i == image_height - 1):
                bordered[i + 2][j + 1] = pixel_array[i][j]
            
            if (i == 0 and j == 0):
                bordered[i][j] = pixel_array[i][j]
                
            if (j == image_width - 1):
                bordered[i + 1][j + 2] = pixel_array[i][j]
            
            if (i == 0 and j == image_width - 1):
                bordered[i][j + 2] = pixel_array[i][j]

            if ((i == image_height - 1) and (j == image_width - 1)):
                bordered[i + 2][j + 2] = pixel_array[i][j]
                
            if ((i == image_height - 1) and (j == 0)):
                bordered[i + 2][j] = pixel_array[i][j]
            
    for i in range(1, image_height + 1):
        
        for j in range(1, image_width + 1):
            total = 0
            
            total = bordered[i - 1][j - 1] + total
            total = bordered[i - 1][j + 1] + total
            total = bordered[i - 1][j] * 2 + total
            total = bordered[i][j - 1] * 2 + total
            total = bordered[i][j + 1] * 2 + total
            total = bordered[i][j] * 4 + total
            total = bordered[i + 1][j - 1] + total
            total = bordered[i + 1][j + 1] + total
            total = bordered[i + 1][j] * 2 + total

            gray[i - 1] [j - 1] = total / 16
            
    return gray

def computeThresholdGE(pixel_array, image_width, image_height):
    
    gray = createInitializedGreyscalePixelArray(image_width, image_height)
    threshold_value = 70
    for i in range(image_height):
        for j in range(image_width):
            
            if (pixel_array[i][j] < threshold_value):
                gray[i][j] = 0
            
            else:
                gray[i][j] = 255
    
    return gray

def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    #Change to gray
    gray = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    contrastStretch = scaleTo0And255AndQuantize(gray, image_width, image_height)

    horizontalEdges = computeHorizontalEdgesSobelAbsolute(contrastStretch, image_width, image_height)
    verticalEdges = computeVerticalEdgesSobelAbsolute(contrastStretch, image_width, image_height)
    gradientArray = computeEdgeMagnitude(horizontalEdges, verticalEdges, image_width, image_height)
    #rerunning smooth
    smoothGaussian = computeGaussianAveraging3x3RepeatBorder(gradientArray, image_width, image_height)
    smoothGaussian = computeGaussianAveraging3x3RepeatBorder(smoothGaussian, image_width, image_height)
    smoothGaussian = computeGaussianAveraging3x3RepeatBorder(smoothGaussian, image_width, image_height)
    smoothGaussian = computeGaussianAveraging3x3RepeatBorder(smoothGaussian, image_width, image_height)
    smoothGaussian = computeGaussianAveraging3x3RepeatBorder(smoothGaussian, image_width, image_height)
    smoothGaussian = computeGaussianAveraging3x3RepeatBorder(smoothGaussian, image_width, image_height)
    contrastStretch = scaleTo0And255AndQuantize(smoothGaussian, image_width, image_height)
    
    computeThreshold = computeThresholdGE(contrastStretch, image_width, image_height)

    pyplot.imshow(smoothGaussian, cmap="gray")
    
    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( (10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none' )
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()
