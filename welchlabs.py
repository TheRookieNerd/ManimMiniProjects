%pylab inline
import time

#Import an image to map:
import matplotlib.image as mpimg
img = mpimg.imread("graphics/imageToMap.jpg")

figure(0, (6,6))
imshow(img)
imgRight = img[:,img.shape[1]/2:]
inputBounds = np.array([0, 2, -2, 2])
inputResolution = imgRight.shape
figure(0, (6,6))
imshow(imgRight)
outputBounds = 6.5*np.array([-1,1,-1,1])
outputResolution = [1200,1200]
#Create x and y sampling vectors
xInput=np.linspace(inputBounds[0], inputBounds[1], inputResolution[1])
yInput=np.linspace(inputBounds[2], inputBounds[3], inputResolution[0])

#Put sampling vectors on 2d grid:
x,y=np.meshgrid(xInput,yInput)
z=x+1j*y
z[0:4,0:4]