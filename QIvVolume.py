import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

site = 'LUNG' # Pick an anatomical site from {PROSTATE, LUNG}
col  = 'CI'   # Pick a Quality Indicator from the list below matching the selected site

if site == 'PROSTATE':
    Patients = ['004','005','006','007','008','011','002','010','001','003','009']  # Patient order based on order of appearance in .csv
    QualIndi = ['Volume','CI','HI','CTV_D98','PTV_D2','PTV_D1','PTV_D99','PTV_D98','Bladder_V60','Bladder_V50',
            'Bladder_V45','Bladder_V40','Bladder_V30','Rectum_V60','Rectum_V57','Rectum_V50','Rectum_V45',
                             'Rectum_V35','Rectum_V30','Rectum_V25','Rectum_V20']
    C_col    = 33
    dataFile = 'ProstateData.csv'
if site == 'LUNG':
    Patients = ['002','003','004','005','006','007','008','009','010','011','001']
    QualIndi = ['Volume','CI','HI','CTV_D100','PTV_D2','PTV_D98','BPlexL_D0','BPlexR_0','Heart_V50','Lung_V20',
            'Lung_V5','Lung_V30','Oesophagus_D0']
    C_col    = 26
    dataFile = 'LungData.csv'

#  Set up dataFrames
df_25mm = pd.DataFrame(columns= QualIndi, index= Patients) #   2.5mm Leaf Width Quality Indicators
df_5mm  = pd.DataFrame(columns= QualIndi, index= Patients) #     5mm Leaf Width Quality Indicators
df_10mm = pd.DataFrame(columns= QualIndi, index= Patients) #    10mm Leaf Width Quality Indicators
df_clin = pd.DataFrame(columns= QualIndi, index= Patients) # Clinically Planned Quality Indicators

#  Sort patient data into dataFrames
with open('ProstateData.csv', 'r') as file:
    data = file.read().splitlines()
    for pat in Patients:             # Loop through each Patient
        i = Patients.index(pat)
        QI2 = data[4+i].split(',')
        QI5 = data[18+i].split(',')
        QI10 = data[32+i].split(',') 
        QIC = data[4+i].split(',')
        for qi in QualIndi:          # Loop through each Quality Indicator
            j = QualIndi.index(qi)
            df_25mm.loc[pat][qi] = float(QI2[11+j])
            df_5mm.loc[pat][qi] = float(QI5[11+j])
            df_10mm.loc[pat][qi] = float(QI10[11+j])
            df_clin.loc[pat][qi] = float(QIC[33+j])


df = [df_25mm,df_5mm,df_10mm] #  Group Leaf Width Data Frames in a list
color = ['steelblue','limegreen','indianred']

font    = {'fontname':'times new roman'}
title_size = 20
label_size = 14

m = [0,0,0] # Gradient array
c = [0,0,0] # Y-Intercept array

# Plot of selected Quality Indicator against Volume
plt.figure(figsize=(12,8))
ax = plt.gca()
for i in range(3):  # Loop through each leaf width
    df[i].plot('Volume',col, ax=ax, kind='scatter',c=color[i],s=50) #  Scatter plot QI against Volume
    x = list(df[i]['Volume'])
    z = np.polyfit(x,list(df[i][col]), 1) # Calulate trendline of data
    p = np.poly1d(z)
    plt.plot(x,p(x),color[i])  #  plot trendline of QI against Volume
    m[i], c[i] = z[0],z[1]
            
plt.title('Volume v '+col+" for Different MLC Leaf Widths for "+site+" Patients",**font,fontsize=title_size)
plt.xlabel('Volume [cc]',**font,fontsize=label_size)
plt.ylabel(col.replace("_",' ')+' [%]',**font,fontsize=label_size)
plt.legend(['2.5mm',"%.4fV+(%.2f)"%(m[0],c[0]),'5mm',"%.4fV+(%.2f)"%(m[1],c[1]),'10mm',"%.4fV+(%.2f)"%(m[2],c[2])])
plt.show()
