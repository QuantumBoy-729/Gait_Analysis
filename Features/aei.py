import glob
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Finding the center of mass of a silhouette
def CenterOfMass(img):
    height, width = img.shape # Import height and width from frames
    X = [] # Sum of x-coordinates of each row
    Y = [] # Sum of y-coordinates of each column
    WoR = [] # Weights of rows
    WoC = [] # Weights of columns
    for i in range(height):
        Nx = [] # x-coordinates of silhouette pixels in a single row
        for j in range(width):
            if img[i,j] == 255: # If the pixel is white
                Nx.append(j) # Append its x-coordinate
        if len(Nx) != 0: # If the row is not empty
            X.append(sum(Nx)) # Append the sum of the x-coordinates of the row
            WoR.append(len(Nx)) # Append the number of white pixels of the row
    CoMX = sum(X) // sum(WoR) # The average of the x-coordinates is their center of mass on x
    for j in range(width):
        Ny = [] # y-coordinates of silhouette pixels in a single column
        for i in range(height):
            if img[i,j] == 255: # If the pixel is white
                Ny.append(i) # Append its y-coordinate
        if len(Ny) != 0: # If the column is not empty
            Y.append(sum(Ny)) # Append the sum of the y-coordinates of the column
            WoC.append(len(Ny)) # Append the number of white pixels of the column
    CoMY = sum(Y) // sum(WoC) # The average of the y-coordinates is their center of mass on y
    return CoMX, CoMY # Return the coordinates of the center of mass of the silhouette

#Finding the corner coordinates of the rectangle surrounding the silhouette
def Border(img):
    height, width = img.shape # Import height and width from frames
    indexl = [] # x-coordinates of left-most pixel of each row
    indexr = [] # x-coordinates of right-most pixel of each row
    for i in range(height): # For each row
        for j in range(width): # Start from the left-most pixel
            if img[i,j] != 0: # If the pixel is not black
                indexl.append(j) # Append its x-coordinate
                break # Move to next row
        for j in reversed(range(width)): # Start from the right-most pixel
            if img[i,j] != 0: # If the pixel is not black
                indexr.append(j) # Append its x-coordinate
                break # Move to next row
    x = min(indexl) # The left-most x-coordinate in all rows
    X = max(indexr) # The right-most x-coordinate in all rows
    indext = [] # y-coordinates of top-most pixel of each column
    indexb = [] # y-coordinates of bottom-most pixel of each column
    for j in range(width):
        for i in range(height): # Start from the top-most pixel
            if img[i,j] != 0: # If the pixel is not black
                indext.append(i) # Append its y-coordinate
                break # Move to next column
        for i in reversed(range(height)): # Start from the bottom-most pixel
            if img[i,j] != 0: # If the pixel is not black
                indexb.append(i) # Append its y-coordinate
                break # Move to next column
    y = min(indext) # The top-most y-coordinate in all columns
    Y = max(indexb) # The bottom-most y-coordinate in all columns
    return x,X,y,Y

#Cropping the silhouette based on the results from Border function
def Crop(img,x,X,y,Y):
    Crop = img[y:Y, x:X]
    return Crop

#Aligning the silhouettes based on their center of mass and averaging them
def align_cropped(old,new,center,black): # Current AEI, new frame, center of mass, black background, frame index
    center = list(center) # Width and height of silhouettes
    height, width = old.shape # Height and width of the frames
    x = (width // 2) - center[0] # left x-coordinate of the silhouette's frame
    y = (height // 2) - center[1] # top y-coordinate of the silhouette's frame
    height, width = new.shape # Width and height of a black background
    X = (x + width) # right x-coordinate of the silhouette's frame
    Y = (y + height) # bottom y-coordinate of the silhouette's frame
    new = cv2.addWeighted(new, 1, old[y:Y, x:X], 1, 0.0) # Combine the new frame inside the silhouette
    old = cv2.addWeighted(black, 1, old, 1, 0.0) # Combine the new frame outside the silhouette
    old[y:Y, x:X] = new # AEI
    return old

#Importing the silhouettes, and getting their dimensions
path = glob.glob('./00001/*.png') # Path of the frames
im = cv2.imread(path[0]) # Read the first frame
y,x,c = im.shape # Height, width and channels respectively

#Combining the functions
black = np.zeros((y,x), np.uint8) # Black background
AEI = black # Define AEI
i = 1 # Define frames index
for path in glob.glob('./00001/*.png'): # For every frame in the path
    image = cv2.imread(path) # Read the frame
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # Turn the frame to one channel
    x,X,y,Y = Border(image) # Find the borders of the silhouette
    cropped = Crop(image,x,X,y,Y) # Crop the silhouette
    
    center = CenterOfMass(cropped) # Find the center of mass of the silhouette
    sz_norm = align_cropped(AEI,cropped,center,black) # Find the AEI with the latest frame

    cv2.imwrite('./test/aframes/cropped_' + str(i) + '.png', sz_norm) # Save the cropped silhouette
    i += 1 # Add 1 to index of frames
    print("Saved..")
