#----------------------------------------------------------##
#        Name: TIFX04-22-82, DataProcessing LEMA
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-22, 13:55
#     Updated: 2022-04-28, 17:25
#       About: Takes in CSV-data från Qualisys measurement
#              and applies gaussian filter and excecutes a
#              numerical derivative to get velocity
#              Saves processed data to another CSV-file
##---------------------------------------------------------##



import os
import csv
import pandas as pd                     # for CSV
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


## CSV_handler ##
CSV_DELIMITER = ','

def read_CSV(readFilePath):
    #requires: "import pandas as pd"
    CSV =  pd.read_csv(readFilePath, sep=CSV_DELIMITER)
    print("DONE: Read CSV: " + readFilePath)
    return CSV

def get_CSV_header(CSV_data):
    return CSV_data.columns.values

def write_data_to_CSV(filenamePath, header, data):
    # requires: "import csv"
    with open(filenamePath, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator='\n')
        csvwriter.writerow(header)
        csvwriter.writerows(data)
    print("DONE: Write data to CSV-file: "+str(filenamePath))



## DATA PROCESSING ##

def remove_zeroValues(position, time):#, *frame): #frame removed, 2022-04-27
    position_noZeroes = []
    time_noZeroes = []
    #frame_noZeroes = []

    for i in range(len(position)):
        if position[i] != 0.000:
            position_noZeroes.append(position[i])
            time_noZeroes.append(time[i])
            #frame_noZeroes.append(frame[i])
    
    #print("DONE: Removed values with '0.000' from position and time vectors")
    return position_noZeroes, time_noZeroes#, frame_noZeroes

def gaussianFilter1D(array1D, sigma):
    #print("DONE: Filtered data with sigma="+str(sigma))
    return gaussian_filter1d(array1D, sigma)


# FILE PATHS #

def get_filePaths_ofFilenames_inFolder(filePathToFolder, filenames):
    filePaths = []
    for i in range(len(filenames)):
        filePaths.append(filePathToFolder + backSlash + filenames[i])
    return filePaths




## CONSTANTS FOR THIS PROJECT ##

currentPath = os.path.abspath(os.getcwd())
backSlash = "\\"
raw_CSV_folder_path       = currentPath + backSlash + "Raw CSV"
formatted_CSV_folder_path = currentPath + backSlash + "Formatted CSV"
processed_CSV_folder_path = currentPath + backSlash + "Processed CSV"
# S for 'final measurements of speed (10m/s)' and DX for 'Diode x-position'
filenames_S  = ['S13_20220426_1524.csv', 'S14_20220426_1526.csv', 'S15_20220426_1529.csv', 'S16_20220426_1534.csv', 'S17_20220426_1539.csv', 'S18_20220426_1547.csv', 'S19_20220426_1550.csv', 'S20_20220426_1552.csv', 'S21_20220426_1605.csv', 'S22_20220426_1609.csv', 'S23_20220426_1612.csv']
filenames_DX = ['DX_32mm_20220426.csv',  'DX_33mm_20220426.csv',  'DX_34mm_20220426.csv',  'DX_35mm_20220426.csv',  'DX_36mm_20220426.csv',  'DX_37mm_20220426.csv',  'DX_38mm_20220426.csv',  'DX_39mm_20220426.csv',  'DX_40mm_20220426.csv',  'DX_41mm_20220426.csv',  'DX_42mm_20220426.csv',  'DX_43mm_20220426.csv',  'DX_44mm_20220426.csv']
filenames_I  = ['I_Steg1_20220429_SD2.csv', 'I_Steg2_20220429_SD2.csv', 'I_Steg3_20220426.csv', 'I_Steg4_20220426.csv', 'I_Steg5_20220426.csv']
filename_I_allCoils = ['I_allCoils_20220426.csv']
filePaths_S  = get_filePaths_ofFilenames_inFolder(formatted_CSV_folder_path, filenames_S)
filePaths_DX = get_filePaths_ofFilenames_inFolder(formatted_CSV_folder_path, filenames_DX)
filePaths_I  = get_filePaths_ofFilenames_inFolder(raw_CSV_folder_path,       filenames_I)
filePath_I_allCoils_raw = raw_CSV_folder_path + backSlash + "I_allCoils_20220426.csv"
filePath_S13_through_S23_time_Xpos           = formatted_CSV_folder_path + backSlash + "S_time_Xpos_20220428.csv"
filePath_processed_S13_through_S23_time_Xvel = processed_CSV_folder_path + backSlash + "S_time_Xvel_20220428_sigma5.csv"

