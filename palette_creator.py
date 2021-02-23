#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 15:46:03 2020

@author: Juan Carbajal
Program to allow user to enter file name,
have image load (probably onto a TKinter object),
and click on 3-5 different locations
after 3 clicks should be given another button or choice to conclude
where palette picture will appear 
"""
# canvas with empty grid to LHS - eventually let user type where they want grid
# each click fills a square
#   - you can imagine grid size being dynamically updated
# ADD:
#   - undo and redo buttons 
#   - button to create PS
#   - dynamic palette size
import Image, ImageTk
import tkinter as Tk
# needs work
def resize(img):
    # store aspect ratio 
    # mess around with height > 600
    x = img.size[0]
    y = img.size[1]
    if (img.size[0]>500):
        ratio = float(500)/x
        img = img.resize((500,int(float(img.size[1])*ratio)), Image.ANTIALIAS)
    elif (img.size[1] > 650):
        ratio = float(650)/y
        img = img.resize((int(float(img.size[0])*ratio),650), Image.ANTIALIAS)
    print (x,y)
    #ratio = float(650)/x
    print (ratio)
    if (img.size[0] == 0):
        print ("x")
    elif (ratio == 0):
        print ('y')
    # depending on image you either * or /
    return img
    
#import os, subprocess
# helper function that allows a keyword arg to take RGB
def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb
class App(object):
    def __init__(self,root,file_name):
        self.file_name = file_name
        #self.PS_counter = 0
        # grid length 
        self.grid = 5
        # array to store rgb colors
        self.cubes = []
        self.colors = []
        #root window
        root.title('Palette Creator')
        #create jpg & pbm file variables
        self.im_jpg = file_name + '.jpg'
        self.im_pbm = file_name + '.ppm'
        #get image dimensions
        self.im = Image.open(self.im_jpg)
        self.im1 = ImageTk.PhotoImage(self.im)
        if (self.im.size[0] > 500 or self.im.size[1] > 650):
            self.im = resize(self.im)
            self.im1 = ImageTk.PhotoImage(self.im)
        else:
            pass
        self.grid_lengthw = self.im.size[0] * 0.2
        self.grid_lengthh = self.im.size[1] / 5
        #self.cube_height = (self.im.size[1]+(self.grid_lengthh/6)) / 6
        self.cube_height = (self.grid_lengthw)
        # store in RGB to be used in click function
        self.rgb_im = self.im.convert('RGB')
        #create initial canvas
        self.x = Tk.Canvas(root, width = self.im.size[0]+self.grid_lengthw, height = self.im.size[1], bg = 'white')
        # create lines for 5 squares
        for i in range(self.grid):
            self.x.create_line(0,self.grid_lengthh*i,self.grid_lengthw,self.grid_lengthh*i)
        #for i in range(2):
         #   self.x.create_line(100*i,0,100*i,500)
        #create rectangles that overlap with the squares
        for i in range(self.grid):
            self.cubes.append(self.x.create_rectangle(0,i*self.grid_lengthh,self.grid_lengthw,(i+1)*self.grid_lengthh))
        # track number of clicks 
        self.clicker_counter = 0
        # create button
      #  self.undo_button = Tk.Button(root, width = 100, text ='undo', command=self.undo)
        # position button
     #   self.undo_button.place(y=float(self.im.size[1])/2 , x =self.im.size[0]+self.grid_lengthw )
        #pack canvas into a frame
        self.x.pack(expand = True, fill='both')
        #load image
        self.img1 = Tk.PhotoImage(file=self.im_pbm)
        #self.label = Tk.Label(root, image =self.img1)
        #self.label.imaage = self.img1
        # put image into canvas
        self.x.create_image(self.grid_lengthw,0, image=self.im1, anchor='nw')
        # bind to label
        self.x.bind("<Button-1>", self.click)
        self.x.pack()
        
    def click(self,event):
        # returns the x and y pixel position of click
        print (event.x, event.y)
        # takes this x,y position and converts it to
        self.colors.append(self.rgb_im.getpixel((event.x-self.grid_lengthw,event.y)))
        print (self.colors)
        while (self.clicker_counter < self.grid):
            self.x.itemconfigure(self.cubes[self.clicker_counter],fill = _from_rgb((self.colors[self.clicker_counter][0],self.colors[self.clicker_counter][1],self.colors[self.clicker_counter][2])))
            self.clicker_counter += 1
        #once we've clicked enough, we export
        #self.clicker_counter == self.grid
        self.x.update()
            #file_name = self.file_name + "_" + str(self.PS_counter) + ".ps"
            #self.PS_counter += 1
            #ps = 
        self.x.postscript(file=file_name, colormode="color")
            #process = subprocess.Popen(["ps2pdf", "tmp.ps", "result.pdf"], shell=True)
            #process.wait()
            #os.remove("tmp.ps")
    #def undo(self,event):
     #   print 'undo called'
      #  self.x.itemconfigure(self.cubes[self.clicker_counter-1], fill = 'white')
       # self.clicker_counter -= 1
        #self.x.update() vnjkvnfjkbdfnb
    
if __name__=="__main__":
    root = Tk.Tk()
    file_name = input("Picture file name (w/o extension): ")
    instantiater = App(root,file_name)
    root.mainloop()