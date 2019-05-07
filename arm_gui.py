import tkinter as tk
import serial.tools.list_ports
import serial

class ArmGui :
    def __init__(self , master):
        self.top_angle = 0
        self.bottom_angle = 0
        self.base_angle = 0

        self.ser = None
        self.connectionState = tk.StringVar()
        self.connectionState.set("Not Connected")

        self.currentAngles = tk.StringVar()
        self.currentAngles.set("Current angles ")

        self.serialInfo = tk.StringVar()
        self.serialInfo.set("Serial Monitoring")

        self.screen_x = 1920
        self.screen_y = 1080
        self.master = master
        master.title('Arm Control Gui')
        master.geometry(str(self.screen_x)+'x'+str(self.screen_y))

        self.textColor = '#053e52'
        self.backgroundColor = '#d3d3d3'
        self.currentLabelColor = '#6600cc'
        self.anglesColor = '#3F3F3F'
        self.btnColor = '#ffe6cc'
        self.btnBgColor ='#404040'
        self.notActivColor = '#ff0000'
        self.activColor = '#00ff00'
        self.exitBtnBgColor = '#660000'
        self.exitTextColor = '#ff6666'
        self.startBtnBgColor = '#009933'
        self.startBtnColor = '#79ff4d'
        self.endBtnBgColor = '#e60000'
        self.endBtnColor = '#ffcccc'
        self.titleColor = '#053e52'
        self.serialInfoColor = '#ffcc00'
        self.serialMonitorColor = '#404040'
        master.configure(background=self.backgroundColor)

        name = tk.Label(master , text='Robot Arm Control' , bg=self.backgroundColor , fg=self.titleColor , font = "Verdana 40 bold")
        name.place(x = self.screen_x/2-250 , y=10)

        start_connection_btn = tk.Button(master , text="Start Connection"  , width = 30, bg=self.startBtnBgColor , fg=self.startBtnColor , font = "Verdana 20 bold" , command = self.start_connection)
        start_connection_btn.place(x = self.screen_x/2-500 , y=90)

        end_connection_btn = tk.Button(master , text="End Connection " , bg=self.endBtnBgColor , fg=self.endBtnColor , width = 30 , font = "Verdana 20 bold" ,  command = self.end_connection)
        end_connection_btn.place(x = self.screen_x/2-200 , y = 150 )

        self.connection_status = tk.Label(master , textvariable = self.connectionState ,bg=self.backgroundColor , fg=self.notActivColor , font = "Verdana 20 bold" )
        self.connection_status.place(x = self.screen_x/2 , y = 220 )

        self.current_angles = tk.Label(master , textvariable = self.currentAngles , bg=self.backgroundColor , fg=self.currentLabelColor ,  font = "Verdana 20 bold" )
        self.current_angles.place(x = self.screen_x/2 , y = self.screen_y - 400 )
        # Link 1 Tag
        self.current_top_label = tk.Label(master , text = "top angle" , bg=self.backgroundColor , fg=self.textColor ,  font = "Verdana 20 ")
        self.current_top_label.place(x = self.screen_x/2-200 , y = self.screen_y-310)
        self.decrease_top_btn = tk.Button(master , text = "-" , bg=self.btnBgColor , fg= self.btnColor ,  font = "Verdana 20 bold" , command = self.decreaseTop)
        self.decrease_top_btn.place(x = self.screen_x/2+60 , y = self.screen_y-310 , height = 35 , width = 35 )
        self.current_top_angle = tk.Label(master , text = self.top_angle  , bg=self.backgroundColor , fg=self.anglesColor , font ="Verdana 20 bold")
        self.current_top_angle.place(x = self.screen_x/2+100 , y = self.screen_y-310 )
        self.increase_top_btn = tk.Button(master , text = "+" , bg=self.btnBgColor , fg= self.btnColor , font = "Verdana 20 bold" , command = self.increaseTop)
        self.increase_top_btn.place(x = self.screen_x/2+165 , y = self.screen_y-310 , height = 35 , width = 35 )
# Link 2 Tag
        self.current_bottom_label = tk.Label(master , text = "bottom angle" , bg=self.backgroundColor , fg=self.textColor , font = "Verdana 20 ")
        self.current_bottom_label.place(x = self.screen_x/2-200 , y = self.screen_y-270)
        self.decrease_bottom_btn = tk.Button(master , text = "-" , bg=self.btnBgColor , fg= self.btnColor , font = "Verdana 20 bold" , command = self.decreaseBottom)
        self.decrease_bottom_btn.place(x = self.screen_x/2+60 , y = self.screen_y-270 , height = 35 , width = 35 )
        self.current_bottom_angle = tk.Label(master , text = self.bottom_angle  , bg=self.backgroundColor , fg=self.anglesColor , font ="Verdana 20 bold")
        self.current_bottom_angle.place(x = self.screen_x/2+100 , y = self.screen_y-270 )
        self.increase_bottom_btn = tk.Button(master , text = "+" , bg=self.btnBgColor , fg= self.btnColor ,  font = "Verdana 20 bold" , command = self.increaseBottom)
        self.increase_bottom_btn.place(x = self.screen_x/2+165 , y = self.screen_y-270 , height = 35 , width = 35 )
