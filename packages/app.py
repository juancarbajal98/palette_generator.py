import tkinter as Tk
from PIL import ImageTk, Image 
from .dimensions import (
    makePhoto, getRGB,
    getImageHeight, getImageWidth
)
from .resize import (
    resizeImage, updateRGB
    )
from .buttons import Buttons

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

# TODO: make image frame appear below (consider smaller square frame), apply logic to E S 

class App(object):
    def __init__(self,file_name):
        # set initial attributes
        self.file_name_stripped = file_name
        self.file_name = file_name + '.jpg'
        self.cubes = []
        self.colors = []
        self.click_counter = 0
        self.save_counter = 0
        # makes canvas 1080 x 1080
        self.max_height = 1080
        self.max_width = 1920
        self.sidebar_height = 0 
        self.sidebar_width = 0 
        self.padding = 40
        self.framing = 14

        # get dimensions from image object
        self.photo = makePhoto(self.file_name)
        self.image_rgb = getRGB(self.file_name)
        self.image_height = getImageHeight(self.photo)
        self.image_width = getImageWidth(self.photo)
        self.ratio = float(self.image_width)/self.image_height
        if(self.ratio <= 0.95):
            self.calc_orientation = 'vertical'
        elif(self.ratio > 0.95 and self.ratio < 1.05):
            self.calc_orientation = 'up_to_user'
        else:
            self.calc_orientation = 'horizontal'
        

    def launchPalette(self, root, direction, grid):
        self.grid = grid 
        self.direction = direction
        self.sidebar_width = 300
        self.sidebar_height = 200

         # get box dimensions
        if(self.direction=='N' or self.direction == 'S'):
            self.box_width = ((self.image_width ) / self.grid) - (2* self.framing)
            self.box_height = self.max_height / 4
        elif(self.direction=='W' or self.direction == 'E'):
            self.box_height = ((self.image_height) / self.grid) - (2*self.framing)
            self.box_width = self.max_height / 4
        
        # resize - TODO: make this iterative (while image dimensions less than frame - should only run twice as much as possible)
        if(
            (self.image_height + self.box_height + (self.framing*3) >= self.max_height) 
            and 
            (self.direction == 'N' or self.direction == 'S')
        ):
            print('Image too large - needs resize')
            self.image_width = self.max_height - (2*self.framing) 
            self.image_height = float(self.image_width) / self.ratio
            self.box_width = self.image_width / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)

        elif(
            (self.image_width + (self.framing*2) >= self.max_height)
            and
            (self.direction == 'N' or self.direction == 'S')
        ):
            print('Image too large - needs resize')
            self.image_width = self.max_height - (2*self.framing) 
            self.image_height = float(self.image_width) / self.ratio
            self.box_width = self.image_width / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        if(
            (self.image_width + self.box_width + (self.framing*3) >= self.max_height)
            and 
            (self.direction == 'W' or self.direction == 'E')
        ):
            print('Image too large - needs resize')
            self.image_height = self.max_height - (2*self.framing) 
            self.image_width = self.ratio * self.image_height
            self.box_height = self.image_height / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)

        elif(
            (self.image_height + (self.framing*2) >= self.max_height)
            and
            (self.direction == 'W' or self.direction == 'E')
        ):
            print('Image too large - needs resize')
            self.image_height = self.max_height - (2*self.framing) 
            self.image_width = self.ratio * self.image_height
            self.box_height = self.image_height / self.grid
            self.photo = resizeImage(self.file_name, self.image_height, self.image_width)
            self.image_rgb = updateRGB(self.file_name, self.image_height, self.image_width)
        
        #create canvases for picture and buttons 
        self.canvas = Tk.Canvas(root, width=self.max_height, height = self.max_height, bg = 'white')
        self.buttons = Tk.Toplevel(root)
        self.buttonWindow = Buttons(self)

        if(self.direction=='N'):
            self.canvas.create_image(self.framing,self.box_height+(self.framing*2), image = self.photo,anchor='nw', tags = "image")
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        self.box_width*i+self.framing,
                        self.framing,
                        self.box_width*(i+1) + self.framing,
                        self.box_height+ self.framing,
                         outline="white"))
            for i in range(self.grid-1):
                self.canvas.create_rectangle(
                    self.box_width*(i+1)+self.framing,
                    self.framing,
                    self.box_width*(i+1)+(self.framing*2),
                    self.box_height+ self.framing,
                    fill="white",
                    outline = "white"
                )
        elif(self.direction=='W'):
            self.canvas.create_image(self.box_width + (2* self.framing),self.framing, image = self.photo,anchor='nw', tags = "image")
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        self.framing,
                        self.box_height*i+self.framing,
                        self.box_height + self.framing,
                        self.box_height*(i+1) + self.framing,
                        outline="white"))
            for i in range(self.grid-1):
                self.canvas.create_rectangle(
                    0,
                    self.box_height*(i+1),
                    self.box_width + self.framing,
                    self.box_height*(i+1)+ self.framing,
                    fill="white",
                    outline = "white"
                )
            
        # elif(self.direction=='E'):
        #     self.canvas.create_image(self.framing,self.framing, image = self.photo,anchor='nw', tags = "image")
        #     for i in range(self.grid):
        #         self.cubes.append(
        #             self.canvas.create_rectangle(
        #                 self.box_width*i+self.framing,
        #                 self.framing,
        #                 self.box_width*(i+1) + self.framing,
        #                 self.box_height+ self.framing, outline="white"))
        #     for i in range(self.grid-1):
        #         self.canvas.create_rectangle(
        #             self.box_width*(i+1)+self.framing,
        #             self.framing,
        #             self.box_width*(i+1)+(self.framing*2),
        #             self.box_height+ self.framing,
        #             fill="white",
        #             outline = "white"
        #         )

        elif(self.direction=='S'):
            self.canvas.create_image(self.framing,self.framing, image = self.photo,anchor='nw', tags = "image")
            for i in range(self.grid):
                self.cubes.append(
                    self.canvas.create_rectangle(
                        self.box_width*i+self.framing,
                        self.image_height+ (2*self.framing),
                        self.box_width*(i+1) + self.framing,
                        self.box_height + self.image_height+ (2*self.framing),
                        outline="white"))
            for i in range(self.grid-1):
                self.canvas.create_rectangle(
                    self.box_width*(i+1)+self.framing,
                    self.image_height+ (2*self.framing),
                    self.box_width*(i+1)+(self.framing*2),
                    self.box_height + self.image_height+ (2*self.framing),
                    fill="white",
                    outline = "white"
                )


        self.canvas.tag_bind("image",'<Button-1>',
            lambda event, file = self.file_name_stripped:
                self.click(event, file))

        root.title('Palette Creator')
        self.canvas.pack()

    def click(self,event,file_name):
        print (event.x, event.y)
        # check for out of bounds  
        if(
            (self.direction=='N' and event.y <= self.box_height) or
            (self.direction=='W' and event.x <= self.box_width) or
            (self.direction=='S' and event.y >= self.image_height) or
            (self.direction=='E' and event.x >= self.image_width)
        ):
            print('out of bounds')
            return
        # check for full palette
        if (self.click_counter == self.grid):
            print('palette is full')
            return        
        # capture  color 
        if(self.direction =='N'):
            self.colors.append(self.image_rgb.getpixel((event.x,event.y-self.box_height)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))
        elif(self.direction == "W"):
            self.colors.append(self.image_rgb.getpixel((event.x-self.box_width,event.y)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))
        elif(self.direction == "S"):
            self.colors.append(self.image_rgb.getpixel((event.x,event.y)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))
        elif(self.direction == "E"):
            self.colors.append(self.image_rgb.getpixel((event.x,event.y)))
            self.canvas.itemconfigure(self.cubes[self.click_counter], fill = _from_rgb((self.colors[self.click_counter][0],self.colors[self.click_counter][1],self.colors[self.click_counter][2])))
        
        # update position
        self.click_counter += 1
            
