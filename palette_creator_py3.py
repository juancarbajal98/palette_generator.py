"""
Remade on Mon Feb 22 2021

@author: Juan Carbajal
Program to allow user to enter file name,
have image load,
and click on x different locations (specified with grid param)
after x clicks should be given another button or choice to conclude
and save palette picture
"""
import tkinter as Tk
from PIL import ImageTk, Image 

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
        self.photo = ImageTk.PhotoImage(Image.open(self.file_name))
        self.image_height = self.photo.height()
        self.image_width = self.photo.width()
        self.image_dimensions = {
            "height": self.image_height,
            "width": self.image_width
        }
        self.image_rgb = Image.open(self.file_name).convert('RGB')

        

        # set box dimensions
        if(orientation=='N' or orientation == 'S'):
            self.box_width = self.image_width / self.grid
            self.box_height = 100
        elif(orientation=='W' or orientation == 'E'):
            self.box_height = self.image_height / self.grid
            self.box_width = 100
        
        # resize
        if(
        (self.image_height + self.box_height) >= 1080 and 
        (orientation == 'N' or orientation == 'S' )):
            print('Image height too large - needs resize.')
        if(
        (self.image_width + self.box_width) >= 1920 and 
        (orientation == 'W' or orientation == 'E' )):
            print('Image width too large - needs resize.')
        if(
        (self.image_height >= 1080) and 
        (orientation == 'W' or orientation == 'E' )):
            print('Image height too large - needs resize.')
        if(
        (self.image_height >= 1920) and 
        (orientation == 'S' or orientation == 'N' )):
            print('Image width too large - needs resize.')

        
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

        self.canvas.bind('<Button-1>',self.click)
        root.title('Palette Creator')
        self.canvas.pack()

    def click(self,event):
        print (event.x, event.y)
        # check for out of bounds click 
        if(
            (self.orientation=='N' and event.y <= self.box_height) or
            (self.orientation=='W' and event.x <= self.box_width) or
            (self.orientation=='S' and event.y >= self.image_dimensions["height"]) or
            (self.orientation=='E' and event.x >= self.image_dimensions["width"])
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


if __name__=="__main__":
    file_name = input("Picture file name: ")
    orientation = input("Orientation(N/W/S/E): ")
    # grid = input("Grid #: ")
    root = Tk.Tk()
    grid = 5
    instantiater = App(root,file_name,orientation, grid)
    root.mainloop()