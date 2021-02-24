import tkinter as Tk
from PIL import ImageTk, Image 
from .dimensions import (
    makePhoto, getRGB,
    getImageHeight, getImageWidth
)
from .resize import (
    resizeImage, updateRGB
    )

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

class App(object):
    def __init__(self,root,file_name,orientation,grid):
        # set initial attributes
        self.file_name = file_name + '.jpg'
        self.cubes = []
        self.colors = []
        self.click_counter = 0
        self.grid = grid
        self.orientation = orientation

        # get dimensions from image object
        self.photo = makePhoto(self.file_name)
        self.image_rgb = getRGB(self.file_name)
        self.image_height = getImageHeight(self.photo)
        self.image_width = getImageWidth(self.photo)
        self.ratio = float(self.image_width)/self.image_height
        

        # get box dimensions
        if(orientation=='N' or orientation == 'S'):
            self.box_width = self.image_width / self.grid
            self.box_height = 150
        elif(orientation=='W' or orientation == 'E'):
            self.box_height = self.image_height / self.grid
            self.box_width = 150
        
        # resize
        if(
        (self.image_height + self.box_height) >= 1080 and 
        (orientation == 'N' or orientation == 'S' )):
            print('Image height too large - needs resize.')
            self.image_width = self.ratio * (1040 - self.box_height)
            self.image_height = 1040 - self.box_height
            self.box_width = self.image_width / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)

        if(
        (self.image_width + self.box_width) >= 1920 and 
        (orientation == 'W' or orientation == 'E' )):
            print('Image width too large - needs resize.')
            self.image_height = self.ratio * (1880 - self.box_width)
            self.image_width = 1880 - self.box_width
            self.box_height = self.image_height / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        
        if(
        (self.image_height >= 1080) and 
        (orientation == 'W' or orientation == 'E' )):
            print('Image height too large - needs resize.')
            self.image_width = self.ratio * (1040 - self.box_height)
            self.image_height = 1040 - self.box_height
            self.box_height = self.image_height / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        if(
        (self.image_height >= 1920) and 
        (orientation == 'S' or orientation == 'N' )):
            print('Image width too large - needs resize.')
            self.image_height = self.ratio * (1880 - self.box_width)
            self.image_width = 1880 - self.box_width
            self.box_width = self.image_width / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        
        #create canvas
        if(orientation=='N'):
            self.canvas = Tk.Canvas(root, width = self.image_width, height = (self.box_height + self.image_height), bg = 'white')
            self.canvas.create_image(0,self.box_height, image = self.photo,anchor='nw')
            # x1, y1, x2, y2
            for i in range(self.grid):
                self.canvas.create_line(self.box_width*i,0,self.box_width*i, self.box_height)
            self.canvas.create_line(0,self.box_height,self.image_width,self.box_height)
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        self.box_width*i,
                        0,
                        self.box_width*(i+1),
                        self.box_height))
        elif(orientation=='W'):
            self.canvas = Tk.Canvas(root, width = (self.box_width + self.image_width), height = self.image_height, bg = 'white')
            self.canvas.create_image(self.box_width,0, image = self.photo,anchor='nw')
            # x1, y1, x2, y2
            for i in range(self.grid):
                self.canvas.create_line(0,self.box_height*i,self.box_width, self.box_height*i)
            self.canvas.create_line(self.box_width,0,self.box_width,self.image_height)
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        0,
                        self.box_height*i,
                        self.box_width,
                        self.box_height*(i+1)))
        elif(orientation=='S'):
            self.canvas = Tk.Canvas(root, width = self.image_width, height = (self.box_height + self.image_height), bg = 'white')
            self.canvas.create_image(0,0, image = self.photo,anchor='nw')
            # x1, y1, x2, y2
            for i in range(self.grid):
                self.canvas.create_line(self.box_width*i,self.image_height,self.box_width*i, (self.image_height + self.box_height))
            self.canvas.create_line(0,(self.image_height + self.box_height),self.image_width,(self.image_height + self.box_height))
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        self.box_width*i,
                        self.image_height,
                        self.box_width*(i+1),
                        self.image_height + self.box_height))
        elif(orientation=='E'):
            self.canvas = Tk.Canvas(root, width = (self.box_width + self.image_width), height = self.image_height, bg = 'white')
            self.canvas.create_image(0,0, image = self.photo,anchor='nw')
            # x1, y1, x2, y2
            for i in range(self.grid):
                self.canvas.create_line(self.image_width,self.box_height*i,self.image_width+self.box_width, self.box_height*i)
            self.canvas.create_line(self.image_width,0,self.image_width,self.image_height)
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        self.image_width,
                        self.box_height*i,
                        self.image_width + self.box_width,
                        self.box_height*(i+1)))

        self.canvas.bind('<Button-1>',
            lambda event, file = file_name:
                self.click(event, file))
        root.title('Palette Creator')
        self.canvas.pack()

    def click(self,event,file_name):
        print (event.x, event.y)
        # check for out of bounds click 
        if(
            (self.orientation=='N' and event.y <= self.box_height) or
            (self.orientation=='W' and event.x <= self.box_width) or
            (self.orientation=='S' and event.y >= self.image_height) or
            (self.orientation=='E' and event.x >= self.image_width)
        ):
            print('out of bounds')
            return        
        # capture click color 
        if(self.orientation =='N'):
            self.colors.append(self.image_rgb.getpixel((event.x,event.y-self.box_height)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))
        elif(self.orientation == "W"):
            self.colors.append(self.image_rgb.getpixel((event.x-self.box_width,event.y)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))

        elif(self.orientation == "S"):
            self.colors.append(self.image_rgb.getpixel((event.x,event.y)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))

        elif(self.orientation == "E"):
            self.colors.append(self.image_rgb.getpixel((event.x,event.y)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))
        
        #print('colors:', self.colors)
        self.click_counter += 1
        if(self.click_counter == self.grid):
            self.canvas.update()
            self.canvas.postscript(file=file_name+'.eps')
            img = Image.open(file_name+'.eps')
            img.save(file_name + '-palette.png', 'png')
