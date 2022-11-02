# circularity = (perimeter^2 / 4*pi) * area
from asyncore import loop
from re import L
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
        if (pixel_array[x, y] == 255):
           return (x, y)
        y += 1

    return min(findCircle(pixel_array, startX/2, width), findCircle(pixel_array, startX + startX/2, width))


def loopAroundCircle(pixel_array, steps, currentX, currentY, dirX, dirY, startX, startY):
    # print("---------------")
    # print(currentX, currentY, dirX, dirY)

    # stop conditions
    if (currentX == startX and currentY == startY):
        print("stop")
        return steps
    if (pixel_array[currentX][currentY] == 0):
        # pixel_array[currentX, currentY] = 100
        # print(pixel_array)
        print("error: moved to a black pixel!")
        return 0

    while(currentX != startX and currentY != startY):
        # debug print
        pixel_array[currentX, currentY] = 100
        # print(np.array([[pixel_array[currentX-1][currentY+1], pixel_array[currentX][currentY+1], pixel_array[currentX+1][currentY+1]], 
        #         [pixel_array[currentX-1][currentY], pixel_array[currentX][currentY], pixel_array[currentX+1][currentY]],
        #         [pixel_array[currentX-1][currentY-1], pixel_array[currentX][currentY-1], pixel_array[currentX+1][currentY-1]]]))    
        # print(pixel_array)

        # Following is a nest of if statements to determine where the next step in following the circle line is.
        # Assuming the circles are somwhat circular would make this a lot easier, but now we have to check for 
        #   each of 5 freedoms of movement, for each moving along the x-axis, y-axis, and a combi of the two. 
        # was done with recursion but reached the recursion depth limit on 800x800 perfect circle image.

        # only moved in y direction
        if (dirX == 0):
            if (pixel_array[currentX][currentY + dirY] == 255):
                print("21")
                # same y direction == white pixel
                if (pixel_array[currentX + 1][currentY + dirY] == 255):
                    print("22")
                    # same y direction, one pixel to right == white pixel
                    if (pixel_array[currentX - 1][currentY + dirY] == 255):
                        print("23")
                        # same y direction, one pixel to left == white pixel
                        if (pixel_array[currentX - 1][currentY] == 255):
                            print("24")
                            # one pixel to left == white pixel, must be same y direction one right
                            # return loopAroundCircle(pixel_array, steps+1, currentX + 1, currentY + dirY, 1, dirY, startX, startY)
                        else:
                            print("25")
                            # one pixel to right == white pixel, same y one to the left must be the next direction
                            # return loopAroundCircle(pixel_array, steps+1, currentX -1, currentY + dirY, -1, dirY, startX, startY)
                    else:
                        print("26")
                        # same y direction, one to left = black pixel, must be same y direction
                        # return loopAroundCircle(pixel_array, steps+1, currentX, currentY + dirY, 0, dirY, startX, startY)
                else:
                    print("27")
                    # same y direction, one to right = black pixel, must be same y direction
                    # return loopAroundCircle(pixel_array, steps+1, currentX, currentY + dirY, 0, dirY, startX, startY)
            # same direction = black pixel
            elif (pixel_array[currentX - 1][currentY + dirY] == 255):
                print("28")
                # same y direction, one to left = white pixel, must be same y direction one to the left
                # return loopAroundCircle(pixel_array, steps+1, currentX - 1, currentY + dirY, -1, dirY, startX, startY)
            elif (pixel_array[currentX + 1][currentY + dirY] == 255):
                print("29")
                # same y direction, one to right = white pixel, must be same y direction one to the left
                # return loopAroundCircle(pixel_array, steps+1, currentX + 1, currentY + dirY, 1, dirY, startX, startY)
            elif (pixel_array[currentX - 1][currentY] == 255):
                print("30")
                # one to left = white pixel, must be one to the left
                # return loopAroundCircle(pixel_array, steps+1, currentX - 1, currentY, -1, 0, startX, startY)
            else:
                print("31")
                # one to right = white pixel, must be one to the righr
                # return loopAroundCircle(pixel_array, steps+1, currentX + 1, currentY, 1, 0, startX, startY)

        # only moved in x direction
        elif (dirY == 0):
            if (pixel_array[currentX + dirX][currentY] == 255):
                print("1")
                # same x direction == white pixel
                if (pixel_array[currentX + dirX][currentY + 1] == 255):
                    print("2")
                    # same x direction, one pixel down == white pixel
                    if (pixel_array[currentX + dirX][currentY - 1] == 255):
                        print("3")
                        # same x direction, one pixel up == white pixel
                        if (pixel_array[currentX][currentY + 1] == 255):
                            print("4")
                            # one pixel down == white pixel, must be same x direction one up 
                            # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY - 1, dirX, -1, startX, startY)
                        else:
                            print("5")
                            # one pixel to up == white pixel, must be the next direction
                            # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY + 1, dirX, 1, startX, startY)
                    else:
                        print("6")
                        # same x direction, one up == black pixel, must be same x direction CHANGED FROM +DIRX +1
                        # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY, dirX, 0, startX, startY)
                else:
                    print("7")
                    # same x direction, one down == black pixel, must be same x direction CHANGED FROM +DIRX -1
                    # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY, dirX, 0, startX, startY)
            # same direction = black pixel
            elif (pixel_array[currentX + dirX][currentY + 1] == 255):
                print("8")
                # same x direction, one up == white pixel, must be same x direction one up
                # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY + 1, dirX, 1, startX, startY)
            elif (pixel_array[currentX + dirX][currentY - 1] == 255):
                print("9")
                # same x direction, one down == white pixel, must be same x direction one down
                # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY - 1, dirX, -1, startX, startY)
            elif (pixel_array[currentX][currentY + 1] == 255):
                print("10")
                # one down == white pixel, must be one down
                # return loopAroundCircle(pixel_array, steps+1, currentX, currentY + 1, 0, 1, startX, startY)
            else:
                print("11")
                # one up == white pixel, must be one up 
                # return loopAroundCircle(pixel_array, steps+1, currentX, currentY - 1, 0, -1, startX, startY)

        # moved in x and y direction
        else:
            if (pixel_array[currentX + dirX][currentY + dirY] == 255):
                print("12")
                # exact same direction == white pixel
                if (pixel_array[currentX][currentY + dirY] == 255):
                    print("13")
                    # y direction == white pixel
                    if (pixel_array[currentX + dirX][currentY] == 255):
                        print("14")
                        # x direction == white pixel
                        if (pixel_array[currentX - dirX][currentY] == 255):
                            print("15")
                            # opposite x direction == white pixel, must be x direction
                            # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY, dirX, 0, startX, startY)
                        else:
                            print("16")
                            # opposite x direction == black pixel, must be y direction
                            # return loopAroundCircle(pixel_array, steps+1, currentX, currentY + dirY, 0, dirY, startX, startY)
                    else:
                        print("17")
                        # x direction == black pixel, must be exact same direction
                        # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY + dirY, dirX, dirY, startX, startY)
                else:
                    print("18")
                    # y direction == black pixel, must be exact same direction
                    # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY + dirY, dirX, dirY, startX, startY)
            # same direction == black pixel
            elif (pixel_array[currentX][currentY + dirY] == 255):
                print("19")
                # y direction == white pixel, must be y direction
                # return loopAroundCircle(pixel_array, steps+1, currentX, currentY + dirY, 0, dirY, startX, startY)
            else:
                print("20")
                # y direction == black pixel, must be x direction
                # return loopAroundCircle(pixel_array, steps+1, currentX + dirX, currentY, dirX, 0, startX, startY)


