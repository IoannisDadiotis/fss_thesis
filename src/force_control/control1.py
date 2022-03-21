#--------------------------------------------------------
#------- Dadiotis Ioannis, Robotics Group 2019-2020-----
#--------------------------------------------------------
import time
from matplotlib import pyplot as plt


class Pid(object):

    def __init__(self):
        self.Pid_var = {
            #15 0.13 198 X modelling
            'Kp': 15, 'Kd': 0.13, 'Ki': 198,#leader PID gains 30 0.35 150 , 25 0.7 130, 25 0.7 50, 25 0.7 10, 15 0.25 80
            'Kp_y': 15, 'Kd_y': 0.13, 'Ki_y': 198,  #7,20,10 / 15 20 0 / 10 7.5 0 / 10 25 0 / 10 60 0 / 10 60 2 / 10 60 15 / 10 60 25 ! / 10 60 35 !/ 10 60 250 / 10 60 100 / 25 70 /110
            'Error_s_x': 0, 'error_prior_x': 0,
            'Error_s_y': 0, 'error_prior_y': 0,
            'dt': 0.055,
            'x_ref': 0.39,'x_ref_inv':0.385, 'y_ref': 0.44
        }
        self.t = 0  #t is used to notice a loop
        self.error_x = []
        self.error_y = []
        self.time_L = []
        self.vleft = []
        self.vright = []

        #sums,priors for debug
        self.sumx = []
        self.sumy = []
        self.priorx = []
        self.priory = []

    def write_data1(self):    #function for writing data of the experiment with only one pid controller

        file = open('error_response.txt', 'w').close() #create txt file for writting and close
        file = open('error_response.txt', 'a+')    #Open for reading and appending (writing at end of file)
        for i in range(len(self.time_L)):
            #file.write(str(self.error[i]) + '  ,  ' + str(self.time_L[i]) + '\n\r')
            file.write(str(self.error_x[i]) + '\r')
        file.close()

        file = open('time_response.txt', 'w').close()
        file = open('time_response.txt', 'a+')
        for i in range(len(self.time_L)):
            # file.write(str(self.error[i]) + '  ,  ' + str(self.time_L[i]) + '\n\r')
            file.write(str(self.time_L[i]) + '\r')
        file.close()

        '''
        with open('time_response.txt', 'a') as file:
            for i in range(len(self.time_L)):
                file.write(str(self.time_L[i]) + '\r')

        with open('error_response.txt', 'a') as file:
            for i in range(len(self.error_x)):
                file.write(str(self.error_x[i]) + '\r')
        '''

        with open('error_response.txt', 'r') as file:
            error = [float(x) for x in file.read().split('\n')[5:-1]]
        with open('time_response.txt', 'r') as file:
            time = [float(x) for x in file.read().split('\n')[5:-1]]

        plt.plot([x - time[0] for x in time], error)
        plt.xlabel('Time (s)')
        plt.ylabel('Error in X')
        plt.title('Kp = {}, Kd = {}, Ki = {}'.format(self.Pid_var['Kp'], self.Pid_var['Kd'], self.Pid_var['Ki']))
        plt.grid()
        axes = plt.gca()
        axes.set_ylim([-0.02, 0.02])
        plt.savefig('x_{}_{}_{}.png'.format(self.Pid_var['Kp'], self.Pid_var['Kd'], self.Pid_var['Ki']))
        plt.show()

        #velocities
        file = open('v_left.txt', 'w').close()
        file = open('v_left.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.vleft[i]) + '\r')
        file.close()

        file = open('v_right.txt', 'w').close()
        file = open('v_right.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.vright[i]) + '\r')
        file.close()

        with open('v_left.txt', 'r') as file:
            v_left = [float(x) for x in file.read().split('\n')[5:-1]]

        with open('v_right.txt', 'r') as file:
            v_right = [float(x) for x in file.read().split('\n')[5:-1]]

        plt.subplot(211)
        plt.plot([x - time[0] for x in time], error)
        plt.xlabel('Time (s)')
        plt.ylabel('error')
        plt.grid()
        plt.subplot(312)
        plt.plot([x - time[0] for x in time], v_left)
        plt.xlabel('Time (s)')
        plt.ylabel('velocity left')
        plt.grid()
        plt.subplot(313)
        plt.plot([x - time[0] for x in time], v_right)
        plt.xlabel('Time (s)')
        plt.ylabel('velocity right')
        plt.grid()
        plt.savefig('velocities')
        plt.show()

    def write_data2(self):      #function for writing data of the experiment with both pid controllers

        #responses
        file = open('error_x_response.txt', 'w').close()
        file = open('error_x_response.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.error_x[i]) + '\r')
        file.close()

        file = open('error_y_response.txt', 'w').close()
        file = open('error_y_response.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.error_y[i]) + '\r')
        file.close()

        file = open('time_response.txt', 'w').close()
        file = open('time_response.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.time_L[i]) + '\r')
        file.close()

        with open('error_x_response.txt', 'r') as file:
            e_x = [float(x) for x in file.read().split('\n')[1:-1]]
        with open('error_y_response.txt', 'r') as file:
            e_y = [float(x) for x in file.read().split('\n')[1:-1]]
        with open('time_response.txt', 'r') as file:
            time = [float(x) for x in file.read().split('\n')[1:-1]]

        plt.plot([x - time[0] for x in time], e_x)
        plt.xlabel("Time (s)")
        plt.ylabel("Error in X")
        plt.title('Kp = {}, Kd = {}, Ki = {}'.format(self.Pid_var['Kp'], self.Pid_var['Kd'], self.Pid_var['Ki']))
        plt.grid()
        axes = plt.gca()
        axes.set_ylim([-0.02, 0.02])
        plt.savefig('x_{}_{}_{}_y_{}_{}_{}.png'.format(self.Pid_var['Kp'], self.Pid_var['Kd'], self.Pid_var['Ki'], self.Pid_var['Kp_y'], self.Pid_var['Kd_y'], self.Pid_var['Ki_y']))
        plt.show()

        plt.plot([x - time[0] for x in time], e_y)
        plt.xlabel("Time (s)")
        plt.ylabel("Error in Y")
        plt.title('Kp = {}, Kd = {}, Ki = {}'.format(self.Pid_var['Kp_y'], self.Pid_var['Kd_y'], self.Pid_var['Ki_y']))
        plt.grid()
        axes = plt.gca()
        axes.set_ylim([-0.01, 0.01])
        plt.savefig('y_{}_{}_{}_x_{}_{}_{}.png'.format(self.Pid_var['Kp_y'], self.Pid_var['Kd_y'], self.Pid_var['Ki_y'], self.Pid_var['Kp'], self.Pid_var['Kd'], self.Pid_var['Ki']))
        plt.show()

        # velocities
        file = open('v_left.txt', 'w').close()
        file = open('v_left.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.vleft[i]) + '\r')
        file.close()

        file = open('v_right.txt', 'w').close()
        file = open('v_right.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.vright[i]) + '\r')
        file.close()

        with open('v_left.txt', 'r') as file:
            v_left = [float(x) for x in file.read().split('\n')[1:-1]]

        with open('v_right.txt', 'r') as file:
            v_right = [float(x) for x in file.read().split('\n')[1:-1]]

        plt.subplot(311)
        plt.plot([x - time[0] for x in time], e_x)
        plt.xlabel('Time (s)')
        plt.ylabel('error X')
        plt.grid()
        plt.subplot(312)
        plt.plot([x - time[0] for x in time], e_y)
        plt.plot([0, 2.05], [0.001, 0.001], 'r', marker='', linewidth='0.5')
        plt.plot([0, 2.05], [-0.001, -0.001], 'r', marker='', linewidth='0.5')
        plt.xlabel('Time (s)')
        plt.ylabel('error Y')
        plt.grid()
        plt.subplot(313)
        plt.plot([x - time[0] for x in time], v_left , 'b', label = 'left')
        plt.plot([x - time[0] for x in time], v_right, 'r', label = 'right')
        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('velocities')
        plt.grid()
        figure = plt.gcf()
        figure.set_size_inches(12, 6)
        plt.savefig('velocities')
        plt.show()

        #errors prior & sums
        file = open('error_x_sum.txt', 'w').close()
        file = open('error_x_sum.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.sumx[i]) + '\r')
        file.close()

        file = open('error_y_sum.txt', 'w').close()
        file = open('error_y_sum.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.sumy[i]) + '\r')
        file.close()

        file = open('error_x_prior.txt', 'w').close()
        file = open('error_x_prior.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.priorx[i]) + '\r')
        file.close()

        file = open('error_y_prior.txt', 'w').close()
        file = open('error_y_prior.txt', 'a+')
        for i in range(len(self.time_L)):
            file.write(str(self.priory[i]) + '\r')
        file.close()

    def forward_control1(self, x, count):       # One pid controller in X direction

        error_x = self.Pid_var['x_ref'] - x

        vel_straight = 0.4

        if count > 1:
            if count <39:  #29#52
                print('Error computed is: {}'.format(error_x))

                '''if error_x > 0.005:
                    vr = 0
                    vl = 0
                else:'''
                dv = self.Pid_var['Kp'] * error_x + self.Pid_var['Kd'] * (error_x - self.Pid_var['error_prior_x']) / self.Pid_var['dt'] + self.Pid_var['Ki'] * self.Pid_var['Error_s_x'] * self.Pid_var['dt']

                if dv > 0.2:
                    dv = 0.2

                elif dv < -0.1:
                    dv = -0.1
                print('dv computed is: {}'.format(dv))

                vr = vel_straight - dv #- 0.01
                vl = vel_straight - dv #- 0.02

                self.Pid_var['error_prior_x'] = error_x
                self.Pid_var['Error_s_x'] += error_x
                print('Counter less than...')
            else:
                vr = 0
                vl = 0

                print('Counter rise')
        else:
            self.Pid_var['x_ref'] = x
            print('x_ref is set to be: {}'.format(self.Pid_var['x_ref']))
            vr = 0
            vl = 0
            print('Counter low')
        print('Control done')
        velocity = '$' + str(format(vr, '.2f')) + '$' + str(format(vl, '.2f')) + '\r\n'

        self.error_x.append(error_x)
        self.time_L.append(time.time())
        #append velocities
        self.vleft.append(format(vl,'.2f'))
        self.vright.append(format(vr,'.2f'))

        return velocity, vr, vl

    def forward_control2(self, x, y, count):        # Both pid controllers in X,Y directions

        error_x = self.Pid_var['x_ref'] - x
        error_y = self.Pid_var['y_ref'] - y

        vel_straight = 0.4

        if count > 1:
            if count < 44: #29#52#39

                print('Error_x computed is: {}'.format(error_x))
                print('Error_y computed is: {}'.format(error_y))

                dv = self.Pid_var['Kp'] * error_x + self.Pid_var['Kd'] * (error_x - self.Pid_var['error_prior_x']) / self.Pid_var['dt'] + self.Pid_var['Ki'] * self.Pid_var['Error_s_x'] * self.Pid_var['dt']

                if abs(error_y) > 0.001:   #0.001
                    dw = self.Pid_var['Kp_y'] * error_y + self.Pid_var['Kd_y'] * (error_y - self.Pid_var['error_prior_y']) / self.Pid_var['dt'] + self.Pid_var['Ki_y'] * self.Pid_var['Error_s_y'] * self.Pid_var['dt']

                    # y_ref change
                    if self.t == 0:
                        self.Pid_var['y_ref'] -= 0.00
                        self.t += 1
                else:
                    dw = 0

                if dv > 0.1:    #check only rise
                    dv = 0.1
                elif dv < -0.1:
                    dv = -0.1

                print('dv computed is: {}'.format(dv))

                vel_total = vel_straight - dv

                if dw > 0.1:
                    dw = 0.1
                elif dw < -0.1:
                    dw = -0.1
                print('dw computed is: {}'.format(dw))

                vr = vel_total - dw
                vl = vel_total + dw

                self.Pid_var['error_prior_x'] = error_x
                self.Pid_var['error_prior_y'] = error_y
                self.Pid_var['Error_s_x'] += error_x
                self.Pid_var['Error_s_y'] += error_y

            else:
                vr = 0
                vl = 0
                print('Counter rise')

        else:
            vr = vl = 0.4
            self.Pid_var['y_ref'] = y
            self.Pid_var['x_ref'] = x
            print('y_ref is set to be: {}'.format(self.Pid_var['y_ref']))
            print('x_ref is set to be: {}'.format(self.Pid_var['x_ref']))
            print('Counter is low')

        print('Control done')
        velocity = '$' + str(format(vr, '.2f')) + '$' + str(format(vl, '.2f')) + '\r\n'

        self.error_x.append(error_x)
        self.error_y.append(error_y)
        self.time_L.append(time.time())

        # append velocities
        self.vleft.append(format(vl, '.2f'))
        self.vright.append(format(vr, '.2f'))

        #append prior,sum
        self.priorx.append(self.Pid_var['error_prior_x'])
        self.sumx.append(self.Pid_var['Error_s_x'])
        self.priory.append(self.Pid_var['error_prior_y'])
        self.sumy.append(self.Pid_var['Error_s_y'])

        return velocity, vr, vl

