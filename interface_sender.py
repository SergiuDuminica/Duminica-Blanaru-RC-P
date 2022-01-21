import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile
import packet
import socket
import sys
import _thread
import time
import udp

from timer import Timer

running = True

global SENDER_ADDR
global RECEIVER_ADDR

global ADRESA_SENDER
global PORT_SENDER
global ADRESA_RECEIVER
global PORT_RECEIVER

global TIMEOUT_INTERVAL
global PACKET_SIZE
global WINDOW_SIZE
global SLEEP_INTERVAL
global filename

# window
window = tk.Tk()

# window icon
# icon = PhotoImage(file="icon3.png")
# window.iconphoto(False, icon)

# window stuff
window.title("Sliding Window Procotol")
#window.geometry('800x600')
window.geometry('1280x720')
window.configure(bg='#555555')

# sender view
label_senderview = tk.Label(window, font=("Calibri", 14), bg='#555555', fg='white', text='SENDER view : ')
label_senderview.place(x=260, y=170)

label_sender = tk.Text(window, state=DISABLED)
label_sender.place(x=90, y=200, width=500, height=400)
scrollbar_views = tk.Scrollbar(window, command=label_sender.yview)
label_sender.config(yscrollcommand=scrollbar_views.set)
scrollbar_views.place(x=590, y=200, width=20, height=400)

def write_sender_view(text):
    label_sender.configure(state='normal')
    label_sender.insert('end', text)
    label_sender.configure(state='disabled')
    label_sender.see('end')

# enter IP for SENDER
label_ipsender = tk.Label(window, bg='#555555', fg='white', text='Introduceti IP SENDER : ')
label_ipsender.place(x=50, y=10)
entry_ipsender = tk.Entry(window)
entry_ipsender.place(x=180, y=10, width=100, height=20)

def enter_ipsender():
    global ADRESA_SENDER
    ip_sender = entry_ipsender.get()
    for i in range(len(ip_sender)):
        if ip_sender[i] not in '0123456789.':
            write_sender_view('Valoarea introdusa pentru IP SENDER nu este valida, incercati alta valoare!\n')
            print("Valoarea introdusa pentru IP SENDER nu este valida, incercati alta valoare!")
            return False
    if ip_sender.count('.') != 3:
        write_sender_view('Valoarea introdusa pentru IP SENDER nu este valida, incercati alta valoare!\n')
        print("Valoarea introdusa pentru IP SENDER nu este valida, incercati alta valoare!")
        return False
    for x in ip_sender.split('.'):
        if int(x) < 0 or int(x) > 255:
            write_sender_view('Valoarea introdusa pentru IP SENDER nu este valida, incercati alta valoare!\n')
            print("Valoarea introdusa pentru IP SENDER nu este valida, incercati alta valoare!")
            return False
    ADRESA_SENDER = ip_sender
    write_sender_view("This is ip Sender: " + ip_sender + "\n")
    print("This is ip Sender: " + ip_sender)
    return True

btn_ips = tk.Button(text="ENTER IP SENDER", bg='#202020', fg="white", command=enter_ipsender)
btn_ips.place(x=90, y=35)

#enter PORT for SENDER
label_portsender = tk.Label(window, bg='#555555', fg='white', text='Introduceti PORT SENDER : ')
label_portsender.place(x=330, y=10)
entry_portsender = tk.Entry(window)
entry_portsender.place(x=480, y=10, width=100, height=20)

def enter_portsender():
    global PORT_SENDER
    global ADRESA_SENDER
    global SENDER_ADDR
    port_sender = entry_portsender.get()
    for i in range (len(port_sender)):
        if port_sender[i] not in '0123456789':
            write_sender_view('Valoarea introdusa pentru PORT SENDER nu este valida, incercati alta valoare!\n')
            print('Valoarea introdusa pentru PORT SENDER nu este valida, incercati alta valoare!')
            print(1)
            return False
    if int(port_sender) > 65535:
        write_sender_view('Valoarea introdusa pentru PORT SENDER nu este valida, incercati alta valoare!\n')
        print('Valoarea introdusa pentru PORT SENDER nu este valida, incercati alta valoare!')
        return False
    if port_sender < '0':
        write_sender_view('Valoarea introdusa pentru PORT SENDER nu este valida, incercati alta valoare!\n')
        print('Valoarea introdusa pentru PORT SENDER nu este valida, incercati alta valoare!')
        print(3)
        return False
    PORT_SENDER = port_sender
    SENDER_ADDR = (str(ADRESA_SENDER), int(PORT_SENDER))
    write_sender_view("This is port Sender: " + port_sender + "\n")
    print("This is port Sender: " + port_sender)
    return True