filePath_simulated_S_data_CSV           = formatted_CSV_folder_path + backSlash + "Simulated_S_data_20220428.csv" 
filePath_processed_and_simulated_S_data = processed_CSV_folder_path + backSlash + "Processed_and_simulated_S_Xvel_sigma5_20220428.csv"

filePath_I_all_individual_coils           = processed_CSV_folder_path + backSlash + "I_Steg12345_20220428.csv"
filePath_I_all_individual_coils_processed = processed_CSV_folder_path + backSlash + "I_Steg12345_20220428_correctedCurrent.csv"
filePath_I_allCoils = processed_CSV_folder_path + backSlash + "I_allCoils_20220428_nonCorrected.csv"

filePath_processedSimulatedSdata_IallCoils = processed_CSV_folder_path + backSlash + "processedSimulatedSdata_and_IallCoils_sameKfactor_20220429.csv"

def get_columnData_from_CSV(filePath, column):
    CSV = read_CSV(filePath)
    header = get_CSV_header(CSV)
    columnData = CSV[header[column]]
    return columnData

def get_part_of_string(string, startIndexInclusive, endIndexInclusive):
    result = string[startIndexInclusive-1:endIndexInclusive]
    return result

def get_columnData_from_CSV_files(filePaths, column):
    columnData = []
    for i in range(len(filePaths)):
        columnData.append(get_columnData_from_CSV(filePaths[i], column))
    return columnData

def get_custom_header_from_S_files(filenames, endHeaderString):
    S_numbers = []
    S_header= []
    for i in range(len(filenames)):
        S_numbers.append( get_part_of_string(filenames[i], 1, 3) )#gives start  to set as header for new CSV-file, e.g. "S13" or "S20"
        S_header.append( S_numbers[i] + endHeaderString)
    return S_header

def create_dataFrame_S_time_and_Xpos_data(filePaths, filenames):
    XposData  = get_columnData_from_CSV_files(filePaths, 2) #2 for X-position
    timeData  = get_columnData_from_CSV(filePaths[0], 1)
    header    = get_custom_header_from_S_files(filenames, " X-position (mm)")
    dataFrame = pd.DataFrame(XposData, header).transpose()
    dataFrame.insert(loc=0, column='Time (s)', value=timeData)
    return dataFrame

def write_dataFrame_to_CSV(dataFrame, filePath_CSV):
    dataFrame.to_csv(filePath_CSV, CSV_DELIMITER, index=False)
    print("DONE: Write dataFrame to CSV: " + str(filePath_CSV))


def add_one_column_from_CSV_to_CSV(column, from_CSV_path, CSV_path, new_CSV_path):
    from_CSV = read_CSV(from_CSV_path)
    from_header = get_CSV_header(from_CSV)

    CSV = read_CSV(CSV_path)
    header = get_CSV_header(CSV)

    columnHeader = from_header[column]
    columnData = from_CSV[columnHeader]
    CSV.insert(loc=len(header), column=columnHeader, value=columnData)

    CSV.to_csv(new_CSV_path, CSV_DELIMITER, index=False)
    print("DONE: Add one column from " + str(from_CSV_path) + " \n      to " + str(new_CSV_path))


def add_all_columns_from_CSV_to_CSV(from_CSV_path, CSV_path, new_CSV_path):
    from_CSV = read_CSV(from_CSV_path)
    from_header = get_CSV_header(from_CSV)

    CSV = read_CSV(CSV_path)
    header = get_CSV_header(CSV)

    for i in range(len(from_header)):
        columnHeader = from_header[i]
        columnData = from_CSV[columnHeader]
        CSV.insert(loc=len(header)+i, column=columnHeader, value=columnData)

    CSV.to_csv(new_CSV_path, CSV_DELIMITER, index=False)
    print("DONE: Added all columns from " + str(from_CSV_path) + " \n      to " + str(new_CSV_path))






## MAIN ##

S_analysis = False #measurements S13-S23 taken 20220426
plot_Sdata = False #plot "gaussed and derivative and noZeroed"-data
add_simulatedData_to_S = False

I_coils_analysis = True
combineIallCoils_and_Smeasurement= True
DX_analysis = False


