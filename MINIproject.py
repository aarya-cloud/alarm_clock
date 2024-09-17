import tkinter as tk
from tkinter import Scrollbar, Listbox
from tkinter.ttk import *
from tkinter import Listbox, ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from pygame import mixer
from datetime import datetime
from threading import Thread
from time import sleep
import pytz
import pygame.mixer
from geopy.geocoders import Nominatim

clk=tk.Tk()
clk.geometry('500x400')
clk.title('ALARM CLOCK')

current_indicator = None  # To keep track of the current indicator

def clock_page():
    delete_pages()
    clock_frame=tk.Frame(main_frame)
    lb=tk.Label(clock_frame,text='CLOCK',font=('Bell MT',30))
    lb.pack()
    clock_frame.pack(pady=10)
    IST=pytz.timezone('Asia/Kolkata')
    def update_clock():
       raw_TS=datetime.now(IST)
       date_now=raw_TS.strftime("%d %b, %Y")
       time_now=raw_TS.strftime("%H:%M:%S %p")
       label_date_now.config(text = date_now)
       label_time_now.config(text = time_now)
       label_time_now.after(1000, update_clock)
   
    date_time_frame = tk.Frame(clock_frame, bd=2, relief="groove")
    date_time_frame.pack(pady=60)

    label_time_now = tk.Label(date_time_frame, text="Time", font=('Helvetica', 20))
    label_time_now.pack(pady=5)

    label_date_now = tk.Label(date_time_frame, text="Date", font=('Helvetica', 15))
    label_date_now.pack(pady=5)

    
    update_clock()
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode("Pune")  

    # Display location
    location_label = tk.Label(clock_frame, text=getLoc.address, font=('Arial', 13))
    location_label.pack(pady=10)
    print(getLoc.address)
    clk.mainloop()

alarm_active = False 
style = ttk.Style()
def alarm_page():
    delete_pages()
    def activate_alarm():
        global alarm_active
        alarm_active = True
        alarm_hour = int(c_hour.get())
        alarm_minute = int(c_min.get())
        alarm_period = c_period.get().upper()
        ringtone_selection = ringtone_combobox.get()  # Get the selected ringtone
        acknowledgment_text = f"Alarm set for {alarm_hour}:{alarm_minute:02d} {alarm_period} today with ringtone: {ringtone_selection}"
        messagebox.showinfo("Alarm Set", acknowledgment_text)
        # Start the alarm thread with selected ringtone
        t = Thread(target=alarm, args=(alarm_hour, alarm_minute, alarm_period, ringtone_selection))
        t.start()

    def deactivate_alarm():
        global alarm_active
        alarm_active = False
        mixer.music.stop()

    def sound_alarm(ringtone):
        mixer.init()
        mixer.music.load(ringtone)
        mixer.music.play()

    def alarm(alarm_hour, alarm_minute, alarm_period, ringtone_selection):
        while alarm_active:
            # Get the current time
            raw_time = datetime.now() 
            current_hour = raw_time.strftime("%I")
            current_minute = raw_time.strftime("%M")
            current_period = raw_time.strftime("%p")
            # Check if the current time matches the alarm time
            if (int(current_hour) == alarm_hour and int(current_minute) == alarm_minute and
                    current_period.upper() == alarm_period):
                sound_alarm(ringtone_selection)  # Activate the selected ringtone
                break  # Exit the loop once the alarm goes off

    ALARM_frame = tk.Frame(main_frame)
    lb = tk.Label(ALARM_frame, text='ALARM', font=('Bell MT', 30))
    ALARM_frame.pack(pady=10)
    lb.pack()

    co1 = "#007FFF"  # blue
    co2 ="#00C957"  #green
    co3 = "#FF4040" #red
    frame_line = Frame(main_frame, width=400, height=5)
    frame_line.pack()

    frame_body = Frame(main_frame, width=400, height=300)
    frame_body.pack()

    name = Label(frame_body, font=('Ivy 18 bold'))
    name.place(x=125, y=10)

    hour_label = Label(frame_body, text="Hours", font=('Ivy 10 bold',14), foreground=co1)
    hour_label.place(x=35, y=40)
    c_hour = Combobox(frame_body, width=2, font=('arial 15'))
    c_hour['values'] = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11","12")
    c_hour.current(0)
    c_hour.place(x=40, y=64)

    min_label = Label(frame_body, text="Minutes", font=('Ivy 10 bold',14), foreground=co1)
    min_label.place(x=91, y=40)
    c_min = Combobox(frame_body, width=2, font=('arial 15'))  
    c_min_values = ["{:02d}".format(i) for i in range(60)]  
    c_min['values'] = c_min_values
    c_min.current(0)
    c_min.place(x=105, y=64)

    sec_label = Label(frame_body, text="Seconds", font=('Ivy 10 bold',14), foreground=co1)
    sec_label.place(x=162, y=40)
    c_sec = Combobox(frame_body, width=2, font=('arial 15'))  
    c_sec_values = ["{:02d}".format(i) for i in range(60)]  
    c_sec['values'] = c_sec_values
    c_sec.current(0)
    c_sec.place(x=175, y=64)

    c_period_label = Label(frame_body, text="AM/PM", font=('Ivy 10 bold',14), foreground=co1)
    c_period_label.place(x=245, y=40)
    c_period = Combobox(frame_body, width=3, font=("arial 15"))
    c_period['values'] = ("AM", "PM")
    c_period.place(x=247, y=64)

    ringtone_label = Label(ALARM_frame, text="Select Ringtone:", font=('Ivy 10 bold', 14))
    ringtone_label.pack(pady=(15, 0))

    ringtone_combobox = ttk.Combobox(ALARM_frame, values=["Ringtone-1.mp3", "Ringtone-2.mp3", "Ringtone-3.mp3"])  # Add your ringtone options here
    ringtone_combobox.pack(pady=(5, 5))

    style.configure("Activate.TButton", background="green")
    activate_button = ttk.Button(frame_body, text="Activate", command=activate_alarm,style="Activate.TButton")
    activate_button.place(x=80, y=105)

    style.configure("Deactivate.TButton", background="red")
    deactivate_button = ttk.Button(frame_body, text="Deactivate", command=deactivate_alarm,style="Deactivate.TButton")
    deactivate_button.place(x=180, y=105)

    
    clk.mainloop()
    
