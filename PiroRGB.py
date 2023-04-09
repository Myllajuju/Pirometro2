import tkinter as tk
import cv2 as cv
import PIL.Image, PIL.ImageTk
import matplotlib.pyplot as plt
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

start_time = time.time()

class App:
    global px,py
    #c = []
    #t = 0
    
    
    def __init__(self, window, window_title, video_source = 0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        self.vid = MyVideoCapture(video_source)
        
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0)
        
        self.RFrame = tk.Frame(window, width=600, height = self.vid.height)
        self.RFrame.grid(row=0, column=1)
        
        self.curve = Figure(figsize = (5,5), dpi = 80)
        self.plot1 = self.curve.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.curve, master = self.RFrame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(column = 0, row = 1, sticky = 'SE', padx = 20)
        
        self.px = int(self.vid.width/2)
        self.py = int(self.vid.height/2)
                       
        self.delay = 10
        self.update()
        
        self.window.mainloop()
        
    
        
    def update(self):
        #global t, start_time
        
        #Trabalhar nas mudanças entre frames aqui!
        ret,frame = self.vid.get_frame()
        self.RGB_capture(frame)
        
        #t+=1
        #print(t)
        
                      
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.label = tk.Label(self.canvas, image = self.photo)
            self.label.bind('<Button-1>', self.onclick)
            self.label.grid(column = 0, row = 0)

        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(column = 0, row = 1, sticky = 'SE', padx = 20)
        self.plot1.plot(time.time()-start_time, T, 'r.')
        
        self.window.after(self.delay, self.update)
    
    def onclick(self, event):
        #global px,py

        self.px = event.x
        self.py = event.y
        
    def RGB_capture(self, frame):
        global R,T
        Radius = 10
        R,G,B = [],[],[]

            
        for i in range(1,Radius):
                
            for x in range(self.px-i, self.px+i+1):
                    
                y1 = self.py + ((i**2)-(x-self.px)**2)**(1/2)
                y2 = self.py - ((i**2)-(x-self.px)**2)**(1/2)
                    
                    
                y1,y2 = int(y1), int(y2)
                    
                   
                    
                R.extend((frame[y1,x][0], frame[y2,x][0]))
                G.extend((frame[y1,x][1], frame[y2,x][1]))
                B.extend((frame[y1,x][2], frame[y2,x][2]))
                    
        X = (sum(R)/len(R))/((sum(R)/len(R))+(sum(G)/len(G))+(sum(B)/len(B)))
        T = 1284*(X**2)-2540*X+2133

                
            
            #R,G,B = [int(frame[int(self.vid.height/2),int(self.vid.width/2)][0]),
             #       int(frame[int(self.vid.height/2),int(self.vid.width/2)][1]),
              #      int(frame[int(self.vid.height/2),int(self.vid.width/2)][2])]
            
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame, 'R ' + str(round(sum(R)/len(R),2)), (int(self.vid.width/2), int(self.vid.height/2)), font, 1, (255, 0, 0), 2)
        #cv.putText(frame, 'G ' + str(round(sum(G)/len(G),2)), (int(self.vid.width/2), int(self.vid.height/2)+25), font, 1, (0, 255, 0), 2)
        cv.putText(frame, 'B ' + str(round(sum(B)/len(B),2)), (int(self.vid.width/2), int(self.vid.height/2)+50), font, 1, (0, 0, 255), 2)

        #cv.circle(frame, ((int(self.vid.width/2), int(self.vid.height/2))), Radius, (255,0,0), 2)
        cv.circle(frame, (self.px, self.py), Radius, (255,0,0), 2)
        #self.plot1.plot(time.time()-start_time, round(sum(R)/len(R),2), 'r.')
        #print(t,round(sum(R)/len(R),2), "--- %s seconds ---" % (time.time() - start_time))

class MyVideoCapture():
    def __init__(self, video_source = 0):
        #Abre a camera 0
        self.vid = cv.VideoCapture(video_source)
        #self.vid.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
        #self.vid.set(cv.CAP_PROP_EXPOSURE, 5)
        if not self.vid.isOpened():
            raise ValueError('não foi possível abrir o video', video_source)
        
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
        #print(self.width, self.height)
                
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()
        
    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
            if ret:
                return(ret, cv.cvtColor(frame,cv.COLOR_BGR2RGB))
            else:
                return(ret, None)
        else:
            return (ret, None)

App(tk.Tk(), 'teste')