btn_ports = tk.Button(text="ENTER PORT SENDER", bg='#202020', fg="white", command=enter_portsender)
btn_ports.place(x=420, y=35)

# enter IP for RECEIVER
label_ipreceiver = tk.Label(window, bg='#555555', fg='white', text='Introduceti IP RECEIVER : ')
label_ipreceiver.place(x=660, y=10)
entry_ipreceiver = tk.Entry(window)
entry_ipreceiver.place(x=800, y=10, width=100, height=20)

def enter_ipreceiver():
    global ADRESA_RECEIVER
    ip_receiver = entry_ipreceiver.get()
    for i in range(len(ip_receiver)):
        if ip_receiver[i] not in '0123456789.':
            write_receiver_view("Valoarea introdusa pentru IP RECEIVER nu este valida, incercati alta valoare!\n")
            print("Valoarea introdusa pentru IP RECEIVER nu este valida, incercati alta valoare!")
            return False
    if ip_receiver.count('.') != 3:
        write_receiver_view("Valoarea introdusa pentru IP RECEIVER nu este valida, incercati alta valoare!\n")
        print("Valoarea introdusa pentru IP RECEIVER nu este valida, incercati alta valoare!")
        return False
    for x in ip_receiver.split('.'):
        if int(x) < 0 or int(x) > 255:
            write_receiver_view("Valoarea introdusa pentru IP RECEIVER nu este valida, incercati alta valoare!\n")
            print("Valoarea introdusa pentru IP RECEIVER nu este valida, incercati alta valoare!")
            return False
    ADRESA_RECEIVER = ip_receiver
    write_receiver_view("This is ip Receiver: " + ip_receiver + "\n")
    print("This is ip Receiver: " + ip_receiver)
    return True

btn_ipr = tk.Button(text="ENTER IP RECEIVER", bg='#202020', fg="white", command=enter_ipreceiver)
btn_ipr.place(x=740, y=35)

# enter PORT for RECEIVER
label_portreceiver = tk.Label(window, bg='#555555', fg='white', text='Introduceti PORT RECEIVER : ')
label_portreceiver.place(x=990, y=10)
entry_portreceiver = tk.Entry(window)
entry_portreceiver.place(x=1150, y=10, width=100, height=20)

def enter_portreceiver():
    global ADRESA_RECEIVER
    global PORT_RECEIVER
    global RECEIVER_ADDR
    port_receiver = entry_portreceiver.get()
    for i in range (len(port_receiver)):
        if port_receiver[i] not in '0123456789':
            write_receiver_view("Valoarea introdusa pentru PORT RECEIVER nu este valida, incercati alta valoare!\n")
            print('Valoarea introdusa pentru PORT RECEIVER nu este valida, incercati alta valoare!')
            return False
    if int(port_receiver) > 65535:
        write_receiver_view("Valoarea introdusa pentru PORT RECEIVER nu este valida, incercati alta valoare!\n")
        print('Valoarea introdusa pentru PORT RECEIVER nu este valida, incercati alta valoare!')
        return False
    if port_receiver <'0':
        write_receiver_view("Valoarea introdusa pentru PORT RECEIVER nu este valida, incercati alta valoare!\n")
        print('Valoarea introdusa pentru PORT RECEIVER nu este valida, incercati alta valoare!')
        return False
    PORT_RECEIVER = port_receiver
    RECEIVER_ADDR = (str(ADRESA_RECEIVER), int(PORT_RECEIVER))
    write_receiver_view("This is port Receiver: " + port_receiver + "\n")
    print("This is port Receiver: " + port_receiver)
    return True

btn_portr = tk.Button(text="ENTER PORT RECEIVER", bg='#202020', fg="white", command=enter_portreceiver)
btn_portr.place(x=1070, y=35)

# enter TIMEOUT
label_timeout = tk.Label(window, bg='#555555', fg='white', text='Introduceti TIMEOUT INTERVAL : ')
label_timeout.place(x=4, y=80)
entry_timeout = tk.Entry(window)
entry_timeout.place(x=180, y=80, width=100, height=20)

def enter_timeout():
    global TIMEOUT_INTERVAL
    timeout = entry_timeout.get()
    if (timeout) < '0':
        write_sender_view("Valoarea introdusa pentru TIMEOUT INTERVAL nu este valida, incercati alta valoare!\n")
        print('Valoarea introdusa pentru TIMEOUT INTERVAL nu este valida, incercati alta valoare!')
        return False
    TIMEOUT_INTERVAL = timeout
    write_sender_view("This is Timeout Interval: " + timeout + "\n")
    print("This is Timeout Interval: " + timeout)
    return True