# Base Tag
        self.current_base_label = tk.Label(master , text = "base angle" , bg=self.backgroundColor , fg=self.textColor ,  font = "Verdana 20 ")
        self.current_base_label.place(x = self.screen_x/2-200 , y = self.screen_y-230)
        self.decrease_base_btn = tk.Button(master , text = "-" , bg=self.btnBgColor , fg= self.btnColor ,font = "Verdana 20 bold" , command = self.decreaseBase)
        self.decrease_base_btn.place(x = self.screen_x/2+60 , y = self.screen_y-230 , height = 35 , width = 35 )
        self.current_base_angle = tk.Label(master , text = self.base_angle  , bg=self.backgroundColor , fg=self.anglesColor , font ="Verdana 20 bold")
        self.current_base_angle.place(x = self.screen_x/2+100 , y = self.screen_y-230 )
        self.increase_base_btn = tk.Button(master , text="+"  , bg=self.btnBgColor , fg= self.btnColor , font = "Verdana 20 bold"  , command = self.increaseBase)
        self.increase_base_btn.place(x = self.screen_x/2+165 , y = self.screen_y-230 , height = 35 , width = 35)

# Top Angle Control
        self.t_text = tk.Entry(master , font = "Verdana 20 bold" )
        self.t_text.place( x = 1200 , y = 400  , height = 50 , width = 70 )

        send_t_btn = tk.Button(master , text="send" , bg=self.btnBgColor , fg= self.btnColor , font = "Verdana 20 bold" , command = self.send_top_angle)
        send_t_btn.place(x = 1300 , y = 400 , height = 50 , width = 90)
        

# Bottom Angle Control
        self.buttom_text = tk.Entry(master , font = "Verdana 20 bold" )
        self.buttom_text.place( x = 1200 , y = 500  , height = 50 , width = 70 )

        send_buttom_btn = tk.Button(master , text="send" , bg=self.btnBgColor , fg= self.btnColor , font = "Verdana 20 bold" , command = self.send_buttom_angle)
        send_buttom_btn.place(x = 1300 , y = 500 , height = 50 , width = 90)

