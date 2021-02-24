from PIL import ImageTk, Image 

def makePhoto(file_name):
    return ImageTk.PhotoImage(Image.open(file_name))

def getRGB(file_name):
    return Image.open(file_name).convert('RGB')

def getImageHeight(photo):
    return photo.height()

def getImageWidth(photo):
    return photo.width()

