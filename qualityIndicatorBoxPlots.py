###
### PROSTATE , LUNG & LIVER - BOX & WHISKER PLOTS
###

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

font    = {'fontname':'times new roman'}
title_size = 20
label_size = 14

siteSet = ['PROSTATE', 'LUNG', 'LIVER']

while True:
    site = input('Which anatomical site {PROSTATE, LUNG, LIVER}?: ')
    if site in siteSet:
        break
    else:
        print('Pick an anatomical site from {PROSTATE, LUNG, LIVER}')

if site == 'PROSTATE':
    Patients = ['002','003','004','006','007','008','009','010','011','012','013','014']  # Patient order based on order of appearance in .csv
    #QualIndi = ['CTV_D98','PTV_D98','PTV_D99','PTV_D2','PTV_D1','CI','Bladder_V60','Bladder_V50',
    #           'Bladder_V45','Bladder_V40','Bladder_V30','FemHeadL_V35','FemHeadL_V45','FemHeadL_V60',
    #           'FemHeadR_V35','FemHeadR_V45','FemHeadR_V60','Rectum_V60','Rectum_V57','Rectum_V50','Rectum_V45',
    #           'Rectum_V35','Rectum_V30','Rectum_V25','Rectum_V20','ALPO','DynALPO','MUperGy','Volume','HI']
    QualIndi = ['CTV_D98','PTV_D98','PTV_D99','PTV_D2','PTV_D1','CI','Bladder_V60','Bladder_V50',
                'Bladder_V45','Bladder_V40','Bladder_V30','FemHeadL_V35','FemHeadL_V45','FemHeadL_V60',
                'FemHeadR_V35','FemHeadR_V45','FemHeadR_V60','Rectum_V60','Rectum_V57','Rectum_V50','Rectum_V45',
                'Rectum_V35','Rectum_V30','Rectum_V25','Rectum_V20','MUperGy','HI']
    dataFile = 'ProstateData-PMS.csv'
    clinFile = 'ProstateData-CLN.csv'
if site == 'LUNG':
    Patients = ['012','001','002','004','005','006','007','008','009','010']
    QualIndi = ['iGTV_D100','PTV_D2','PTV_D98','CI','Heart_V50','BPlexL_D0','BPlexR_0','Lung_V20',
            'Lung_V5','Lung_V30','Oesophagus_D0','ALPO','DynALPO','MUperGy','HI']
    dataFile = 'LungData-PMS.csv'
    clinFile = 'LungData-CLN.csv'
if site == 'LIVER':
    Patients = ['001','002','003','004','005','006','007','008','009','010']
    QualIndi = ['GTV_D100','PTV_D98','PTV_D99','PTV_D2','PTV_D1','CI','Aorta_D0','CHT_V25','CHT_V30',
                'Chestwall_D30','CBD_D5','Duodenum_D5','Gallbladder_D5','Heart_D30','IVC_D0','LargeBowel_D5',
                'LargeBowel_D0','Oesophagus_D0','Skin_D0','SmallBowel_D5','SmallBowel_D0',
                'Stomach_D5', 'Stomach_D0','ALPO','DynALPO','MUperGy','Volume','HI']
    dataFile = 'LiverData-PMS.csv'
    #clinFile = 'LiverData-CLN.csv'
    
#  Set up dataFrames
df_25mm = pd.DataFrame(columns= QualIndi, index= Patients) #   2.5mm Leaf Width Quality Indicators
df_5mm  = pd.DataFrame(columns= QualIndi, index= Patients) #     5mm Leaf Width Quality Indicators
df_10mm = pd.DataFrame(columns= QualIndi, index= Patients) #    10mm Leaf Width Quality Indicators
df_clin = pd.DataFrame(columns= QualIndi, index= Patients) # Clinically Planned Quality Indicators

#  Sort patient data into dataFrames
# with open(dataFile, 'r') as a, open(clinFile, 'r') as b:  # Comment out this line for an absolute value comparison
with open(dataFile, 'r') as a:
    data = a.read().splitlines()
    #clin = b.read().splitlines()    #  Comment out this line for an absolute value comparison
    for pat in Patients:             # Loop through each Patient
        i = Patients.index(pat)
        QI2 = data[1+3*i].split(',')
        QI5 = data[2+3*i].split(',')
        QI10 = data[3+3*i].split(',')
        #QIC = clin[1+i].split(',')     #  Comment out this line for an absolute value comparison
        for qi in QualIndi:             # Loop through each Quality Indicator
            j = QualIndi.index(qi)
            df_25mm.loc[pat][qi] = float(QI2[4+j])
            df_5mm.loc[pat][qi] = float(QI5[4+j])
            df_10mm.loc[pat][qi] = float(QI10[4+j])
            #df_clin.loc[pat][qi] = float(QIC[4+j])   #  Comment out this line for an absolute value comparison

colors = ['steelblue','limegreen','indianred']
    
for col in QualIndi:
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
    
    #plt.savefig('outputFigures/Boxplots/' + site + '_' + col + '.png', dpi=600, transparent=True)
    plt.show()
    plt.close()
