//-----------------------------------------------------
//----- Dadiotis Ioannis Robotics Group 2019-2020------
//------------------------------------------------------
//Code from Mbed online compiler

#include "mbed.h"
#include <stdio.h>
#include <string>
#include <iostream>
#include <stdlib.h>

DigitalIn mybutton(USER_BUTTON);
Serial pc(USBTX, USBRX);
AnalogIn f1(A0);
AnalogIn f2(A1);
Timer t;

class F_sensor
{
private:
    float X, Y;
    
public:  
    F_sensor()
        : X(0), Y(0)
    {
    }

    F_sensor(float st1, float st2)
        : X(st1), Y(st2)
    {
    }
    
    void Assign(float s1, float s2)
    {
        X=s1;
        Y=s2;
    }
    
    void Print()
    {
        printf("%f  %f\n", X, Y);
    }
    
    //float[] Return ()
    //{
        //return Y;
     //   return [X,Y]  
    //}
    
    void Save(float* row1, float* row2, int i)
    {
        *(row1+i)=X;
        *(row2+i)=Y;
    }
    
    std::string Conv2string ()
    {
        char string1[9], string2[9];
        sprintf (string1, "%f", X);
        sprintf (string2, "%f", Y);
    
        std::string new_str = "$" + std::string(string1) + "$"+ std::string(string2);
        printf("%s\n",new_str.c_str());
        
        return new_str;
    }
    
};

int main()
{
    F_sensor mysensor;
    //F_sensor mysensor(f1.read(), f2.read());
    float arr[2][500];
    int i=0;
    wait(2);
    do
    {
        if (i==1)
        {
            t.stop();
            printf("Sampling Period is : %f \n",t.read());
        }
        t.start();
        
        mysensor.Assign(f1.read(), f2.read());
        wait(0.1);
        if (mybutton==0)
        {
            printf("\n");
            mysensor.Print();
            //mysensor.Save(arr[0], arr[1], i);
        }
        //std::string string_reading = mysensor.Conv2string();
        
        i++;
        
    }while(1);

    int imax=i;
    
    printf("--------------------------------\n");
    printf("------------PRINT DATA----------\n");
    printf("-------------- X ---------------\n");
    printf("--------------------------------\n");
    
    for (i=0; i<imax; i++)
    {
        printf("%f\n", arr[0][i]);
    }
    
    printf("--------------------------------\n");
    printf("-------------- Y ---------------\n");
    printf("--------------------------------\n");
    
    for (i=0; i<imax; i++)
    {
        printf("%f\n", arr[1][i]);
    }
    
    return 0;
        
}
