import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path

import hashlib
import pandas as pd

#script feito por Luis Nunes

# Set the directory path
directory = 'C:/Users/loc/2022'

# Initialize the file count
file_count = 0


dayTimeSpecs = []

def getDiferential(info):
        if info['endDay'] ==info['startDay']:
                start_dt = datetime.strptime(info['startTime'], "%H:%M")
                end_dt = datetime.strptime(info['endTime'], "%H:%M")
                differential = (end_dt - start_dt).total_seconds() / 60
                #print("Time expended: {:.2f} minutes".format(differential))
                return differential

def createInstance(place, number, dateInfo, hash_value):    
        instance = []
        instance.append(place + ',' + str(number))
        info=GetDayTimeSpecs(dateInfo)
        instance.append(info['startDay'])
        instance.append(info['startTime'])
        instance.append(info['endDay'])
        instance.append(info['endTime'])
        instance.append(getDiferential(info))
        instance.append(getDiferential(info)/60)
        instance.append(hash_value)
        dayTimeSpecs.append(instance)
    

def correctTime(time):
        original_time = time
        minutes = time[3:5]
        side_time = int(time[0:2])-5
        corrected_time = str(side_time) +':' + str(minutes) 
        return corrected_time

def GetDayTimeSpecs(point):
        info = {}
        if 'placeVisit' in point:
                if "startTimestamp" in point['placeVisit']['duration']:
                        #timezone is minus five from the standart used here.
                        start = point['placeVisit']['duration']['startTimestamp']
                        end = point['placeVisit']['duration']['endTimestamp']
                        info['startDay'] = start[0:10]
                        info['startTime'] = correctTime(start[11:16])
                        info['endDay'] = end[0:10]
                        info['endTime'] = correctTime(end[11:16])
                        return info
                       # print (start)
                       # print(end)
                       # print (startDay)
                       # print (startTime)
                       # print(endDay)
                       # print (endTime)
                        
#

def save_curated_data(data):
        # Convert the 2D array to a pandas DataFrame
    df = pd.DataFrame(data, columns=["ENDEREÇO", "DIA", "HORA_ENTRADA", "DIA", "HORA_SAIDA", "TEMPO(Min)", "TEMPO(h)", "SHA-1"])

    # Get the desktop directory
    desktop_path = str(Path.home() / "Desktop")

    # Create the results directory if it doesn't exist
    results_path = os.path.join(desktop_path, "results")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Write the data to an Excel file in the results directory
    file_path = os.path.join(results_path, "curatedData.xlsx")
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=False)

    print(f"Data saved to {file_path}")

    
def initializeRead(data, hash_value):
        
        for point in data:
                #print(type(locations))
                if 'placeVisit' in point:
                        if "address" in point['placeVisit']['location']:
                                
                                
                                pkt = point['placeVisit']['location']['address']
                                Saturn = pkt[0:22]
                                number = pkt[24:28]
                                #print("here")
                                if number.isdigit():
                                        number = int(number)
                                else:
                                        number = 15
                                #print("here 2 ")
                                #print(Saturn)
                                if Saturn == "Av. Saturnino de Brito" and number >=1250 and number <= 1450:
                                        #print (Saturn, number)
                                        #print("Endereço bate")
                                        #GetDayTimeSpecs(point)
                                        createInstance(Saturn, number, point, hash_value)
                        else:
                                print('not have')

# Loop through each file in the directory
for filename in os.listdir(directory):
    # Check if the file is a regular file
    if os.path.isfile(os.path.join(directory, filename)):
        # Increment the file count
        file_count += 1
        
        # Open the file and read its contents
        with open(os.path.join(directory, filename), errors="ignore") as fh:
        # Calculate the SHA-1 hash value of the file contents
                file_contents = fh.read().encode('utf-8')
                hash_value = hashlib.sha1(file_contents).hexdigest()
                
                raw = json.loads(file_contents)
                data = raw['timelineObjects']
                
                initializeRead(data, hash_value)
            


save_curated_data(dayTimeSpecs)