if S_analysis:
    print("ANALYSIS: S-measurements")
    filePath = filePath_S13_through_S23_time_Xpos
    processedFilePath = filePath_processed_S13_through_S23_time_Xvel
    dataFrame_S = create_dataFrame_S_time_and_Xpos_data(filePaths_S, filenames_S)
    write_dataFrame_to_CSV(dataFrame_S, filePath)

    data = read_CSV(filePath) #data is: 0 = time, 1 = Xpos S13, 2 = Xpos S14, 3 = Xpos S15, ...
    header = get_CSV_header(data)
    Xpos_range = range(1,12) #which Xpos_S columns to keep in analysis
    column_start = min(Xpos_range)
    time = data[header[0]]

    # apply gaussian for each column in Xpos_range before velcity calc
    sigma = 5 #arbitrarily chosen as 5
    V_x_S  = [None for x in Xpos_range]
    time_S = [None for x in Xpos_range]
    Xpos_S_gaussed = [None for x in Xpos_range]
    V_x_header = [None for x in Xpos_range]
 
    for i in Xpos_range:
        # gauss filter per column (Xpos for each S-measurement)
        Xpos_S_i = data[header[i]]
        [Xpos_S_i_noZeroes, time_noZeroes] = remove_zeroValues(Xpos_S_i, time)
        Xpos_S_gaussed[i-column_start] = gaussianFilter1D(Xpos_S_i_noZeroes, sigma)

        # get velocity in x-axis by use of gradient (negative since Qualisys defines coordinate system different from us)
        V_x_S[i-column_start] = -(np.gradient(Xpos_S_gaussed[i-column_start])/np.gradient(time_noZeroes))/1000 #div 1000 to mm/s --> m/s

        # remove values from velocity that are below a certain lower limit (+ som buffer rows(?)) to align S-measurements in time with each other
        V_x_S_i = V_x_S[i-column_start]
        minSpeed = 80/1000 # 50 mm/s = 50/1000 m/s
        for k in range(len(V_x_S_i)):
            if V_x_S_i[k] > minSpeed:
                firstFastIndex = k
                break
        numIndexesBeforeMinSpeed = 50 #in order to get data where dx/dt = 0 in figure
        indexes = range(firstFastIndex-numIndexesBeforeMinSpeed, len(V_x_S_i))

        #indexes = V_x_S_i > minSpeed
        #indexes_numbers = 
        V_x_S_i_selected = [V_x_S_i[x] for x in indexes]
        time_selected    = [time_noZeroes[x] for x in indexes]
        #time_selected = []
        #for j in range(len(time_noZeroes)): #ugly way of saying: "time_selected = time_noZeroes[indexes]", but since i get error otherwise I dont care if its ugly //2022-04-27
        #    if indexes[j]:
        #        time_selected.append(time_noZeroes[j])

        removeNumLastDataPoints = 20 #remove last 20 points, since numerical derivative gets funky there
        V_x_S_i_selected = V_x_S_i_selected[0:len(V_x_S_i_selected)-removeNumLastDataPoints]
        time_selected    = time_selected[0:len(time_selected)-removeNumLastDataPoints]
     
        # plot to make sure it looks good
        t = time_selected
        time_S[i-column_start] = t
        V_x = V_x_S_i_selected
        V_x_S[i-column_start] = V_x
        
        if i != 3: #remove S15 which had bad data from Qualisys, 2022-04-27
            plt.plot(t, V_x, label=str(header[i])+" (calc dx/dt, sigma="+str(sigma)+")")
    
    if plot_Sdata:
        plt.legend()
        plt.show()

    # remove end points of vectors s.t. they become only as long as the shortest (for average later)
    V_x_S_temp = V_x_S.copy()
    V_x_S_temp.pop(2) #remove S15 measurement
    V_x_S_selected = V_x_S_temp 

    minVectorLen = len(min(V_x_S_selected, key=len))
    V_x_S_cut = V_x_S_selected.copy()
    for i in range(len(V_x_S_selected)):
        V_x_S_cut[i] = V_x_S_selected[i][0:minVectorLen]
        
    t = t[0:minVectorLen] 
    
    arbitraryStartTime_ms = []
    dt = 0.0001*1000 #timestep in Qualiys-data (s)*1000 to get in milliseconds (ms)
    t_index_correction_from_figure = 5 #looked at figure and picked an index value s.t. t=0 looks good w.r.t. calculated dx/dt
    for i in range(len(max(V_x_S_cut, key=len))):
        arbitraryStartTime_ms.append(dt*(i-numIndexesBeforeMinSpeed+t_index_correction_from_figure)) 

    V_x_average = np.average(V_x_S_cut, axis=0)
    V_x_header = get_custom_header_from_S_files(filenames_S, ' dx/dt (m/s)')
    V_x_header.pop(1) #remove S15 header
    V_x_dataFrame = pd.DataFrame(V_x_S_cut, V_x_header).transpose()
    V_x_dataFrame.insert(loc=0, column='Average dx/dt (m/s)', value=V_x_average)
    V_x_dataFrame.insert(loc=0, column='Arbitrary start time (ms)', value=arbitraryStartTime_ms)
    write_dataFrame_to_CSV(V_x_dataFrame, processedFilePath)

    if add_simulatedData_to_S:
        print("ANALYSIS: S-measurements: added simulated data to S-file")
        add_all_columns_from_CSV_to_CSV(filePath_simulated_S_data_CSV, processedFilePath, filePath_processed_and_simulated_S_data)
    
    
    quit()
    

