from datetime import datetime
import csv
import os

def write_time(type_vial,i,j,start_time):
    current_time = datetime.now()
    delta = current_time - start_time
    # milliseconds = int(current_time.strftime("%f")) // 1000  # Convert microseconds to milliseconds
    # time_string = current_time.strftime("%H:%M:%S:") + str(milliseconds).zfill(3)  # Add milliseconds to the time string
    time_list = [type_vial,i,j,delta]
    file_path = os.path.join(os.getcwd(), 'time_decapping.csv')  # Full file path
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(time_list)

