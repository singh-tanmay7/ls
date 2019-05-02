import math
import numpy as np

def cart2pol(x,y):
	theta= np.arctan2(y,x)
	rho1=np.add(np.square(x),np.square(y))
	rho=np.sqrt(rho1)
	return (theta,rho)

def hillshade(dem,azimuth,altitude,zf):
	if azimuth==-1:
		azimuth=315
	if altitude==-1:
		altitude=45
	if zf==-1:
		zf=1



	dx=5  # get cell spacing in x and y direction
	dy=5  # from coordinate vectors

	# lighting azimuth
	azimuth = 360.0-azimuth+90 #convert to mathematic unit 
	if (azimuth>=360):
		azimuth=azimuth-360
	azimuth = azimuth * (math.pi/180) #  convert to radians

	#lighting altitude
	altitude = (90-altitude) * (math.pi/180) # convert to zenith angle in radians


	(fx,fy)= np.gradient(dem)
	(asp,grad)=cart2pol(fx,fy)
	grad=np.arctan(grad*zf)
	check=asp<(math.pi)
	asp=np.multiply(asp,check)
	asp=np.add(asp,(math.pi)/2)
	check= asp<0
	asp=np.multiply(asp,check)
	asp=np.add(asp,2*math.pi)

	asp=asp*-1
	asp=asp+azimuth

	h=255*np.add(np.multiply(np.cos(altitude),np.cos(grad)),np.multiply(np.sin(altitude),np.multiply(np.sin(grad),np.cos(asp))))
	h=np.asarray(h)
	check=h<0
	h=np.multiply(h,check)

	return h




