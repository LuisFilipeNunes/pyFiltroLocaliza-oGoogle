import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import re 
import hashlib
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk

#script feito por Luis Nunes

def get_differential(start_time, end_time):
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")
        differential = (end_dt - start_dt).total_seconds() / 60
        return differential

def create_instance(place, number, dateInfo, hash_value):    
        instance = []
        instance.append(place + ',' + str(number))
        info=get_day_time_specs(dateInfo)
        instance.append(info['startDay'])
        instance.append(info['startTime'])
        instance.append(info['endTime'])
        instance.append(get_differential(info['startTime'], info['endTime']))
        instance.append(int(get_differential(info['startTime'], info['endTime'])/60))
        instance.append(hash_value)
        dayTimeSpecs.append(instance)

def correctTime(time):
        minutes = time[3:5]
        side_time = int(time[0:2])-5
        corrected_time = str(side_time) +':' + str(minutes) 
        return corrected_time

def get_day_time_specs(point):
        info = {}
        if 'placeVisit' in point:
                if "startTimestamp" in point['placeVisit']['duration']:
                        #timezone is minus five from the standart used here.
                        start = point['placeVisit']['duration']['startTimestamp']
                        end = point['placeVisit']['duration']['endTimestamp']
                        info['startDay'] = start[0:10]
                        info['startTime'] = correctTime(start[11:16])
                        info['endTime'] = correctTime(end[11:16])
                        return info

def show_table(data):
        root = tk.Tk()
        root.title("Tabela de Dados Curados")

        table = ttk.Treeview(root)

        table["columns"]=list(data.columns)
        table["show"]="headings"
        for col in table["columns"]:
                table.heading(col, text=col)

        for index, row in data.iterrows():
                table.insert("",index,values=list(row))

        table.pack(expand=True, fill="both")

        root.mainloop()


def save_curated_data(data):
        df = pd.DataFrame(data, columns=["ENDEREÇO", "DIA", "HORA_ENTRADA", "HORA_SAIDA", "TEMPO(Min)", "TEMPO(h)", "SHA-1"])
        

        desktop_path = str(Path.home() / "Desktop")
        results_path = os.path.join(desktop_path, "results")
        if not os.path.exists(results_path):
                os.makedirs(results_path)
        
       
        # Solicita o nome do arquivo ao usuário
        file_name = input("Digite o nome do relatório para salvar o arquivo (sem extensão): ")
        file_path = os.path.join(results_path, file_name + ".xlsx")
        with pd.ExcelWriter(file_path) as writer:
                df.to_excel(writer, index=False)
        
        print(f"Data saved to {file_path}")
        show_table(df)




def initializeRead(data, hash_value):
        
        for point in data:
                if 'placeVisit' in point:
                        if "address" in point['placeVisit']['location']: 
                                pkt = point['placeVisit']['location']['address']
                                match = re.search(r'Av\.\s+([^\d]+)\s*,\s*(\d+)', pkt)
                                street_name = "ero"
                                if match:
                                        street_name = match.group(1)
                                        street_number = match.group(2)
                                        if street_number.isdigit():
                                                street_number = int(street_number)
                                        else:
                                                street_number = 15
                                if street_name == "Saturnino de Brito" and street_number >=1250 and street_number <= 1450:
                                        create_instance(street_name, street_number, point, hash_value)
                                #else:
                                        #print('...') 

def process_files(directory):
        # Loop through each file in the directory
        for filename in directory:
                # Check if the file is a regular file
                if os.path.isfile(filename):
                        # Open the file and read its contents
                        with open(filename, errors="ignore") as fh:
                        # Calculate the SHA-1 hash value of the file contents
                                file_contents = fh.read().encode('utf-8')
                                hash_value = hashlib.sha1(file_contents).hexdigest()
                                
                                raw = json.loads(file_contents)
                                data = raw['timelineObjects']
                                
                                initializeRead(data, hash_value)

if __name__ == "__main__":
        file_count = 0
        dayTimeSpecs = []
        root = tk.Tk()
        root.withdraw()
        
        file_paths = filedialog.askopenfilenames()
        print(f"{len(file_paths)} arquivos selecionados")
        data = process_files(file_paths)
        save_curated_data(dayTimeSpecs)