btn_timeout = tk.Button(text="ENTER TIMEOUT", bg='#202020', fg="white", command=enter_timeout)
btn_timeout.place(x=90, y=105)

# enter PACKET SIZE
label_packetsize = tk.Label(window, bg='#555555', fg='white', text='Introduceti PACKET SIZE : ')
label_packetsize.place(x=330, y=80)
entry_packetsize = tk.Entry(window)
entry_packetsize.place(x=480, y=80, width=100, height=20)

def enter_packetsize():
    global PACKET_SIZE
    packetsize = entry_packetsize.get()
    if packetsize < '1':
        write_sender_view("Valoarea introdusa pentru PACKET SIZE nu este valida, incercati alta valoare!\n")
        print('Valoarea introdusa pentru PACKET SIZE nu este valida, incercati alta valoare!')
        return False
    PACKET_SIZE = packetsize
    write_sender_view("This is Packet Size: " + packetsize + "\n")
    print("This is Packet Size: " + packetsize)
    return True


btn_packetsize = tk.Button(text="ENTER PACKET SIZE", bg='#202020', fg="white", command=enter_packetsize)
btn_packetsize.place(x=420, y=105)


# enter WINDOW SIZE
label_windowsize = tk.Label(window, bg='#555555', fg='white', text='Introduceti WINDOW SIZE : ')
label_windowsize.place(x=650, y=80)
entry_windowsize = tk.Entry(window)
entry_windowsize.place(x=800, y=80, width=100, height=20)

def enter_windowsize():
    global WINDOW_SIZE
    windowsize = entry_windowsize.get()
    if windowsize < '1':
        write_sender_view("Valoarea introdusa pentru WINDOW SIZE nu este valida, incercati alta valoare!\n")
        print('Valoarea introdusa pentru WINDOW SIZE nu este valida, incercati alta valoare!')
        return False
    WINDOW_SIZE = windowsize
    write_sender_view("This is Window Size: " + windowsize + "\n")
    print("This is Window Size: " + windowsize)
    return True


btn_windowsize = tk.Button(text="ENTER WINDOW SIZE", bg='#202020', fg="white", command=enter_windowsize)
btn_windowsize.place(x=740, y=105)

# enter SLEEP INTERVAL
label_sleep = tk.Label(window, bg='#555555', fg='white', text='Introduceti SLEEP INTERVAL : ')
label_sleep.place(x=990, y=80)
entry_sleep = tk.Entry(window)
entry_sleep.place(x=1150, y=80, width=100, height=20)

def enter_sleep():
    global SLEEP_INTERVAL
    sleepinterval = entry_sleep.get()
    if sleepinterval < '0':
        print('Valoarea introdusa pentru SLEEP INTERVAL nu este valida, incercati alta valoare!')
        return False
    SLEEP_INTERVAL = sleepinterval
    write_sender_view("This is Sleep Interval: " + sleepinterval + "\n")
    print("This is Sleep Interval: " + sleepinterval)
    return True


btn_sleep = tk.Button(text="ENTER SLEEP INTERVAL", bg='#202020', fg="white", command=enter_sleep)
btn_sleep.place(x=1070, y=105)

# receiver view
label_receiverview = tk.Label(window, font=("Calibri", 14), bg='#555555', fg='white', text='RECEIVER view : ')
label_receiverview.place(x=880, y=170)

label_receiver = tk.Text(window, state=DISABLED)
label_receiver.place (x=700, y=200, width=500, height=400)
scrollbar_viewr = tk.Scrollbar(window, command=label_receiver.yview)
label_receiver.config(yscrollcommand=scrollbar_viewr.set)
scrollbar_viewr.place(x=1200, y=200, width=20, height=400)

def write_receiver_view(text):
    label_receiver.configure(state='normal')
    label_receiver.insert('end', text)
    label_receiver.configure(state='disabled')
    label_receiver.see('end')

# browse button for file to read from
def open_file():
    global filename
    file = tk.filedialog.askopenfile(mode='r')
    if file:
        content = file.read()
        file.close()
        print("%d characters in this file" % len(content))
        print("Fisier selectat!")
    f = str(file).split('/')
    print(f[5])
    f1 = str(f[5]).split("'")
    print(f1[0])
    filename = f1[0]
    write_sender_view("This is the selected file: " + filename + "\n")

btn_browse_sender = tk.Button(window, text="BROWSE FOR FILE TO READ FROM", bg='#202020', fg="white", command=open_file)
btn_browse_sender.place(x=90, y=610)

def start_sender():
    global filename
    global SENDER_ADDR
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    send(sock, filename)
    sock.close()

# start sender button
btn_startsender = tk.Button(window, text="START SENDER", bg='#202020', fg="white", command=start_sender) # TODO start sender
btn_startsender.place(x=390, y=610)

