//------------------------------------------
//Dadiotis Ioannis, Robotics Group 2019-2020 
//------------------------------------------
//Code from Mbed online compiler for follower-robot
#include "mbed.h"
#include "Motor.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string>

Motor left(D5, D3, D4);
Motor right(D9, D7, D6);
DigitalIn mybutton(USER_BUTTON);
#define pi 3.141592
AnalogIn f1(A0);
AnalogIn f2(A1);
Timer t;

Serial debug_connection(USBTX,USBRX);
Serial esp8266(D8,D2);

char buffer[100];
const char delim[2]="$";
int volatile size = 0;  
int flag = 1;

typedef struct {
    double right;
    double left;
    }velocity;

void esp8266_initialize(void);
void esp8266_tcp_coonection(void);
void esp8266_send_data(void);
void esp8266_receive_velocities(void);
void esp8266_send_volt(float tt1, float tt2);
velocity parsing_velocities(char* buffer);

int main() 
{   
    float x1, x2;
    wait(1);
    velocity vel;
    
    debug_connection.baud(9600);
    esp8266.baud(115200);
    
    esp8266_initialize();
    wait_ms(500);
    
    esp8266.attach(&esp8266_receive_velocities, Serial::RxIrq); 
    
    //float arra[100][2];   //debug
    
    int i=2;
    
    //t.start();
    
    while(mybutton==1) 
    {
        if (i==80)
            break;
        
        x1=f1.read();
        x2=f2.read();
        
        __disable_irq();
        
        //esp8266_send_data();
        //t.start();
        
        esp8266_send_volt(x1,x2);
        
        wait_ms(2);
        
        __enable_irq();
        
        
        wait_ms(35);    //70
        size = 0;
        
        vel = parsing_velocities(buffer);
        
        left.speed(vel.left);
        right.speed(vel.right);
        
        /*                      //debug
        arra[i][0]=vel.left;    
        arra[i][1]=vel.right;
        
        t.stop();
        printf("time lapsed %f\n",t.read());
        printf("---------------%d------------------\n",i);
        printf("Voltages: %f %f\n", x1, x2);
        printf("Velocities: %f %f\r\n", vel.right, vel.left);
        */
        
        i++;
    }
    left.speed(0);
    right.speed(0);
    
    //t.stop();
    //printf("time lapsed %f\n",t.read());
    
    /*
    for (int k=2; k<100; k++)
    {
        printf("%f  %f\n", arra[k][0], arra[k][1]);
    }
    */
}
    
void esp8266_initialize(void) {
    esp8266.printf("AT+SLEEP=0\r\n");
    wait_ms(50);
    esp8266.printf("AT+CWMODE=1\r\n"); //Station mode
    wait_ms(50);
    esp8266.printf("AT+CIPMUX=0\r\n"); //Single TCP connection
    wait_ms(50);
    esp8266.printf("AT+CIPMODE=0\r\n"); //Normal transmission mode pg 55
    wait_ms(50);
    //esp8266.printf("AT+CWJAP=\"HOME\",\"2613017083@\"\r\n"); //Connects to an Access Point
    wait_ms(2000);
    //esp8266.printf("AT+CIFSR\r\n"); //giannis
     //wait_ms(2000); //giannis
    esp8266_tcp_coonection();
    wait_ms(5);
    esp8266.printf("AT+CIPSEND=3\r\n");
    wait_ms(5);
    esp8266.printf("1\r\n");
}

void esp8266_send_data(void) {
    esp8266_tcp_coonection();
    wait_ms(5);
    esp8266.printf("AT+CIPSEND=3\r\n");
    wait_ms(5);
    esp8266.printf("1\r\n");
}

void esp8266_send_volt(float tt1, float tt2) 
{
    esp8266_tcp_coonection();
    wait_ms(5);
    esp8266.printf("AT+CIPSEND=19\r\n");
    wait_ms(5);
    esp8266.printf("%.6f$%.6f\r\n",tt1, tt2);
}

void esp8266_tcp_coonection(void) {
    esp8266.printf("AT+CIPSTART=\"TCP\",\"192.168.0.103\",3000\r\n"); //Protocol (TCP/UDP/SSL, server ip, server port, tcp keep alive (secs)
    //IP of my desktop
    wait_ms(2);
}

void esp8266_receive_velocities(void) {
    while(esp8266.readable()) {
        buffer[size]=esp8266.getc();
        size++;
        buffer[size]='\0'; 
    }                    
}

//for attach
void esp8266_transmitt_volt(float ttt1, float ttt2)
{
    esp8266.putc('A');
}

velocity parsing_velocities(char* buffer) 
{
    char *tok;
    int tok_num = 0;    
    velocity vel;
    
    tok=strtok(buffer,delim);   
    while( tok != NULL ) 
    {
        tok = strtok(NULL, delim);
        if(tok_num == 0)
        {
            vel.right=atof(tok);   
            tok_num++;
        }
        else if(tok_num == 1) {
            vel.left=atof(tok);
            tok_num++;
        }
    }
    return vel;
}
//AT+CWJAP="TP-LINK_FC11DA","robotsrobotsrobots"
//AT+CIPSTART="TCP","192.168.0.116",3000
//AT+CWJAP="testC","test1234"
//AT+CIPSTART="TCP","192.168.137.1",3000
//AT+CIPSTART="TCP","192.168.1.2",3000
//AT+CWJAP="CONN-X_1514","8ttNk3a1"
//AT+CWJAP="PoirotCafe","agatha118"
//AT+CIPSTART="TCP","192.168.1.119",3000
//AT+CWJAP="Thomson90D1EF","EBBA92A4C7"
//AT+CIPSTART="TCP","192.168.10.12",3000
