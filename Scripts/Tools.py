import colorama


def ProgressBarColor(current,total,ColorProc=colorama.Fore.YELLOW,ColorComplete=colorama.Fore.GREEN):
    Percent= int(100*(float(current)/float(total)))
    bar="█"*Percent+" "*(100-Percent)
    print(ColorProc+f"\r|{bar}|{Percent}%",end="\r")
    # print("\çn")
    if current in (total,total-1):
        print(ColorComplete+f"\r|{bar}|100%",end="\r")
        print(colorama.Fore.RESET)



def ExportTOCSV(gjPath,exitPath):

    import json
    import csv
    
    
    # Opening JSON file and loading the data
    # into the variable data
    with open(gjPath) as json_file:
        data = json.load(json_file)
    # print(data)
    feature_data = data["features"]
    
    # now we will open a file for writing
    data_file = open(exitPath, 'w')
    
    # create the csv writer object
    csv_writer = csv.writer(data_file)
    
    # Counter variable used for writing
    # headers to the CSV file
    header=['StopCode']
    Check0=feature_data
    Check=Check0[0]['properties']
    if 'CenDeg' in Check:
        header.append('CenDeg')
    if 'Clossnes'in Check:
        header.append('Clossnes')
    if 'Eigen'in Check:
        header.append('Eigen')
    if 'wheelchair_boarding'in Check:
        header.append('wheelchair_boarding')
    print(header)
    print(type(feature_data))
    # print("Check",Check)

    csv_writer.writerow(header)
    # csv_writer.writerow(List)
    # csv_writer.writerow(emp.values())

    for i,Line in enumerate(feature_data):
        ProgressBarColor(current=i,total=len(feature_data))
        # print(Line)

        WorkString=Line['properties']
        # print(WorkString)
        ExitList=[]
        for h in header:
            # print(h,end=",")
            ExitList.append(WorkString[h])
        # print(WorkString)
        # print("")
        # if count == 0:
        # b=input("Delete")
        #     # Writing headers of CSV file
        #     header = emp.keys()
        csv_writer.writerow(ExitList)
        #     count += 1
    
        # # Writing data of CSV file
    
    data_file.close()

if __name__=="__main__":
    # ExportTOCSV(gjPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/Barcelona/Barcelona_Bus.geojson",exitPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/TABLES/Test.csv")

    Path=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/Data.txt"
    FileList=[]
    File = open(Path)
    Lines=File.readlines()
    for line in Lines:
        print(line.rstrip())
        FileList.append(line.rstrip())
    FileList=list(set(FileList))
    print(FileList)  

    for f in FileList:
        name=f.split('/')[-1].split('.')[0]
        print(name)
        exitPath="/mnt/e/GitHub/CAMMM-Tool_1.3/Results/TABLES/"+name+".csv"
        ExportTOCSV(gjPath=f,exitPath=exitPath)