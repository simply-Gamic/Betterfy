import customtkinter as ctk
import socket
import time


# config
WLED_CONTROLLER_IP = "192.168.178.124"
NUM_PIXELS = 50


class WledRealtimeClient:
    def __init__(self, wled_controller_ip, num_pixels, udp_port=21324, max_pixels_per_packet=126):
        self.wled_controller_ip = wled_controller_ip
        self.num_pixels = num_pixels
        self.udp_port = udp_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.red = [255, 0, 0]
        self.blue = [0, 0, 255]
        self.green = [0, 255, 0]

    def update(self, color):
        custom = bytearray(bytes([2, 1]))  # header
        if color == "red":
            for i in range(0, self.num_pixels):
                custom.extend(self.red)
        if color == "blue":
            for i in range(0, self.num_pixels):
                custom.extend(self.blue)
        else:
            for i in range(0, self.num_pixels):
                custom.extend(self.green)
        self._sock.sendto(custom, (self.wled_controller_ip, self.udp_port))
        print("----------------------------------------------------------------------------------------------------------------------------------------- \nSend: " + str(custom), end="\n")


def blink_blue():
    GUI.title.configure(text="Blinking blue now!")
    GUI.title.update()
    wled = WledRealtimeClient(WLED_CONTROLLER_IP, NUM_PIXELS)
    t_end = time.time() + 60 * 0.01
    while time.time() < t_end:
        wled.update("blue")
    GUI.title.configure(text="Finished Test!")


def blink_red():
    GUI.title.configure(text="Blinking red now!")
    GUI.title.update()
    wled = WledRealtimeClient(WLED_CONTROLLER_IP, NUM_PIXELS)
    t_end = time.time() + 60 * 0.01
    while time.time() < t_end:
        wled.update("red")
    GUI.title.configure(text="Finished Test!")


def blink_green():
    GUI.title.configure(text="Blinking green now!")
    GUI.title.update()
    wled = WledRealtimeClient(WLED_CONTROLLER_IP, NUM_PIXELS)
    t_end = time.time() + 60 * 0.01
    while time.time() < t_end:
        wled.update("green")
    GUI.title.configure(text="Finished Test!")


class GUI:
    # settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # app frame
    app = ctk.CTk()
    app.geometry("720x480")
    app.title("Betterfy")

    # adding UI
    title = ctk.CTkLabel(app, text="Test!")
    title.pack(padx=10, pady=10)
    button = ctk.CTkButton(app, text="Blink green", command=blink_green, fg_color="green")
    button.pack(pady=10, padx=10)
    button = ctk.CTkButton(app, text="Blink blue", command=blink_blue, fg_color="blue")
    button.pack(pady=10, padx=10)
    button = ctk.CTkButton(app, text="Blink red", command=blink_red, fg_color="red")
    button.pack(pady=10, padx=10)


GUI.app.mainloop()

