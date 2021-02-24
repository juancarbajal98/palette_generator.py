from PIL import ImageTk, Image 

def resizeImage(file_name,height,width):
    if(isinstance(height,float) or isinstance(width,float)):
        height = round(height)
        width = round(width)
    image = Image.open(file_name)
    image = image.resize((width,height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

def updateRGB(file_name, height, width):
    if(isinstance(height,float) or isinstance(width,float)):
        height = round(height)
        width = round(width)
    image = Image.open(file_name)
    image = image.resize((width,height), Image.ANTIALIAS)
    return image.convert('RGB')