def calculatePerimeter(pixel_array, startX, startY):
    # start in white pixel on edge circle
    x = startX
    y = startY
    	
    # 0, 3
    # 1, 5

    # pixel_array[x,y] = 100

    # first step, counter clockwise, almost always at the top of circle
    if (pixel_array[x+1][y-1] == 0 and  pixel_array[x+1][y] == 255):
        x = x - 1
        dirX = -1
        dirY = 0
    elif (pixel_array[x+1][y-1] == 0 and pixel_array[x+1][y] == 0):
        x = x - 1
        y = y - 1
        dirX = -1
        dirY = +1
    
    # print(x, y)
    # pixel_array[x+1,y-1] = 100
    # pixel_array[x+1,y] = 100
    # print(pixel_array)
    # print("------")

    # loops around the circle by following around the edge
    return loopAroundCircle(pixel_array, 1, x, y, dirX, dirY, startX, startY)

    

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # read image of circle
    image = Image.open(os.path.join(current_dir, 'perfect_circle.png'))
    width, height = image.size

    # 800x800, (0,0) top left
    pixel_array = np.array(image)
    print(pixel_array.shape)
    # pixel_array = pixel_array[:][:]
    print(pixel_array)
    
    # circle = np.where(pixel_array == 255)
    # print(circle)
    
    # find a coordinate of the circle to start calculating the perimeter
    (circle_startX, circle_startY) = findCircle(pixel_array, width/2, width)
    print(calculatePerimeter(pixel_array, circle_startX, circle_startY))
    # print(perimeter)

    # # print(perimeter)
    # for i in range(circle_startY):
        # pixel_array[circle_startX, i] = 255

    # pixel_array[0, 3] = 255
    # pixel_array[1, 5] = 255

    newIm = Image.fromarray(pixel_array)
    newIm.save('test3.png')

if __name__ == "__main__":
    main()