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
        if (pixel_array[x, y] > 0):
           return (x, y)
        y += 1

    return min(findCircle(pixel_array, startX/2, width), findCircle(pixel_array, startX + startX/2, width))


def calculatePerimeter(pixel_array, startX, startY):
    # start in white pixel on edge circle
    currentX = startX
    currentY = startY

    # print(np.array([[pixel_array[currentX-1][currentY+1], pixel_array[currentX][currentY+1], pixel_array[currentX+1][currentY+1]], 
    #             [pixel_array[currentX-1][currentY], pixel_array[currentX][currentY], pixel_array[currentX+1][currentY]],
    #             [pixel_array[currentX-1][currentY-1], pixel_array[currentX][currentY-1], pixel_array[currentX+1][currentY-1]]]))    
        
    # first step
    adjIndices = np.array(pixel_array[startX-1:startX+2, startY-1:startY+2]).flatten()
    print(adjIndices)
    for i in range(len(adjIndices)):
        pass

    # print(np.array([[pixel_array[currentX-1][currentY+1], pixel_array[currentX][currentY+1], pixel_array[currentX+1][currentY+1]], 
    #             [pixel_array[currentX-1][currentY], pixel_array[currentX][currentY], pixel_array[currentX+1][currentY]],
    #             [pixel_array[currentX-1][currentY-1], pixel_array[currentX][currentY-1], pixel_array[currentX+1][currentY-1]]]))    
        
    
    # steps around circle
    steps = 1

    while(currentX != startX or currentY != startY):

        if (pixel_array[currentX][currentY] == 0):
            print("error: moved to a black pixel!")
            return 0

        # debug print
        pixel_array[currentX, currentY] = 100
        # print(np.array([[pixel_array[currentX-1][currentY+1], pixel_array[currentX][currentY+1], pixel_array[currentX+1][currentY+1]], 
        #         [pixel_array[currentX-1][currentY], pixel_array[currentX][currentY], pixel_array[currentX+1][currentY]],
        #         [pixel_array[currentX-1][currentY-1], pixel_array[currentX][currentY-1], pixel_array[currentX+1][currentY-1]]]))    
        # print(pixel_array)


        # Following is a nest of if statements to determine where the next step in following the circle line is.
        # Assuming the circles are somwhat circular would make this a lot easier, but now we have to check for 
        #   each of 5 freedoms of movement, for each moving along the x-axis, y-axis, and a combi of the two. 
        # Was done with recursion but reached the recursion depth limit on 800x800 perfect circle image. 
        #   Now rewritten using a big while loop (very ugly code >:( )

        # only moved in y direction
        if (dirX == 0):
            if (pixel_array[currentX][currentY + dirY] > 0):
                print("21")
                # same y direction == white pixel
                if (pixel_array[currentX + 1][currentY + dirY] > 0):
                    print("22")
                    # same y direction, one pixel to right == white pixel
                    if (pixel_array[currentX - 1][currentY + dirY] > 0):
                        print("23")
                        # same y direction, one pixel to left == white pixel
                        if (pixel_array[currentX - 1][currentY] > 0):
                            print("24")
                            # one pixel to left == white pixel, must be same y direction one right
                            nextStep = (currentX + 1, currentY + dirY)
                        else:
                            print("25")
                            # one pixel to right == white pixel, same y one to the left must be the next direction
                            nextStep = (currentX - 1, currentY + dirY)
                    else:
                        print("26")
                        # same y direction, one to left = black pixel, must be same y direction
                        nextStep = (currentX, currentY + dirY)
                else:
                    print("27")
                    # same y direction, one to right = black pixel, must be same y direction
                    nextStep = (currentX, currentY + dirY)
            # same direction = black pixel
            elif (pixel_array[currentX - 1][currentY + dirY] > 0):
                print("28")
                # same y direction, one to left = white pixel, must be same y direction one to the left
                nextStep = (currentX - 1, currentY + dirY)
            elif (pixel_array[currentX + 1][currentY + dirY] > 0):
                print("29")
                # same y direction, one to right = white pixel, must be same y direction one to the left
                nextStep = (currentX + 1, currentY + dirY)
            elif (pixel_array[currentX - 1][currentY] > 0):
                print("30")
                # one to left = white pixel, must be one to the left
                nextStep = (currentX - 1, currentY)
            else:
                print("31")
                # one to right = white pixel, must be one to the righr
                nextStep = (currentX + 1, currentY)

        # only moved in x direction
        elif (dirY == 0):
            if (pixel_array[currentX + dirX][currentY] > 0):
                print("1")
                # same x direction == white pixel
                if (pixel_array[currentX + dirX][currentY + 1] > 0):
                    print("2")
                    # same x direction, one pixel down == white pixel
                    if (pixel_array[currentX + dirX][currentY - 1] > 0):
                        print("3")
                        # same x direction, one pixel up == white pixel
                        if (pixel_array[currentX][currentY + 1] > 0):
                            print("4")
                            # one pixel down == white pixel, must be same x direction one up 
                            nextStep = (currentX + dirX, currentY - 1)
                        else:
                            print("5")
                            # one pixel to up == white pixel, must be the next direction
                            nextStep = (currentX + dirX, currentY + 1)
                    else:
                        print("6")
                        # same x direction, one up == black pixel, must be same x direction CHANGED FROM +DIRX +1
                        nextStep = (currentX + dirX, currentY)
                else:
                    print("7")
                    # same x direction, one down == black pixel, must be same x direction CHANGED FROM +DIRX -1
                    nextStep = (currentX + dirX, currentY)
            # same direction = black pixel
            elif (pixel_array[currentX + dirX][currentY + 1] > 0):
                print("8")
                # same x direction, one up == white pixel, must be same x direction one up
                nextStep = (currentX + dirX, currentY + 1)
            elif (pixel_array[currentX + dirX][currentY - 1] > 0):
                print("9")
                # same x direction, one down == white pixel, must be same x direction one down
                nextStep = (currentX + dirX, currentY - 1)
            elif (pixel_array[currentX][currentY + 1] > 0):
                print("10")
                # one down == white pixel, must be one down
                nextStep = (currentX, currentY + 1)
            else:
                print("11")
                # one up == white pixel, must be one up 
                nextStep = (currentX, currentY - 1)

        # moved in x and y direction
        else:
            if (pixel_array[currentX + dirX][currentY + dirY] > 0):
                print("12")
                # exact same direction == white pixel
                if (pixel_array[currentX][currentY + dirY] > 0):
                    print("13")
                    # y direction == white pixel
                    if (pixel_array[currentX + dirX][currentY] > 0):
                        print("14")
                        # x direction == white pixel
                        if (pixel_array[currentX - dirX][currentY] > 0):
                            print("15")
                            # opposite x direction == white pixel
                            if (pixel_array[currentX + dirX][currentY - dirY] > 0):
                                print("43")
                                # same x, opposite y == white pixel, must be direction
                                nextStep = (currentX + dirX, currentY - dirY)
                            else:
                                print("44")
                                # same x, opposite y == black pixel, must be same x direction
                                nextStep = (currentX + dirX, currentY)
                        elif (pixel_array[currentX - dirX][currentY + dirY] > 0):
                            print("45")
                            # angle of 90 degrees towards y direction == white pixel, must be this direction
                            nextStep = (currentX - dirX, currentY + dirY)
                        else:
                            print("16")
                            # opposite x direction == black pixel, must be y direction
                            nextStep = (currentX, currentY + dirY)
                    else:
                        print("17")
                        # x direction == black pixel, must be exact same direction
                        nextStep = (currentX + dirX, currentY + dirY)
                else:
                    print("18")
                    # y direction == black pixel, must be exact same direction
                    nextStep = (currentX + dirX, currentY + dirY)
            # same direction == black pixel
            elif (pixel_array[currentX][currentY + dirY] > 0):
                print("19")
                # y direction == white pixel, must be y direction
                nextStep = (currentX, currentY + dirY)
            elif (pixel_array[currentX + dirX][currentY] > 0):
                print("42")
                # x direction == white pixel, must be x direction
                nextStep = (currentX + dirX, currentY )
            elif (pixel_array[currentX + dirX][currentY - dirY] > 0):
                print("20")
                # angle of 90 degrees of of last step in x direction is the only possible direction
                nextStep = (currentX + dirX, currentY - dirY)
            else: 
                print("41")
                # angle of 90 degrees of of last step in y direction is the only possible direction
                nextStep = (currentX - dirX, currentY + dirY)

        # calc direction of step taken
        dirX = nextStep[0] - currentX
        dirY = nextStep[1] - currentY

        # assign new coords
        currentX = nextStep[0]
        currentY = nextStep[1]

        steps += 1

    # end of while loop -> back at the starting pixel after going around perimeter of circle
    return steps

    

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # read image of circle
    image = Image.open(os.path.join(current_dir, 'weird_shape_small.png'))
    width, height = image.size

    # 800x800, (0,0) top left
    pixel_array = np.array(image)
    
    # find a coordinate of the circle to start calculating the perimeter
    (circle_startX, circle_startY) = findCircle(pixel_array, width/2, width)
    # print(circle_startX, circle_startY)
    pixel_array[circle_startX, circle_startY] = 100
    print(calculatePerimeter(pixel_array, circle_startX, circle_startY))
    # print(perimeter)

    newIm = Image.fromarray(pixel_array)
    newIm.save('test3.png')

if __name__ == "__main__":
    main()