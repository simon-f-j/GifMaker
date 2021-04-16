from tkinter import *
import tkinter
import pyautogui
import datetime
from makegif import combined



class Application():
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        root.attributes("-transparent", "blue")
        root.geometry('220x80+200+200')  # set new geometry
        root.title('Gif grab')
        self.menu_frame = Frame(master, bg="blue")
        self.menu_frame.grid(row = 0, column = 0)

        self.buttonBar = Frame(self.menu_frame)
        self.buttonBar.grid(row = 1, column = 0)

        self.snipButton = Button(self.buttonBar, width=4, command=self.createScreenCanvas, background="green",text="record")
        self.snipButton.grid(row = 2, column = 0)

        
        

        self.scale = Scale(self.buttonBar, from_=5,to=20, orient=tkinter.HORIZONTAL,label="duration",width=10)
        self.scale.set(10)
        self.scale.grid(row = 3, column = 0)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH,expand=YES)

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        x = datetime.datetime.now()
        fileName = x.strftime("%f")
        im.save("snips/" + fileName + ".png")

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH,expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    



    def on_button_release(self, event):
        self.recPosition()
        self.exitScreenshotMode()
        if self.curX > self.start_x and self.curY > self.start_y:
            combined(top=int(self.start_y),left=int(self.start_x),width=int(self.curX-self.start_x),height=int(self.curY-self.start_y))
        elif self.curX > self.start_x and self.curY < self.start_y:
            combined(top=int(self.curY),left=int(self.start_x),width=int(self.curX-self.start_x),height=int(self.start_y-self.curY))
        
        elif self.curX < self.start_x and self.curY < self.start_y:
            combined(top=int(self.curY),left=int(self.curX),width=int(self.start_x-self.curX),height=int(self.start_y-self.curY))
            print("reached elif")

        elif self.curX < self.start_x and self.curY > self.start_y:
            combined(top=int(self.start_y),left=int(self.curX),width=int(self.start_x-self.curX),height=int(self.curY-self.start_y))
            
            
            #print(f"width:{int(self.start_x-self.curX)}, height:{int(self.curY-self.start_y)}")
        #elif self.curX < self.start_x:
            #combined(top=int(self.curY),left=int(self.curX),width=int(self.start_x-self.curX),height=int(self.curY-self.start_y))
            #print(f"width:{int(self.start_x-self.curX)}, height:{int(self.curY-self.start_y)}")
        
        
        return event

    def exitScreenshotMode(self):
        print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()