if I_coils_analysis:
    print("ANALYSIS: current through coils")
    for i in range(1,len(filePaths_I)): #skip first file since we use first file for current through coilpar 1
        if i == 1:
            add_one_column_from_CSV_to_CSV(1, filePaths_I[i], filePaths_I[0], filePath_I_all_individual_coils)
        else:
            add_one_column_from_CSV_to_CSV(1, filePaths_I[i], filePath_I_all_individual_coils, filePath_I_all_individual_coils)
    
    I_data = read_CSV(filePath_I_all_individual_coils)
    header = get_CSV_header(I_data)

    t = I_data[header[0]]*1000 #s --> ms
    I_coil_measured = []
    for i in range(1,len(header)):
        I_coil_measured.append(I_data[header[i]])
        plt.plot(t, I_coil_measured[i-1], label="non-corrected current coilpar "+str(i))

    plt.legend()
    #plt.show()

    # correction of measured current vs. actual current through coilpair (we used current divider as to not cap the oscilloscope)
    K_factor = [3,3,4,4,4] #measured K_i = I_actualCurrent / I_measuredCurrent  for coilpair i

    I_coil_corrected = []
    for i in range(len(I_coil_measured)):
        I_coil_corrected.append(I_coil_measured[i]*K_factor[i])
    
    #write to new CSV
    header_corrected = []
    for i in range(1,len(header)):
        header_corrected.append("Measured current through coilpair "+str(i) + " scaled by factor K_" + str(i)+" = " + str(K_factor[i-1]) + " (A)")

    dataFrame = pd.DataFrame(I_coil_corrected, header_corrected).transpose()
    dataFrame.insert(loc=0, column="Oscilloscope time (ms)", value=t)
    write_dataFrame_to_CSV(dataFrame, filePath_I_all_individual_coils_processed)



    # I_allCoils_20220426
    I_all = read_CSV(filePath_I_allCoils_raw)
    header_I_all = get_CSV_header(I_all)

    t_offset = 1.35 #ms, by looking at graph
    t = I_all[header_I_all[0]]
    t *= 1000 #s --> ms
    t += t_offset #to get first coil to trigger att t = 0

    #t_startStage = []
    #t_endStage = []
    #I_stage = []
    #for i in range(5):
    #    I_stage.append(I_all[header_I_all[1]][])

    ### split I_all into each stage (1,2,3,4,5) and correct by factor K_i according to lablogg
    #plt.plot(t, I_stage[i])

    # filePath_processedSimulatedSdata_IallCoils

    I_all[header_I_all[0]] = t
    K_all = 6 #K_i \approx 6 forall i, this is a test!
    I_all[header_I_all[1]] *= K_all 
    I_all = I_all.rename(columns={header_I_all[0]: "Oscilloscope time (ms)", header_I_all[1]: "Measured current through all coilpairs (A) scaled by factor " + str(K_all)})
    write_dataFrame_to_CSV(I_all, filePath_I_allCoils)


    if combineIallCoils_and_Smeasurement:
        add_all_columns_from_CSV_to_CSV(filePath_I_allCoils, filePath_processed_and_simulated_S_data, filePath_processedSimulatedSdata_IallCoils)

    quit()


#EOF