pygame.mixer.init()
# Define a global variable to store the sound
timer_sound = None
def timer_page():
    def start_timer(minutes_entry, seconds_entry):
        pass
    def reset_timer():
        pass
    def play_timer_sound():
        pass
    def stop_timer_sound():
        pass
    global timer_sound
    
    def play_timer_sound():
        global timer_sound
        timer_sound = pygame.mixer.Sound("Ringtone-1.mp3")
        timer_sound.play(loops=-1)  # Play the sound in a loop

    def stop_timer_sound():
        global timer_sound
        if timer_sound:
            timer_sound.stop()

    def update_timer(total_seconds):
        minutes, seconds = divmod(total_seconds, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        label.config(text=time_str)
        
        if total_seconds == 0:
            # Timer ends, play the sound
            play_timer_sound()
        elif total_seconds < 0:
            # Timer ended and sound is played, stop the sound
            stop_timer_sound()
        else:
            clk.after(1000, update_timer, total_seconds - 1)

    def start_timer(minutes_entry, seconds_entry):
        minutes = int(minutes_entry.get())
        seconds = int(seconds_entry.get())
        total_seconds = minutes * 60 + seconds
        update_timer(total_seconds)

    def reset_timer():
        minutes_entry.delete(0, tk.END)
        minutes_entry.insert(0, "00")
        seconds_entry.delete(0, tk.END)
        seconds_entry.insert(0, "00")
        label.config(text="00:00")
        stop_timer_sound()

    delete_pages()
    timer_frame=tk.Frame(main_frame)
    lb=tk.Label(timer_frame,text='TIMER',font=('Bell MT',30))
    lb.pack()
    timer_frame.pack(pady=10)
    set_time_frame = tk.Frame(main_frame)
    set_time_frame.pack()

    ttk.Label(set_time_frame, text="Minutes:", font=('Arial', 14)).grid(row=0, column=0, padx=5, pady=5)
    minutes_entry = ttk.Entry(set_time_frame, width=5, font=('Arial', 14))
    minutes_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(set_time_frame, text="Seconds:", font=('Arial', 14)).grid(row=1, column=0, padx=5, pady=5)
    seconds_entry = ttk.Entry(set_time_frame, width=5, font=('Arial', 14))
    seconds_entry.grid(row=1, column=1, padx=5, pady=5)

    global label
    label = ttk.Label(main_frame, text="00:00", font=("Arial", 40))
    label.pack(pady=10)

    # Define the button frame
    button_frame = tk.Frame(main_frame)
    button_frame.pack()
    style = ttk.Style()
    style.configure("Green.TButton", foreground="green")
    style.configure("Red.TButton", foreground="red")

    start_button = ttk.Button(button_frame, text="Start Timer",style="Green.TButton", command=lambda: start_timer(minutes_entry, seconds_entry))
    start_button.pack(side=tk.TOP, padx=5, pady=5)

    reset_button = ttk.Button(button_frame, text="Reset Timer",style="Red.TButton", command=reset_timer)
    reset_button.pack(side=tk.TOP, padx=5, pady=5)

    # Center the button frame horizontally
    button_frame.pack_configure(anchor='center')

is_running = False
start_time = None

def sw_page():
    global is_running, start_time
    delete_pages()
    sw_frame = tk.Frame(main_frame)
    lb = tk.Label(sw_frame, text='STOP WATCH', font=('Bell MT', 30))
    lb.pack()
    sw_frame.pack(pady=10)

    def start_stopwatch():
        global is_running, start_time
        if not is_running:
           is_running = True
           start_time = datetime.now()
           update_time()  
           start_button.config(text="Stop")
        else:
           is_running = False
           start_button.config(text="Start")

    def reset_stopwatch():
        global is_running, start_time
        is_running = False
        start_time = None
        start_button.config(text="Start")
        time_label.config(text="00:00:00")

    def update_time():
        global is_running, start_time
        if is_running:
            elapsed_time = datetime.now() - start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
            time_label.config(text=time_str)
            time_label.after(1000, update_time)

    time_label = tk.Label(main_frame, text="00:00:00", font=("Helvetica", 48))
    time_label.pack(pady=20)

    button_frame = tk.Frame(main_frame)  # Create a frame for buttons
    button_frame.pack()  

    start_frame = tk.Frame(button_frame, highlightbackground="green", highlightthickness=2, bd=0)
    start_frame.pack(side=tk.LEFT, padx=5)
    start_button = tk.Button(start_frame, text="Start", command=start_stopwatch, font=("Arial", 14))
    start_button.pack()

    reset_frame = tk.Frame(button_frame, highlightbackground="red", highlightthickness=2, bd=0)
    reset_frame.pack(side=tk.LEFT, padx=5)
    reset_button = tk.Button(reset_frame, text="Reset", command=reset_stopwatch, font=("Arial", 14))
    reset_button.pack()
    button_frame.pack_configure(anchor='center')

def hid_indicators():
    home_indicate.config(bg='#8EE5EE')
    ALARM_indicate.config(bg='#8EE5EE')
    timer_indicate.config(bg='#8EE5EE')
    sw_indicate.config(bg='#8EE5EE')

def delete_pages():
    for widget in main_frame.winfo_children():
        widget.destroy()

def indicate(lb, page):
    hid_indicators()
    lb.config(bg='#1C86EE')
    page()
    
#OPTIONS
options_frame=tk.Frame(clk,bg='#8EE5EE')

home_btn = tk.Button(options_frame, text='Home', font=('Bold,20'), fg='#000000', bd=2, bg='#FFFFFF', command=lambda: indicate(home_indicate))
home_btn.place(x=15, y=175)

ALARM_btn = tk.Button(options_frame, text='Alarm', font=('Bold,20'), fg='#000000', bd=2, bg='#FFFFFF', command=lambda: indicate(ALARM_indicate, alarm_page))
ALARM_btn.place(x=15, y=225)

timer_btn = tk.Button(options_frame, text='Timer', font=('Bold,20'), fg='#000000', bd=2, bg='#FFFFFF', command=lambda: indicate(timer_indicate, timer_page))
timer_btn.place(x=15, y=275)

sw_btn = tk.Button(options_frame, text='Stop Watch', font=('Bold,20'), fg='#000000', bd=2, bg='#FFFFFF', command=lambda: indicate(sw_indicate, sw_page))
sw_btn.place(x=15, y=325)

#image
img=Image.open('alarm.png')
img.resize((125,125))
img=ImageTk.PhotoImage(img)

app_image=tk.Label(options_frame,height=125,image=img,highlightthickness=1,highlightbackground='black')
app_image.place(x=10,y=10)

home_indicate = tk.Label(options_frame, text='', bg='#8EE5EE')
home_indicate.place(x=12, y=175, width=5, height=40)
home_btn.config(command=lambda: indicate(home_indicate, clock_page))

ALARM_indicate = tk.Label(options_frame, text='', bg='#8EE5EE')
ALARM_indicate.place(x=12, y=225, width=5, height=40)
ALARM_btn.config(command=lambda: indicate(ALARM_indicate, alarm_page))

timer_indicate = tk.Label(options_frame, text='', bg='#8EE5EE')
timer_indicate.place(x=12, y=275, width=5, height=40)
timer_btn.config(command=lambda: indicate(timer_indicate, timer_page))

sw_indicate = tk.Label(options_frame, text='', bg='#8EE5EE')
sw_indicate.place(x=12, y=325, width=5, height=40)
sw_btn.config(command=lambda: indicate(sw_indicate, sw_page))

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=150,height=400)

main_frame=tk.Frame(clk,highlightbackground='gray29',highlightthickness=2)
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=350,height=400)

indicate(home_indicate, clock_page)
clk.mainloop()