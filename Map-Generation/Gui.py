from tkinter import Tk, Scale, Button, LabelFrame, Label, Entry, PanedWindow, Frame, DoubleVar, IntVar, StringVar
from PIL import ImageTk


import Perlin_Generation 



def main(height: int, width: int):

    root = Tk()
    #root.geometry("800x600")
    root.configure(width=width, height=height, background='beige')

    # ---------------- Defining tkInter Variables ------------------------ #
    cW_width = 250      # Controls the width of the Control window, where users modify the generator settings.

    # for setting variables within sliders or other modules, they must be tkinter variables.
    seed = StringVar(value="Abracadabara")  # RNG Seed used for the generation of the image
    tk_height = IntVar(value=height)        # Height of the image
    tk_width = IntVar(value=width)          # Width of the image

    scale = IntVar(value=40)                # Actually the level of zoom, unlike octaves
    octaves = IntVar(value=4)               # seems to affect zoom, actually effectively halves the length of a cell, creating more detail
    persistance = DoubleVar(value=.5)       # reduces the strength each successive octave has on the last (reccommend < 1)
    lacunarity = DoubleVar(value=2.0)       # determines octave scaling. (4 octaves with lacu. of 2.0 is 4 layers, each at half the size as the last)

    perlinMap = Perlin_Generation.main(     # perlinMap is the map of values we are retrieving from the perlin_generation. 
        seed=seed.get(), scale=scale.get(), width=tk_width.get(), 
        height=tk_height.get(), octaves=octaves.get(), 
        persistance=persistance.get(), lacunarity=lacunarity.get())
                                            


    # ---------------------------------------------------------- Image Window Set up ------------------------------------------------------------ #
    superWindow = PanedWindow(orient='horizontal', width=(tk_width.get()+cW_width), height=tk_height.get(), bg="beige")
    imageWindow = PanedWindow(superWindow, orient="horizontal", width=tk_width.get(), height=tk_height.get())
    superWindow.add(imageWindow)    # adds image window to the super window

    perlinImage = ImageTk.PhotoImage(image= perlinMap)
    image_label = Label(root, image=perlinImage)
    image_label.pack(side="left", expand=True, fill="both") # place(relx=0, rely=0)   # display the image in the top left corner

    imageWindow.add(image_label)        # add the image to the root window
    
    
    # ---------------- Function for Updating Image, used in control window ------------------------------ #
    def updateButton():
        imageWindow.configure(width=tk_width.get(), height=tk_height.get())

        new_perlinMap = Perlin_Generation.main( seed=seed.get(),            scale=scale.get(),      # this function has a lot of variables. 
                    width=tk_width.get(),       height=tk_height.get(),     octaves=octaves.get(),  # refreshes our perlinMap with the new values
                    persistance=persistance.get(), lacunarity=lacunarity.get())
        
        new_Image = ImageTk.PhotoImage(image= new_perlinMap)
        image_label.configure(image=new_Image)
        image_label.image = new_Image
    
    # ---------------------------------------------------- Control Window Set up ---------------------------------------------------------------- #
    controlWindow = PanedWindow(superWindow, orient="vertical", bg='black', width=cW_width, height=tk_height.get())

    size_frame = Frame(controlWindow, padx=5)        # Frame to contain both width and height
    x_label = LabelFrame(size_frame, text="Width:", width=15, labelanchor='nw')
    x_entry = Entry(x_label, textvariable=tk_width, width=15)
    x_entry.pack()
    y_label = LabelFrame(size_frame, text="Height:", width=15, labelanchor='nw')
    y_entry = Entry(y_label, textvariable=tk_height, width=15)
    y_entry.pack()
    
    x_label.pack(side="left", expand=True)      # pack the width and height labels into the frame
    y_label.pack(side= "right", expand=True)
    controlWindow.add(size_frame, minsize=50)   # add frame to the control window

    
    # -------------------- Labels and Scales for other controllable values --------------------------------------------------- #
    seed_label = LabelFrame(controlWindow, text="Seed", labelanchor='nw')
    seed_entry = Entry(seed_label, textvariable=seed)
    seed_entry.pack(side="top", fill="x")

    scale_label = LabelFrame(controlWindow, text="Scale: (default 40)", labelanchor='nw')
    scale_scale = Scale(scale_label, from_=1, to=160, orient='horizontal', sliderlength=20, variable=scale)
    scale_scale.pack(side="top", fill="x")
    
    octave_label = LabelFrame(controlWindow, text="Octaves: (default 4)", labelanchor='nw')
    octave_scale = Scale(octave_label, from_=1, to=10, orient='horizontal', sliderlength=20, variable=octaves)
    octave_scale.pack(side="top", fill="x")

    pers_label = LabelFrame(controlWindow, text="Persistance: (default 0.5)", labelanchor='nw')
    pers_scale = Scale(pers_label, from_=0, to=2.5, orient='horizontal', sliderlength=20, variable=persistance, resolution=.05)
    pers_scale.pack(side="top", fill="x")

    lacun_label = LabelFrame(controlWindow, text="Lacunarity: (default 2.0)", labelanchor='nw')
    lacun_scale = Scale(lacun_label, from_=0, to=10, orient='horizontal', sliderlength=20, variable=lacunarity, resolution=0.1)
    lacun_scale.pack(side="top", fill="x")

    update = Button(controlWindow, text="update?", command=updateButton, width=100, height=20)

    # --------------------------------------- Control Window Structure Setup-------------------------------------------------- #
    controlWindow.add(seed_label, minsize=40)
    controlWindow.add(scale_label, minsize=60)
    controlWindow.add(octave_label, minsize=60)
    controlWindow.add(pers_label, minsize=60)
    controlWindow.add(lacun_label, minsize=60, height=4000)   # height = height for appearence reasons. prevents update button being massive
    controlWindow.add(update, minsize=40)


    superWindow.add(controlWindow)
    controlWindow.configure(sashwidth=2)

    superWindow.paneconfig(controlWindow, minsize=cW_width)     # Prevent control panel from being crushed by window resize
    # superWindow.paneconfig(imageWindow, minsize=(root.winfo_width()-cW_width))
    superWindow.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    width, height = 600, 600

    main(height, width)

# We could definitely integrate our perlin generator into this, but real time updates would be VERY slow unless we also added GPU 
# computation to the perlin script.

# TODO: Integrate GPU to perlin generation to allow for real time setting updates within the gui

# TODO: Add features to the gui:
    # Color palette selector
    # X and Y panning
    # Image Window minsize updates on Tk window resize.
    # Noise generator selector

