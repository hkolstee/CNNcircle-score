from asyncore import loop
from PIL import Image
import numpy as np
import os.path
import sys
import math
import cv2 as cv
from collections import namedtuple

# After writing using namedtuple, found out it is rather expensive on creation
Perimeter = namedtuple('Perimeter',['coords','length'])
Pixel = namedtuple('Pixel', ['x','y'])

# np.set_printoptions(edgeitems=30, linewidth=100000, 
                    # formatter=dict(float=lambda x: "%.3g" % x))

# recursively try to find the circle
def findCircle(pixel_array, startX, step, width, height):
    # stop condition
    if (step < int(width/200)):
        return (0, 0)
    
    x = int(startX)
    y = 0

    while (y < height):
        if (pixel_array[x, y] > 0):
           return Pixel(x, y)
        y += 1

    return max(findCircle(pixel_array, startX + step, step/2, width, height), 
                findCircle(pixel_array, startX - step, step/2, width, height))

# find the next step around the circle
def findNextStep(pixel_array, currentPixel):

    # 8 adjacent indices
    adjPixels = np.array(pixel_array[currentPixel.x-1:currentPixel.x+2, 
                                    currentPixel.y-1:currentPixel.y+2])
    adjPos = (0,0)
    direction = [(1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1)]
    # rotate through adjecent indices, comparing them to next one next to the current to look for border white/black pixel
    for i in range(adjPixels.size-1):
        if (adjPixels[adjPos[0], adjPos[1]] > 0 and adjPixels[(adjPos[0] + direction[i][0], adjPos[1] + direction[i][1])] == 0):
        
            # We found a bordering pixel where current adjacent pixel is white, and clockwise next adjacent pixel is black
            # subtract 1 from both coords to adjust for the offset of the adjecent pixel array
            nextPixel = Pixel(currentPixel.x + adjPos[0] - 1, currentPixel.y + adjPos[1] - 1)
            break

        # next pixel in circle around starting pixel
        nextX = adjPos[0] + direction[i][0]
        nextY = adjPos[1] + direction[i][1]
        adjPos =  (nextX, nextY)
    
    return nextPixel

# calculates the perimeter of a shape (not necessarily circular)
def calculatePerimeter(pixel_array, startPixel):
    pixel_array[startPixel.x, startPixel.y] = 100

    # first step
    currentPixel = findNextStep(pixel_array, startPixel)

    # coordinates of the perimeter of the shape
    perimeterCoords = [currentPixel]
    perimeterLength = 0.0

    # while not at starting pixel
    while(currentPixel.x != startPixel.x or currentPixel.y != startPixel.y):
        if (pixel_array[currentPixel.x][currentPixel.y] == 0):
            print("error: moved to a black pixel!")
            return 0

        # debug 
        # pixel_array[currentPixel.x, currentPixel.y] = 100

        # next step
        nextPixel = findNextStep(pixel_array, currentPixel)
        
        # check if diagonal step is taken -> add diagonal to length
        if (nextPixel.x - currentPixel.x !=0 and nextPixel.y - currentPixel.y !=0):
            perimeterLength += math.dist(perimeterCoords[-1], currentPixel)
            perimeterCoords.append((currentPixel.x, currentPixel.y))

        # assign new coords
        currentPixel = nextPixel

    # end of while loop -> back at the starting pixel after going around perimeter of circle
    return Perimeter(perimeterCoords, perimeterLength)

# calculates the area of the irregular shape using the shoelace algorithm
def calculateArea(perimeterCoords):
    sum1 = 0
    sum2 = 0

    for i in range(0, len(perimeterCoords)-1):
        sum1 += perimeterCoords[i][0] * perimeterCoords[i+1][1]
        sum2 += perimeterCoords[i][1] * perimeterCoords[i+1][0]

    # last coord -> first coord
    sum1 += perimeterCoords[len(perimeterCoords)-1][0] * perimeterCoords[0][1]
    sum2 += perimeterCoords[0][0] * perimeterCoords[len(perimeterCoords)-1][1]

    return (abs(sum1 - sum2) / 2)

# The formula to calculate the circularity of a shape
# circularity = (4*pi * area) / (perimeter^2)
def Circularity(perimeterLength, area): 
    return ((4 * np.pi * area) / pow(perimeterLength, 2))

# function that should be called when importing this file
def calculateCircularity(image):
    width, height = image.size
    pixel_array = np.array(image)

    pixel = findCircle(pixel_array, width/2, width/4, width, height)

    if (pixel.x or pixel.y):
        perimeter = calculatePerimeter(pixel_array, pixel)
        area = calculateArea(perimeter.coords)

        # fine tuned to a perfect circle
        return Circularity(perimeter.length, area)
    else:
        return 0

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # read image of circle
    image = Image.open(os.path.join(current_dir, sys.argv[1]))
    width, height = image.size

    # 800x800, (0,0) top left
    pixel_array = np.array(image)
    print(pixel_array)
    
    # find a coordinate of on the edge of the circle to start calculating the perimeter
    circlePixel = findCircle(pixel_array, width/2, width/4, width, height)
    print(pixel_array)
    
    if (circlePixel.x or circlePixel.y):
        # find the coordinates that make the perimeter
        perimeter = calculatePerimeter(pixel_array, circlePixel)

        # debug
        # for i in range(0, len(perimeter.coords)):
            # pixel_array[perimeter.coords[i]] = 100
        # img = Image.fromarray(pixel_array)
        # img.save("test.png")
        
        # find the area of the shape within the perimeter
        area = calculateArea(perimeter.coords)

        # calculate the circularity
        circularity = Circularity(perimeter.length, area)

        print("Perimeter, Area, Circularity = " + str(perimeter.length) + ", " + str(area) + ", " + str(circularity))
        return 0
    else:
        print("No circle found.")
        return 0


if __name__ == "__main__":
    main()