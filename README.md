# fss_mobile_force_control
Thesis: "Development of a force sensory system for the control and coordination of mobile robots handling fabrics"

## Development of the force sensory system
The developed force sensory system is based on strain gauge-sensing and targeted for the fabric gripper that is presented in:

A 3-Finger Robotic Gripper for Grasping Fabrics Based on Cams-Followers Mechanism

The gripper is suitable for integration with small wheeled mobile robots and can be seen on the following pictures:

<p float="left">
  <img src="https://user-images.githubusercontent.com/75118133/159372939-beaf94a2-fa9c-4b10-b6cc-da1e09dafda9.png" width="300" />
  <img width="10" />
  <img src="https://user-images.githubusercontent.com/75118133/159373044-4143eb60-5efa-44cb-ad3a-6fe17e54c543.png" width="300" /> 
</p>

The developed force sensory system has the following structure:

![image](https://user-images.githubusercontent.com/75118133/159374038-3470c8cd-0274-4bee-ba54-6d72d12e9dba.png)

while the componenets of the measurement chain are:

* 4 strain gauges 350 Ohm Tokyo Instruments FLAB-3-350-11-1LJB-F
* 2 custom made half Wheatstone bridges
* A Load Cell/Wheatstone Shield Amplifier bought by Robotshop. The shield is equipped with an AD8426 mplifier from Analog Devices.
* A Nucleo F334R8 microcontroller.

<p float="left">
  <img src="https://user-images.githubusercontent.com/75118133/159375447-395f4a6d-1de8-4425-b5af-53eb7837ac1e.png" width="400" />
  <img width="10" />
  <img src="https://user-images.githubusercontent.com/75118133/159375021-d0e04246-2cdb-4cbb-838e-31c801a3b4b3.png" width="300" /> 
</p>


## Fabric force control
The FSS presente above was used for cooperative fabric transportation by two wheeled mobile robot in a leader-follower formation. Only the follower is equipped with the FSS and used the provided fabric force feedback to follow the leader.

![image](https://user-images.githubusercontent.com/75118133/159376304-20202a23-c892-4d47-8cb0-8b0c0be8201a.png)

The force control system of the follower is comprised of two parallel PID controllers.
![image](https://user-images.githubusercontent.com/75118133/159375837-40476073-5735-401d-93b3-7df05c143125.png)


[A 3-Finger Robotic Gripper for Grasping Fabrics Based on Cams-Followers Mechanism]: https://link.springer.com/chapter/10.1007/978-3-319-61276-8_64
