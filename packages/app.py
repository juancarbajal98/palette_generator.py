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
        self.save_counter = 0
        self.grid = grid
        self.orientation = orientation
        self.max_height = 1080
        self.max_width = 1920
        self.sidebar_height = 0 
        self.sidebar_width = 0 
        self.padding = 40

        # get dimensions from image object
        self.photo = makePhoto(self.file_name)
        self.image_rgb = getRGB(self.file_name)
        self.image_height = getImageHeight(self.photo)
        self.image_width = getImageWidth(self.photo)
        self.ratio = float(self.image_width)/self.image_height
        

        # get box & sidebar dimensions
        if(orientation=='N' or orientation == 'S'):
            self.box_width = self.image_width / self.grid
            self.box_height = 150
            self.sidebar_width = 300
        elif(orientation=='W' or orientation == 'E'):
            self.box_height = self.image_height / self.grid
            self.box_width = 150
            self.sidebar_height = 200
        
        # resize
        if(
        (self.image_height + self.box_height) >= self.max_height and 
        (orientation == 'N' or orientation == 'S' )):
            print('Image height too large - needs resize.')
            self.image_width = self.ratio * ((self.max_height-self.padding) - self.box_height)
            self.image_height = (self.max_height-self.padding) - self.box_height
            self.box_width = self.image_width / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)

        if(
        (self.image_width + self.box_width) >= self.max_width and 
        (orientation == 'W' or orientation == 'E' )):
            print('Image width too large - needs resize.')
            self.image_height = self.ratio * ((self.max_width-self.padding) - self.box_width)
            self.image_width = (self.max_width-self.padding) - self.box_width
            self.box_height = self.image_height / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        
        if(
        (self.image_height >= (self.max_height-self.sidebar_height)) and 
        (orientation == 'W' or orientation == 'E' )):
            print('Image height too large - needs resize.')
            self.image_width = self.ratio * ((self.max_height-self.sidebar_height-self.padding) - self.box_height)
            self.image_height = (self.max_height-self.sidebar_height-self.padding) - self.box_height
            self.box_height = self.image_height / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        if(
        (self.image_width >= (self.max_width-self.sidebar_width)) and 
        (orientation == 'S' or orientation == 'N' )):
            print('Image width too large - needs resize.')
            self.image_height = self.ratio * ((self.max_width-self.sidebar_width-self.padding) - self.box_width)
            self.image_width = (self.max_width-self.sidebar_width-self.padding) - self.box_width
            self.box_width = self.image_width / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        
        #create canvas
        if(orientation=='N'):
            self.canvas = Tk.Canvas(root, width = self.image_width + self.sidebar_width, height = (self.box_height + self.image_height), bg = 'white')
            self.canvas.create_image(0,self.box_height, image = self.photo,anchor='nw', tags = "imageClick")
            
            # undo and save buttons 
            self.canvas.create_rectangle(
                self.image_width + 100,
                self.image_height - 300,
                self.image_width + 200,
                self.image_height - 200,
                tags = "undoButton"
            )
            self.canvas.create_text(self.image_width + 150, self.image_height - 250, text="Undo", font=("Papyrus", 26), fill='blue',tags = "undoButton")
            self.canvas.create_rectangle(
                self.image_width + 100,
                self.image_height - 150,
                self.image_width + 200,
                self.image_height - 50,
                tags = "saveButton"
            )
            self.canvas.create_text(self.image_width + 150, self.image_height - 100, text="Save", font=("Papyrus", 26), fill='blue', tags = "saveButton")
            self.canvas.tag_bind("undoButton", "<Button-1>", self.undo)
            self.canvas.tag_bind("saveButton", "<Button-1>", lambda event, file = file_name:
            self.save(event,file))

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
            self.canvas = Tk.Canvas(root, width = (self.box_width + self.image_width), height = self.image_height + self.sidebar_height , bg = 'white')
            self.canvas.create_image(self.box_width,0, image = self.photo,anchor='nw', tags = "imageClick")
            
            # undo and save buttons 
            self.canvas.create_rectangle(
                self.image_width - 300,
                self.image_height + 50 ,
                self.image_width - 200,
                self.image_height + 150,
                tags = "undoButton"
            )
            self.canvas.create_text(self.image_width - 250, self.image_height + 100, text="Undo", font=("Papyrus", 26), fill='blue',tags = "undoButton")
            self.canvas.create_rectangle(
                self.image_width - 150,
                self.image_height + 50 ,
                self.image_width - 50,
                self.image_height + 150,
                tags = "saveButton"
            )
            self.canvas.create_text(self.image_width - 100, self.image_height + 100, text="Save", font=("Papyrus", 26), fill='blue', tags = "saveButton")
            self.canvas.tag_bind("undoButton", "<Button-1>", self.undo)
            self.canvas.tag_bind("saveButton", "<Button-1>", lambda event, file = file_name:
            self.save(event,file))
            
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
            self.canvas = Tk.Canvas(root, width = self.image_width + self.sidebar_width, height = (self.box_height + self.image_height), bg = 'white')
            self.canvas.create_image(0,0, image = self.photo,anchor='nw',tags = "imageClick")
            
            # undo and save buttons 
            self.canvas.create_rectangle(
                self.image_width + 100,
                self.image_height - 300,
                self.image_width + 200,
                self.image_height - 200,
                tags = "undoButton"
            )
            self.canvas.create_text(self.image_width + 150, self.image_height - 250, text="Undo", font=("Papyrus", 26), fill='blue', tags = "undoButton")
            self.canvas.create_rectangle(
                self.image_width + 100,
                self.image_height - 150,
                self.image_width + 200,
                self.image_height - 50,
                tags = "saveButton"

            )
            self.canvas.create_text(self.image_width + 150, self.image_height - 100, text="Save", font=("Papyrus", 26), fill='blue',tags = "saveButton")
            self.canvas.tag_bind("undoButton", "<Button-1>", self.undo)
            self.canvas.tag_bind("saveButton", "<Button-1>", lambda event, file = file_name:
            self.save(event,file))

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
            self.canvas = Tk.Canvas(root, width = (self.box_width + self.image_width), height = self.image_height + self.sidebar_height , bg = 'white')
            self.canvas.create_image(0,0, image = self.photo,anchor='nw', tags = "imageClick")
            
            # undo and save buttons 
            self.canvas.create_rectangle(
                self.image_width - 300,
                self.image_height + 50 ,
                self.image_width - 200,
                self.image_height + 150,
                tags = "undoButton"
            )
            self.canvas.create_text(self.image_width - 250, self.image_height + 100, text="Undo", font=("Papyrus", 26), fill='blue',tags = "undoButton")
            self.canvas.create_rectangle(
                self.image_width - 150,
                self.image_height + 50 ,
                self.image_width - 50,
                self.image_height + 150,
                tags = "saveButton"
            )
            self.canvas.create_text(self.image_width - 100, self.image_height + 100, text="Save", font=("Papyrus", 26), fill='blue', tags = "saveButton")
            self.canvas.tag_bind("undoButton", "<Button-1>", self.undo)
            self.canvas.tag_bind("saveButton", "<Button-1>", lambda event, file = file_name:
            self.save(event,file))

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

        self.canvas.tag_bind("imageClick",'<Button-1>',
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
        # check for full palette
        if (self.click_counter == self.grid):
            print('palette is full')
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
        
        # update position
        self.click_counter += 1
    
    def undo(self,event):
        # delete stored color
        del self.colors[-1]
        # update position
        self.click_counter -= 1
        # set rectangle to default
        self.canvas.itemconfigure(self.cubes[self.click_counter], fill='')

    def save(self,event,file_name):
        # save full grids only
        if(self.click_counter != self.grid):
            print('Cannot save incomplete grid. Click more')
            return
            
        self.canvas.update()
        self.canvas.postscript(file=file_name+'.eps')
        img = Image.open(file_name+'.eps')
        img.save(file_name + '-palette-'+ str(self.save_counter)+ '.png', 'png')
        self.save_counter += 1
            
