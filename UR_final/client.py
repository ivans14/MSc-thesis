import time
from typing import Tuple

from UR_SiLA_final import Client



def main():
    certificate_authority = open("ca.pem", "rb").read()
    print("adfasdfadf")
    client = Client("127.0.0.1", 50053, root_certs=certificate_authority )

    client.LabwareTransferSiteFestoController.PrepareForInput(
        ("1",2),3,"penfill","pen")
    
    # client.RobotController.ConfigureMainProgram(1,2,1,1,1,1)
    
    print(client.LabwareTransferSiteFestoController.AvailableHandoverPositions.get())


    


if __name__ == "__main__":
    main()