def stop_button():
    global running
    running = False

# stop sender button
btn_stopsender = tk.Button(window, text="STOP SENDER", bg='#202020', fg="white", command=stop_button) # TODO start sender
btn_stopsender.place(x=490, y=610)

# browse button for file to write in
btn_browse_receiver = tk.Button(window, text="BROWSE FOR FILE TO WRITE IN", bg='#202020', fg="white", command=open_file)
btn_browse_receiver.place(x=700, y=610)

# start receiver button
btn_startreceiver = tk.Button(window, text="START RECEIVER", bg='#202020', fg="white", command=open_file) # TODO start receiver
btn_startreceiver.place(x=990, y=610)

# stop receiver button
btn_stopreceiver = tk.Button(window, text="STOP RECEIVER", bg='#202020', fg="white", command=open_file) # TODO start sender
btn_stopreceiver.place(x=1100, y=610)

# watermark
label_prezentare = tk.Label(window,
                bg='#555555',
                text="Proiect realizat de Duminică Sergiu și Blanaru Ioana\nFacultatea de Automatică și Calculatoare Iași, specializarea CTI, an III, grupa 1306A\ncoordonator: Ș.I.dr.ing. Nicolae-Alexandru Botezatu",
                font=("Courier New", 12),
                fg='#FFFFFF',
                justify="center")
label_prezentare.place(relx=0.5, rely=0.95, anchor="center")

base = 0
mutex = _thread.allocate_lock() # returnam un nou thread, initial deblocat
                                # variabila mutex este folosita la sincronizarea threadurilor
def get_send_timer():
    global TIMEOUT_INTERVAL
    send_timer = Timer(TIMEOUT_INTERVAL)
    return send_timer

# Setam dimensiunea ferestrei
def set_window_size(num_packets):
    global base
    global WINDOW_SIZE
    return min(int(WINDOW_SIZE), num_packets - base)


# Trimitem threadul in executie
def send(sock, filename):
    global mutex
    global base
    global RECEIVER_ADDR
    global SENDER_ADDR
    send_timer = get_send_timer()

    try:
        file = open(filename, 'rb')
    except IOError:
        write_sender_view("Unable to open '" + filename + "'\n")
        print('Unable to open', filename)
        return

    # Adaugam toate pachetele in buffer
    packets = []
    seq_num = 0 # variabila ce numara pachetele
    while True:
        data = file.read(int(PACKET_SIZE))
        if not data:
            break
        packets.append(packet.make(seq_num, data))
        seq_num += 1

    num_packets = len(packets)
    write_sender_view("I got: " + str(num_packets) + " packets \n")
    print('I got', num_packets)
    window_size = set_window_size(num_packets)
    next_to_send = 0
    base = 0

    # Dam start threadului ce ii apartine receiverului
    _thread.start_new_thread(receive, (sock,))

    while base < num_packets:
        mutex.acquire() # blocam threadul senderului
        # Trimitem toate pachetele in fereastra
        while next_to_send < base + window_size:
            write_sender_view("Sending packet: " + str(next_to_send) + "\n")
            print('Sending packet', next_to_send)
            udp.send(packets[next_to_send], sock, RECEIVER_ADDR)
            next_to_send += 1

        # Dam start la cronometru
        if not send_timer.running():
            write_sender_view("Starting timer \n")
            print('Starting timer')
            send_timer.start()

        # Asteptam pana se termina cronometru SAU pana primim un raspuns de la receiver
        while send_timer.running() and not send_timer.timeout():
            mutex.release() # deblocam threadul senderului
            write_sender_view("Sleeping \n")
            print('Sleeping')
            time.sleep(int(SLEEP_INTERVAL))
            mutex.acquire() # il blocam iar

        if send_timer.timeout():
            write_sender_view("Timeout \n")
            print('Timeout')
            send_timer.stop();
            next_to_send = base
        else:
            write_sender_view("Shifting window \n")
            print('Shifting window')
            window_size = set_window_size(num_packets)
        mutex.release() # deblocam threadul senderului

    udp.send(packet.make_empty(), sock, RECEIVER_ADDR)
    file.close()


# Threadul receiverului
def receive(sock):
    global mutex
    global base
    send_timer = get_send_timer()
    while True:
        pkt, _ = udp.recv(sock);
        ack, _ = packet.extract(pkt);
        write_sender_view("Got ACK " + str(ack) + "\n")
        print('Got ACK', ack)
        if (ack >= base):
            mutex.acquire()
            base = ack + 1
            write_sender_view("Base updates " + str(base) + "\n")
            print('Base updated', base)
            send_timer.stop()
            mutex.release()

window.mainloop()
