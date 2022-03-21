#--------------------------------------------------------
#------- Dadiotis Ioannis, Robotics Group 2019-2020-----
#--------------------------------------------------------
import socket
import threading
import time
import math
from control1 import Pid

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.IP_dict = {
            '192.168.0.200': 3,
            '192.168.0.130': 5
        }
        #self.test = {"1": None, "2": None, "3": None} #alternative
        self.vr = 0
        self.vl = 0

    def listen(self):
        self.sock.listen(5)
        i = 0
        while True:

            print(socket.gethostbyname(socket.gethostname()))
            client, address = self.sock.accept()
            if i == 0:
                thread1 = threading.Thread(target=self.listenToClient, args=(client, address))
                thread1.start()
            if i == 1:
                thread2 = threading.Thread(target=self.listenToClient, args=(client, address))
                thread2.start()

            #threading.Thread(target=self.listenToClient, args=(client, address)).start()
            #self.listenToClient(client, address) #replace the above
            i+=1
            print("listening number: {}".format(i))

            if i == 1:  #number of robots
                print('exit program')
                break

        if i == 1:
            thread1.join()
        if i == 2:
            thread1.join()
            thread2.join()

    def listenToClient(self, client, address):
        global pid_inst
        pid_inst=Pid()
        #size = 19
        size=100
        #size = 4
        counter = 0
        #vel1, vel2 = 0, 0
        vel1, vel2 = -0.55, -0.52 #-0.4, -0.5
        voltage_tot = []

        while True:
            print("\n---While loop---")
            try:
                #v = client.recv(4)
                nucleo_data = client.recv(size)
                #print('time for receiving is: {}'.format(time.time()-starttime))
                #msg='1'
                #client.send(msg.encode('utf-8'))
                #totaltime = time.time() - starttime
                #voltage = [float(x) for x in vol.decode().split("$")]
                #if nucleo_data.decode('utf-8') in ['1', '2', '3']: # alternative
                #    if self.test[nucleo_data] is None:
                #        self.test[nucleo_data] = address
                #self.test['1']

                starttime=time.time()
                if counter == 5 :
                    newstarttime = time.time()
                if counter == 6:
                    print('-----Time for one count is {}-----'.format(time.time()-newstarttime))

                voltage = [float(x) for x in nucleo_data.decode().split("$")]

                if (voltage != [1.0]) and self.IP_dict[str(address[0])] == 5:
                    voltage_tot.append(voltage)
                #print('voltage tot is : {}'.format(voltage_tot))

                if nucleo_data:
                    #print("nucleo data received: {}".format(nucleo_data.decode()))
                    print("volt data received: {}".format(voltage))
                    #print('length of voltage total list: ', len(voltage_tot))
                    if self.IP_dict[str(address[0])] == 5:
                        #velocity='${}${}\r\n'.format("%.3f" %vel1,"%.3f" % vel2)
                        #velocity, self.vr, self.vl = pid_inst.forward_control1(voltage[0], counter)
                        velocity, self.vr, self.vl = pid_inst.forward_control2(voltage[0], voltage[1], counter)

                        print('Velocities_3: ' + str(velocity) + 'Connection Address: ' + str(address[0]))
                        client.send(velocity.encode('utf-8'))
                        #vel1 += 0.01
                        #vel2 += 0.01

                    elif self.IP_dict[str(address[0])] == 3:
                        if 2 < counter < 25: #2<counter<38
                            vel1, vel2 = -0.65, -0.5 #-0.57, -0.6

                        elif 24 < counter < 43:
                            vel1, vel2 = -0.5, -0.6

                        elif counter > 42:
                            vel1, vel2 = 0, 0

                        velocity='${}${}\r\n'.format("%.3f" % vel1,"%.3f" % vel2)
                        print('Velocities_3: ' + str(velocity) + 'Connection Address: ' + str(address[0]))
                        client.send(velocity.encode('utf-8'))
                    else:
                        velocity = '$' + str(format(0, '.2f')) + '$' + str(format(0, '.2f')) + '\r\n'
                        client.send(velocity.encode('utf-8'))
                        print('Another IP')
                        print('Velocities_3: ' + str(velocity) + 'Connection Address: ' + str(address[0]))

                    totaltime = time.time() - starttime
                    print('Operation Time:', totaltime)
                else:
                    print("nucleo data not received")
            except Exception as e:
                print(e)
                print('Client Closed from Exception')
                #client.close()
                #return False
            counter += 1
            print("Counter is: {}".format(counter))

            if counter == 45:#53 #40
                break
        if self.IP_dict[str(address[0])] == 5:
            with open('Voltages_X.txt', 'w') as filehandle:
                for listitem in voltage_tot:
                    filehandle.write('%s\n' % listitem[0])
            with open('Voltages_Y.txt', 'w') as filehandle:
                for listitem in voltage_tot:
                    filehandle.write('%s\n' % listitem[1])
            print('save')

        client.close()
        print('Client Closed')

if __name__ == "__main__":

    global pid_inst
    print('initializing server\n')
    t = ThreadedServer('0.0.0.0', 3000)
    print('listening sockets\n')
    t.listen()
    print('diagramm printed')
    #pid_inst.write_data1()
    pid_inst.write_data2()
    print('main executed')