# Base Angle Control
        self.base_text = tk.Entry(master , font = "Verdana 20 bold" )
        self.base_text.place( x = 1200 , y = 600  , height = 50 , width = 70 )

        send_base_btn = tk.Button(master , text="send" , bg=self.btnBgColor , fg= self.btnColor , font = "Verdana 20 bold" , command = self.send_base_angle)
        send_base_btn.place(x = 1300 , y = 600 , height = 50 , width = 90)

        exit_btn = tk.Button(master ,text="Exit", width = 30, bg=self.exitBtnBgColor  , fg=self.exitTextColor,  font = "Verdana 20 bold" ,  command=self.quit)
        exit_btn.place(x = self.screen_x/2-200 , y=self.screen_y-150)

        self.serialMonitor = tk.Label(master , text = "serial mointor" , bg=self.backgroundColor , fg=self.serialMonitorColor , font="Verdana 15 bold")
        self.serialMonitor.place(x = self.screen_x - 550 , y = self.screen_y - 360 )

        self.serial_info = tk.Label(master , textvariable = self.serialInfo , bg=self.backgroundColor , fg=self.serialInfoColor ,  font = "Verdana 15 " )
        self.serial_info.place(x = self.screen_x - 550 , y = self.screen_y - 300 )
        # ###################

    def increaseTop(self):
        try :
            if self.top_angle < 180 :
                self.top_angle = self.top_angle + 1
                self.ser.write( ('3/'+str(self.top_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                print("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                self.current_top_angle.configure(text = str(self.top_angle))
            else :
                self.top_angle = 0
                self.ser.write( ('3/'+str(self.top_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                print("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                self.current_top_angle.configure(text = str(self.top_angle))
        except :
            print("connection dosen't established yet ")

    def decreaseTop(self):
        try :
            if self.top_angle > 0 :
                self.top_angle = self.top_angle - 1
                self.ser.write( ('3/'+str(self.top_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                print("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                self.current_top_angle.configure(text = str(self.top_angle))
            else :
                self.top_angle = 0
                self.ser.write( ('3/'+str(self.top_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                print("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
                self.current_top_angle.configure(text = str(self.top_angle))
        except :
            print("connection dosen't established yet ")

    def increaseBottom(self):
        try :
            if self.bottom_angle < 180 :
                self.bottom_angle = self.bottom_angle + 1
                self.ser.write(('2/'+str(self.bottom_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to bottom successfully  ".format(str(self.bottom_angle)))
                print("angle [ {} ] sent to bottom successfully  ".format(str(self.bottom_angle)))
                self.current_bottom_angle.configure(text = str(self.bottom_angle))
            else :
                self.bottom_angle = 0
                self.ser.write(('2/'+str(self.bottom_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to bottom successfully  ".format(str(self.bottom_angle)))
                print("angle [ 0 ] sent to bottom successfully  ")
                self.current_bottom_angle.configure(text = str(self.bottom_angle))
        except :
            print("connection dosen't established yet ")

    def decreaseBottom(self):
        try :
            if self.bottom_angle > 0 :
                self.bottom_angle = self.bottom_angle - 1
                self.ser.write(('2/'+str(self.bottom_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to bottom successfully  ".format(str(self.bottom_angle)))
                print("angle [ 0 ] sent to bottom successfully  ")
                self.current_bottom_angle.configure(text = str(self.bottom_angle))
            else :
                self.bottom_angle = 0
                self.ser.write(('2/'+str(self.bottom_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to bottom successfully  ".format(str(self.bottom_angle)))
                print("angle [ 0 ] sent to bottom successfully  ")
                self.current_bottom_angle.configure(text = str(self.bottom_angle))
        except :
            print("connection dosen't established yet ")

    def increaseBase(self):
        try :
            if self.base_angle < 180 :
                self.base_angle = self.base_angle + 1
                self.ser.write(('1/'+str(self.base_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                print("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                self.current_base_angle.configure(text=str(self.base_angle))
            else :
                self.base_angle = 0
                self.ser.write(('1/'+str(self.base_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                print("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                self.current_base_angle.configure(text=str(self.base_angle))
        except :
            print("connection dosen't established yet ")

    def decreaseBase(self):
        try :
            if self.base_angle > 0 :
                self.base_angle = self.base_angle - 1
                self.ser.write(('1/'+str(self.base_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                print("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                self.current_base_angle.configure(text=str(self.base_angle))
            else :
                self.base_angle = 0
                self.ser.write(('1/'+str(self.base_angle)).encode())
                self.serialInfo.set("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                print("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
                self.current_base_angle.configure(text=str(self.base_angle))
        except :
            print("connection dosen't established yet ")

    # ################

    def send_top_angle(self):
        try :
            angle = int(self.t_text.get())
            self.top_angle = angle
            self.ser.write( ('3/'+str(self.top_angle)).encode())
            self.current_top_angle.configure(text=str(self.top_angle))
            self.serialInfo.set("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
            print("angle [ {} ] sent to top successfully ".format(str(self.top_angle)))
        except :
            if( self.ser == None ) :
                print("Connection isn't established yet !")
            elif ( self.ser.isOpen() and self.t_text.get()==''):
                print("Enter angle Please !")
            else :
                print("Numeric Values Only Accepted ! ")

    def send_buttom_angle(self) :
        try :
            angle = int(self.buttom_text.get())
            self.bottom_angle = angle
            self.ser.write( ('2/'+str(self.bottom_angle)).encode())
            self.current_bottom_angle.configure(text=str(self.bottom_angle))
            self.serialInfo.set("angle [ {} ] sent to bottom successfully ".format(str(self.bottom_angle)))
            print("angle [ {} ] sent to bottom successfully ".format(str(self.bottom_angle)))
        except :
            if( self.ser == None ) :
                print("Connection isn't established yet !")
            elif ( self.ser.isOpen() and self.buttom_text.get()==''):
                print("Enter angle Please !")
            else :
                print("Numeric Values Only Accepted ! ")

    def send_base_angle(self) :
        try :
            angle = int(self.base_text.get())
            self.base_angle = angle
            self.ser.write(('1/'+str(self.base_angle)).encode())
            self.serialInfo.set("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
            self.current_base_angle.configure(text=str(self.base_angle))
            print("angle [ {} ] sent to base successfully ".format(str(self.base_angle)))
        except :
            if( self.ser == None ) :
                print("Connection isn't established yet !")
            elif ( self.ser.isOpen() and self.base_text.get()==''):
                print("Enter angle Please !")
            else :
                print("Numeric Values Only Accepted ! ")

    def start_connection(self):
        ports = list(serial.tools.list_ports.comports())
        flag = 0
        port =''
        for p in ports :
            if 'Arduino' in str(p) :
                flag = 1
                port = str(p).split('-')[0]
                self.ser = serial.Serial( port , 9600)
                print(" connected at : " + str(p).split('-')[0] )
                self.connectionState.set(" Connected at : " + str(p).split('-')[0] )
                self.connection_status['fg'] = self.activColor

        if flag == 0 :
            self.connectionState.set("Arduino Not Found" )
            print("Not Found !")

    def end_connection(self):
        try :
            if self.ser.isOpen():
                self.ser.close()
                self.connectionState.set("Disconnected")
                self.connection_status['fg'] = self.notActivColor
                print("connection closed successfully ")
            else :
                self.connection_status['fg'] = self.notActivColor
                self.connectionState.set("Already Disconnected !")
                print("Already Closed .....")
        except :
            self.connectionState.set("connection isn't created yet !")
            self.connection_status['fg'] = 'red'
            print("Serial Object is not created yet !")

    def display_current_angles(self):
            self.connection_status = tk.Label(master , textvariable = self.connectionState ,  font = "Verdana 20 bold" )
            self.connection_status.place(x = self.screen_x/2 , y = 220 )

    def quit(self):
        exit()

if __name__=='__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    ArmGui(root)
    root.mainloop()