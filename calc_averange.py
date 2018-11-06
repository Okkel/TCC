from os import listdir
import pandas as pd

core = 'fitness_evolutionmoreno_health/fitness_evolutionmoreno_health_medida_'
mesure_number = 18

dataFrames = []
for i in range(mesure_number):
    dataFrames.append(pd.read_csv(core + str(i) + '.csv',sep=';'))

new_df = pd.DataFrame()
for i,j in enumerate(dataFrames):
    new_df[str(i)] = j['average']

new_df.to_csv(core.split('/')[0]+'/averange-'+ core.split('/')[1]+'.csv')
