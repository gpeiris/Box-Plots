import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

font    = {'fontname':'times new roman'}
title_size = 20
label_size = 14

site = 'LUNG' # Pick an anatomical site from {PROSTATE, LUNG}
col  = 'CI'   # Pick a Quality Indicator from the list below

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
with open(dataFile, 'r') as file:
    data = file.read().splitlines()
    for pat in Patients:             # Loop through each Patient
        i = Patients.index(pat)
        QI2 = data[1+3*i].split(',')
        QI5 = data[2+3*i].split(',')
        QI10 = data[3+3*i].split(',')
        #QIC = data[4+i].split(',')
        for qi in QualIndi:          # Loop through each Quality Indicator
            j = QualIndi.index(qi)
            df_25mm.loc[pat][qi] = float(QI2[4+j])
            df_5mm.loc[pat][qi] = float(QI5[4+j])
            df_10mm.loc[pat][qi] = float(QI10[4+j])
            #df_clin.loc[pat][qi] = float(QIC[C_col+j])

colors = ['steelblue','limegreen','indianred']

for col in QualIndi: # Loop through all metrics 
# By default will show difference from clinically planned value 
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    x,y,z,c = list(df_25mm[col]), list(df_5mm[col]), list(df_10mm[col]), list(df_clin[col])
    X,Y,Z,C = [float(i) for i in x], [float(i) for i in y], [float(i) for i in z], [float(i) for i in c]
    #X,Y,Z = np.subtract(X,C), np.subtract(Y,C), np.subtract(Z,C) # Comment out this line for an absolute value comparison
    #plt.axhline(y=0,color='orange')                              # Comment out this line for an absolute value comparison
    bp = ax.boxplot([X,Y,Z],patch_artist = True)
    ax.set_xticklabels(['2.5', '5','10'])

    plt.title(col+" Different MLC Leaf Widths for "+site+" Patients",**font,fontsize=title_size)
    plt.xlabel('MLC Leaf Width [mm]',**font,fontsize=label_size)
    plt.ylabel(col.replace("_",' ')+' [%]',**font,fontsize=label_size)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.savefig('outputFigures/Boxplots/' + site + '_' + col + '.png', dpi=600, transparent=True)
    plt.show()
    plt.close()
