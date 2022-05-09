from tkinter import *
import serial
import serial.tools.list_ports
import threading
from PIL import Image, ImageTk
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

data = []
x = np.array([])
y = np.array([])
x2 = np.array([])
y2 = np.array([])
cnt = 0

    
class Graphics():
    pass

def connect_menu_init():
    global root, graph, fig, ax, ax2, canvas, lines, lines2, canvas2
    global connect_btn, refresh_btn
    root = Tk()
    root.title("EKG Application")
    root.geometry("1500x800")
    root.config(bg="white")
    root.state('zoomed')
    root.iconbitmap('h1.ico')
    
    port_label = Label(root, text="Avaible Ports: ", bg="white")
    port_label.grid(column=1, row=2, pady=20, padx=10)
    
    port_bd = Label(root, text="BaudRate: ", bg="white")
    port_bd.grid(column=1, row=3, pady=20, padx=10)
    
    scale_lbl = Label(root, text="Monitor Scaling", bg="white")
    scale_lbl.grid(column=1, row=4, pady=20, padx=10)
    
    refresh_btn = Button(root, text="Refresh", height=2, width=10, command=update_coms)
    refresh_btn.grid(column=3, row=2)
    
    connect_btn = Button(root, text="Connect", height=2, width=10, state="disabled", command=connection)
    connect_btn.grid(column=3, row=3)
    baud_select()
    update_coms()
    scale_select_min()
    scale_select_max()
    scale_select_min2()
    scale_select_max2()
    
    
    plt.close('all')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('EKG Monitor')
    ax.set_ylabel('Heart Signal')
    ax.set_xlabel('Time')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 30)
    #plt.grid(True)
    lines = ax.plot([], [], color='red')[0]
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_title('Blood Presure Monitor')
    ax2.set_ylabel('Blood Signal')
    ax2.set_xlabel('Time')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 30)
    lines2 = ax2.plot([], [], color='blue')[0]

    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=500, y=10, width=1400, height=400)
    canvas.draw()
    
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2.get_tk_widget().place(x=500, y=420, width=1400, height=400)
    canvas2.draw()
    
def scale_select_min():
    global clicked_scale_min, drop_scale_min
    clicked_scale_min = StringVar()
    
    
    scl_opt_min = ["0", "-50", "-100", "-300", "-500"]
    
    
    clicked_scale_min.set(scl_opt_min[0])
    
    
    drop_scale_min = OptionMenu(root, clicked_scale_min, *scl_opt_min, command=scale_set)
    drop_scale_min.config(width=10)
    drop_scale_min.grid(column=1, row=5, padx=10)
    

    
def scale_select_max():
    global clicked_scale_max, drop_scale_max
    clicked_scale_max = StringVar()
    
    scl_opt_max = ["30", "50", "100", "300", "500", "800", "1000"]
    clicked_scale_max.set(scl_opt_max[0])
    
    drop_scale_max = OptionMenu(root, clicked_scale_max, *scl_opt_max, command=scale_set)
    drop_scale_max.config(width=10)
    drop_scale_max.grid(column=2, row=5, padx=10)
    
def scale_select_min2():
    global clicked_scale_min2, drop_scale_min2
    clicked_scale_min2 = StringVar()
    
    
    scl_opt_min2 = ["0", "100", "300", "500", "-50", "-100", "-300", "-500"]
    
    
    clicked_scale_min2.set(scl_opt_min2[0])
    
    
    drop_scale_min2 = OptionMenu(root, clicked_scale_min2, *scl_opt_min2, command=scale_set)
    drop_scale_min2.config(width=10)
    drop_scale_min2.grid(column=1, row=6, padx=10)
    

    
def scale_select_max2():
    global clicked_scale_max2, drop_scale_max2
    clicked_scale_max2 = StringVar()
    
    scl_opt_max2 = ["30", "50", "100", "300", "500", "1000"]
    clicked_scale_max2.set(scl_opt_max2[0])
    
    drop_scale_max2 = OptionMenu(root, clicked_scale_max2, *scl_opt_max2, command=scale_set)
    drop_scale_max2.config(width=10)
    drop_scale_max2.grid(column=2, row=6, padx=10)
    
def baud_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-", "2400", "9600", "115200"]
    clicked_bd.set(bds[0])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command=connect_check)
    drop_bd.config(width=20)
    drop_bd.grid(column=2, row=3, padx=50)
    
def update_coms():
    global clicked_com, drop_com
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0,"-")
    try:
        drop_com.destroy()
    except:
        pass
    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_com = OptionMenu(root, clicked_com, *coms, command=connect_check)
    drop_com.config(width=20)
    drop_com.grid(column=2, row=2, padx=50)
    connect_check(0)
    
def scale_set(args):
    ax.set_ylim(int(clicked_scale_min.get()), int(clicked_scale_max.get()))
    ax2.set_ylim(int(clicked_scale_min2.get()), int(clicked_scale_max2.get()))
    canvas.draw()
    canvas2.draw()
    
def connect_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"
        
def connection():
    global ser, serialData, t3
    if connect_btn["text"] in "Disconnect":
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_com["state"] = "active"
        serialData = False
        if ser.in_waiting:
            ser.reset_input_buffer()
            ser.close()
    else:
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disable"
        drop_bd["state"] = "disable"
        drop_com["state"] = "disable"
        serialData = True
        port = clicked_com.get()
        baud = clicked_bd.get()
        cnt = 0
        try:
            ser = serial.Serial(port,baud,timeout=0)
        except:
            pass
        t1 = threading.Thread(target=read_serial)
        t1.deamon = True
        t1.start()
        
    
    
def read_serial():
    global serialData, graph, plot1, plot2, t3, t2
    while serialData:
        if serialData:
            if(ser.in_waiting):
                if ser.read() == b'A' :
                    while ser.in_waiting < 5:
                        pass
                    byte = ser.read(4)
                    check = ser.read(1)
                    print(check)
                    print('Byte: ')
                    print(byte)
                    if check == b'#':
                        sensor1 = int.from_bytes(byte, "little", signed=False)
                        plot = sensor1

                        print('Sensor1: ')
                        print(sensor1)
                        global lines, y, x
                        if(len(y) < 100):
                            y = np.append(y, plot)
                        else:
                            y[0:99] = y[1:100]
                            y[99] = plot
                        x = np.append(x, np.arange(0,len(y)))
                        lines.set_xdata(np.arange(0,len(y)))
                        lines.set_ydata(y)
                        canvas.draw()
        if serialData:
            if(ser.in_waiting):
                if ser.read() == b'B' :
                    while ser.in_waiting < 5:
                        pass
                    byte = ser.read(4)
                    check = ser.read(1)
                    print(check)
                    print('Byte: ')
                    print(byte)
                    if check == b'#':
                        sensor2 = int.from_bytes(byte, "little", signed=True)
                        plot2 = sensor2

                        print('Sensor2: ')
                        print(sensor2)
                        global lines2, y2, x2
                        if(len(y2) < 100):
                            y2 = np.append(y2, plot2)
                        else:
                            y2[0:99] = y2[1:100]
                            y2[99] = plot2
                        x2 = np.append(x2, np.arange(0,len(y2)))
                        lines2.set_xdata(np.arange(0,len(y2)))
                        lines2.set_ydata(y2)
                        canvas2.draw()

            

                
                
connect_menu_init()
root.mainloop()