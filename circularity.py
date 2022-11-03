from asyncore import loop
from PIL import Image
import numpy as np
import os.path
import sys

np.set_printoptions(edgeitems=30, linewidth=100000, 
                    formatter=dict(float=lambda x: "%.3g" % x))

# recursively try to find the circle
def findCircle(pixel_array, startX, width):
    # stop condition
    if (startX < width/20 or startX > width - width/20):
        return (None, None)
    
    x = int(startX)
    y = 0

    while (y < 800):
        if (pixel_array[x, y] > 0):
           return (x, y)
        y += 1

    return min(findCircle(pixel_array, startX/2, width), findCircle(pixel_array, startX + startX/2, width))

# find the next step around the circle
def findNextStep(pixel_array, currentX, currentY):
    # first step
    # 8 adjecent indices
    adjIndices = np.array(pixel_array[currentX-1:currentX+2, currentY-1:currentY+2])
    pixelX = 0
    pixelY = 0
    direction = [(1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1)]
    # rotate through adjecent indices, comparing them to next one next to the current to look for border white/black pixel
    for i in range(adjIndices.size-1):
        if (adjIndices[pixelX, pixelY] > 0 and adjIndices[(pixelX + direction[i][0], pixelY + direction[i][1])] == 0):
            # add offset to real current pixel
            pixelX -= 1
            pixelY -= 1
            # set next pos
            nextX = currentX + pixelX
            nextY = currentY + pixelY
            break
        # next pixel in circle around starting pixel
        pixelX += direction[i][0]
        pixelY += direction[i][1]
    
    return (nextX, nextY)

# calculates the perimeter of a shape (not necessarily circular)
def calculatePerimeter(pixel_array, startX, startY):
    pixel_array[startX, startY] = 100

    # first step
    currentX, currentY = findNextStep(pixel_array, startX, startY)

    # coordinates of the perimeter of the shape
    perimeterCoords = []

    # while not at starting pixel
    while(currentX != startX or currentY != startY):
        if (pixel_array[currentX][currentY] == 0):
            print("error: moved to a black pixel!")
            return 0

        # add new coordinate
        perimeterCoords.append((currentX, currentY))

        # debug 
        pixel_array[currentX, currentY] = 100

        # next step
        nextStepX, nextStepY = findNextStep(pixel_array, currentX, currentY)

        # assign new coords
        currentX = nextStepX
        currentY = nextStepY

    # end of while loop -> back at the starting pixel after going around perimeter of circle
    return perimeterCoords

# calculates the area of the irregular shape using the shoelace algorithm
def calculateArea(perimeter):
    sum1 = 0
    sum2 = 0

    for i in range(len(perimeter)-1):
        sum1 += perimeter[i][0] * perimeter[i+1][1]
        sum2 += perimeter[i][1] * perimeter[i+1][0]

    # last coord -> first coord
    # sum1 += perimeter[len(perimeter)-1][0] * perimeter[0][1]
    # sum2 += perimeter[0][0] * perimeter[len(perimeter)-1][0]

    return (abs(sum1 - sum2) / 2)

# The formula to calculate the circularity of a shape
# circularity = (perimeter^2) / (4*pi * area)
def calculateCircularity(perimeterLength, area): 
    # the way the perimeter coords is found (on the line not in the line)
    #   we need to add a factor of 10% approximately for perfect circles
    return ((4 * np.pi * area) / pow(perimeterLength * 1.1, 2))

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # read image of circle
    image = Image.open(os.path.join(current_dir, "dataset/" + sys.argv[1]))
    width, _ = image.size

    # 800x800, (0,0) top left
    pixel_array = np.array(image)
    
    # find a coordinate of the circle to start calculating the perimeter
    (circle_startX, circle_startY) = findCircle(pixel_array, width/2, width)

    # find the coordinates that make the perimeter
    perimeterCoords = calculatePerimeter(pixel_array, circle_startX, circle_startY)
    
    # find the area of the shape within the perimeter
    area = calculateArea(perimeterCoords)

    # calculate the circularity
    circularity = calculateCircularity(len(perimeterCoords), area)

    # 
    print("Perimeter, Area, Circularity = " + str(len(perimeterCoords)) + ", " + str(area) + ", " + str(circularity))

    # newIm = Image.fromarray(pixel_array)
    # newIm.save('test3.png')

if __name__ == "__main__":
    main()