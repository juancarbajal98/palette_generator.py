import tkinter as Tk
from PIL import ImageTk, Image 


class Buttons:
    def __init__(self, app):
        self.master = app.buttons
        self.app = app
        self.frame = Tk.Canvas(self.master, width =app.sidebar_width, height = app.sidebar_height, bg = "white" )
        self.frame.create_rectangle(
            100,
            25,
            200,
            75,
            tags = "undoButton"
        )
        self.frame.create_text(150, 50,text="Undo", font=("Papyrus", 26), fill='blue',tags = "undoButton")
        self.frame.create_rectangle(
            100,
            125,
            200,
            175,
            tags = "saveButton"
        )
        self.frame.create_text(150, 150,text="Save", font=("Papyrus", 26), fill='blue',tags = "saveButton")
        self.frame.tag_bind("undoButton", "<Button-1>", self.undo)
        self.frame.tag_bind("saveButton", "<Button-1>", lambda event, file = app.file_name_stripped:
        self.save(event,file))
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
    
    def undo(self,event):
        # delete stored color
        del self.app.colors[-1]
        # update position
        self.app.click_counter -= 1
        # set rectangle to default
        self.app.canvas.itemconfigure(self.app.cubes[self.app.click_counter], fill='')

    def save(self,event,file_name):
        # save full grids only
        if(self.app.click_counter != self.app.grid):
            print('Cannot save incomplete grid. Click more')
            return
            
        self.app.canvas.update()
        self.app.canvas.postscript(file=file_name+'.eps')
        img = Image.open(file_name+'.eps')
        img.save(file_name + '-palette-'+ str(self.app.save_counter)+ '.png', 'png')
        self.app.save_counter += 1