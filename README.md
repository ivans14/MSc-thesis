# Optimization in automation design for laboratory liquid handling with a robotic arm

## Background
The current laboratory process involves manually handling repetitive and monotonous tasks, such as decapping vials called Penfills and pouring their contents into larger vials. This decapping process is done using a specialized tool and is time-consuming and labor-intensive, impacting productivity.

Besides the Penfills, other commonly used containers, like pre-filled syringes (PFS), also require manual liquid transfer to similar larger vials. While some automation solutions have been implemented for handling PFS in bulk, these solutions rely on human intervention to load racks with vials and are standalone, isolated systems that lack the flexibility to handle other vial types.

There is a growing need for an automation solution that can autonomously decap Penfills without additional manual intervention and improve the efficiency and robustness of the existing stand-alone automation systems.

## Project Objective
The goal of this project is to optimize the automation of laboratory liquid handling by leveraging a Universal Robots (UR) arm. The solution will be designed to decap Penfill vials and transfer their contents into larger vials without human intervention. Additionally, the project aims to improve existing automation systems to handle various vial types, including PFS, with minimal human interaction, increasing efficiency and throughput in the laboratory.

This automated solution will eliminate the manual labor required for repetitive vial handling tasks, enhance flexibility, and improve overall process reliability.

## Solution overview
The proposed solution automates the manual vial-handling and liquid transfer processes through a robotic station equipped with peripheral tools and a custom-built user interface (UI) designed to interact with the system's SiLA drivers. This solution addresses the inefficiencies of current manual processes by integrating advanced robotics and laboratory automation protocols into a seamless workflow.

### System Prototype for Full Robotic Automation
The system is centered around a Universal Robots (UR5e) arm, which is capable of performing tasks such as vial decapping, liquid transfer, and handling with minimal human intervention. Peripheral tools include a capping and decapping station, a 3D-printed gripper for precise manipulation of lab vials, and a custom-designed liquid transfer system. The entire setup is designed to fit on a laboratory bench, streamlining tasks that are usually performed manually. The robotic arm, in conjunction with these peripheral tools, automates vial processing from start to finish, with the only human input being the provision of empty vials and occasional liquid refills.

### Custom UI for Discovering and Controlling SiLA Drivers
A key part of the solution is the customized user interface that allows users to easily discover, configure, and control the SiLA drivers developed for this system. The SiLA protocol standardizes communication between lab equipment and software, and the custom UI acts as a central control hub for all automation tasks. This UI enables real-time monitoring and interaction with the robotic system, making it possible to schedule tasks, adjust parameters, and view system status at a glance. Through the UI, the user can initiate vial decapping, liquid transfers, and other processes with precision and control, ensuring that the system is adaptable to different laboratory workflows.

### Integration with SiLA Protocol for Seamless Automation
The solution uses SiLA 2 drivers, which have been custom-developed for this robotic setup to enable interoperability and real-time communication between the robot and laboratory infrastructure. These drivers ensure that the robotic arm, peripheral tools, and other devices in the system can be controlled and monitored in a unified manner. The SiLA drivers provide a standardized interface for controlling the robot's actions, enabling smooth operation across different laboratory environments. This level of integration allows for the automation of various vial-handling processes without the need for complex programming or manual adjustments, significantly improving the overall efficiency and scalability of the laboratory setup.

## Media

The following picture and videos demonstrates the solution described
### Complete robotic setup
![image](https://github.com/user-attachments/assets/1abd573b-60f3-4be3-87e4-a5cce7438713)

### Full run with decapping and pooling
https://github.com/user-attachments/assets/ba46888f-f00a-4282-9fad-6213b38c4d6d

### UI demo + decapping only
https://github.com/user-attachments/assets/104b8dd5-33cf-4f2e-95a2-f27065cb975c
