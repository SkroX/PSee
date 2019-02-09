import pyscreenshot as ps
import matplotlib.image as img
def getScreenShot():
	image=ps.grab()
	image.save('sa.png')
	#image.show()
	matrix=img.imread('sa.png')
	return matrix
getScreenShot()
	
