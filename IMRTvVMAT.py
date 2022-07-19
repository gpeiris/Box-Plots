import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

font    = {'fontname':'times new roman'}
title_size = 20
label_size = 14

Patients = ['002','003','004','006','007','008','009','010','011','012','013','014'] 
QualIndi = ['CTV_D98','PTV_D98','PTV_D99','PTV_D2','PTV_D1','CI','Bladder_V60','Bladder_V50',
            'Bladder_V45','Bladder_V40','Bladder_V30','FemHeadL_V35','FemHeadR_V35','Rectum_V60','Rectum_V57',
            'Rectum_V50','Rectum_V45','Rectum_V35','Rectum_V30','Rectum_V25','Rectum_V20','MUperGy','HI']
# Only a portion of the Metrics can be compared as some don't apply to IMRT in the TPS used

df_IMRT = pd.DataFrame(columns= QualIndi, index= Patients)
df_VMAT = pd.DataFrame(columns= QualIndi, index= Patients)

with open('IMRTVMAT-PMS.csv', 'r') as file:
    data = file.read().splitlines()
    for pat in Patients: 
        i = Patients.index(pat)
        QIVMAT  = data[1+2*i].split(',')
        QIIMRT = data[2+2*i].split(',')
        for qi in QualIndi:
            j = QualIndi.index(qi)
            df_IMRT.loc[pat][qi] = float(QIIMRT[4+j])
            df_VMAT.loc[pat][qi] = float(QIVMAT[4+j])

for col in QualIndi:
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    x,y = list(df_IMRT[col]), list(df_VMAT[col])
    X,Y = [float(i) for i in x], [float(i) for i in y]
    #X,Y,Z = np.subtract(X,C), np.subtract(Y,C), np.subtract(Z,C)
    #plt.axhline(y=0,color='orange')
    bp = ax.boxplot([X,Y],patch_artist = True)
    ax.set_xticklabels(['IMRT','VMAT'])

    colors = ['steelblue','limegreen','indianred']

    plt.title(col+" Different Treatment Techniques for Prostate Patients",**font,fontsize=title_size)
    plt.xlabel('Treatment Technique',**font,fontsize=label_size)
    plt.ylabel(col.replace("_",' ')+' [%]',**font,fontsize=label_size)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    plt.savefig('output_IMRTvVMAT/TrmtTq_' + col + '.png', dpi=600, transparent=True)
    plt.show()
    plt.close()
