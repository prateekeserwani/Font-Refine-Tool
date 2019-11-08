import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import glob
import fnmatch
import numpy as np
import six
from PIL import Image, ImageDraw, ImageFont
#from check_font import *

class MainWindow(tk.Frame):
    def __init__(self, args, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.list_of_fonts=[]
        self.read_fonts()
        self.font_size=150;
        self.String1 = " 1234567890"
        self.String2 = " - . @ , \" \' : ; $ ! & % + = \\ ( ) [ ] { } < > # "
        self.String3 = "ABCDEFGHIJKLM"
        self.String4 = "NOPQRSTUVWXYZ"
        self.String5 = "abcdefghijklm"
        self.String6 = "nopqrstuvwxyz"

        self.index = 0

        self.font_render()
        self.create_widgets()

    def read_fonts(self):
        for root, dirnames, filenames in os.walk(args.PATH):
            for filename in fnmatch.filter(filenames, '*.ttf'):
                self.list_of_fonts.append(os.path.join(root, filename));

        for root, dirnames, filenames in os.walk(args.PATH):
            for filename in fnmatch.filter(filenames, '*.TTF'):
                self.list_of_fonts.append(os.path.join(root, filename));

        print('NUMBER OF FONTS ==>',len(self.list_of_fonts))

    def create_widgets(self):

        self.var = StringVar()
        self.var.set(str(self.index)+'/'+str(len(self.list_of_fonts)))
        print('......'+str(self.index)+'/'+str(len(self.list_of_fonts)))

        self.myLabel = tk.Label(self, text=self.var)
        self.myLabel.pack()
        
        self.myImage = tk.Label(self, image=self.img)
        self.myImage.pack()
        
        self.myAcceptButton = tk.Button(self, text='Accept', command=self.AccWin)
        self.myRejectButton = tk.Button(self, text='Reject', command=self.RejWin)
        self.myAcceptButton.pack()
        self.myRejectButton.pack()

    def font_render(self):
        font_path = self.list_of_fonts[self.index];
        text_image = np.zeros((3000,5000,3),dtype='uint8')

        # Pass the image to PIL  
        pil_im = Image.fromarray(text_image)  
        draw = ImageDraw.Draw(pil_im)  

        # use a truetype font  
        font = ImageFont.truetype(font_path, self.font_size)

        # Draw the text  
        draw.text((0, 0), self.String1, font=font)    # RGBA

        # Draw the text  
        draw.text((0, 200), self.String2, font=font)    # RGBA

        # Draw the text  
        draw.text((0, 400), self.String3, font=font)    # RGBA

        # Draw the text  
        draw.text((0, 600), self.String4, font=font)    # RGBA


        # Draw the text  
        draw.text((0, 800), self.String5, font=font)    # RGBA

        # Draw the text  
        draw.text((0, 1000), self.String6, font=font)    # RGBA


        w, h = pil_im.size
        scale = max(w, h) / 1024.
        self.img = pil_im.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)

        self.img = ImageTk.PhotoImage(self.img)
        try:
            self.myImage.configure(image=self.img)
        except:
            pass

    def AccWin(self):
        #print('NEXT', self.current_pointer, self.index)  
        font_path = self.list_of_fonts[self.index];
        font_path='\ '.join(font_path.split(' ')) 
        cmd1 = 'cp ' + font_path +' ' +args.selected_font_path+font_path.split(os.sep)[-1]
        print(cmd1)	
        os.system(cmd1) 	
        self.index+=1

        if self.index > len(self.list_of_fonts)-1:
            print ("you have checked all fonts. Thank You ...")
            self.master.destroy()
        self.font_render()
        self.var.set(str(self.index)+'/'+str(len(self.list_of_fonts)))
        print('......'+str(self.index)+'/'+str(len(self.list_of_fonts)))


    def RejWin(self):
        #print('NEXT', self.current_pointer, self.index)  
        font_path = self.list_of_fonts[self.index];
        cmd1 = 'cp ' + font_path +' ' +args.rejected_font_path+font_path.split(os.sep)[-1]
        os.system(cmd1) 	
        self.index+=1

        if self.index > len(self.list_of_fonts)-1:
            print ("you have checked all fonts. Thank You ...")
            self.master.destroy()
        self.font_render()
        self.var.set(str(self.index)+'/'+str(len(self.list_of_fonts)))
        print('......'+str(self.index)+'/'+str(len(self.list_of_fonts)))
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IITR and ISI annotation tool for recognition tasks")
    parser.add_argument("--selected_font_path", type=str,default='./filter/selected/',  help="enter path of input lmdb directory")
    parser.add_argument("--rejected_font_path", type=str,default='./filter/rejected/',  help="enter output directory")
    parser.add_argument("--PATH", type=str,default='./fonts/',  help="enter output directory")
    args = parser.parse_args()
    try:
        os.makedirs(os.path.join(args.selected_font_path))
        os.makedirs(os.path.join(args.rejected_font_path))
    except:
        raise ValueError("could not create output directory. Please remove existing output directory")
    root = tk.Tk()
    root.title("Font checker")
    root.minsize("500", "350")

    mf = MainWindow(args=args, master=root)
    root.mainloop()



