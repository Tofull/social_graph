import pandas as pd
import glob
import os
import shutil


path =r'../data'
allFiles = glob.glob(path + "/relations*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
frame = pd.concat(list_)
# print(frame)
#
# for index, row in df.iterrows():
#     print(row[1], row[2])

# nameUsers = pd.concat([frame[frame.columns[1]] + frame[frame.columns[2]] ])
nameUsersJoin = frame[frame.columns[1]].append(frame[frame.columns[2]]).reset_index(drop=True)
nameUsers = nameUsersJoin.unique()
print(nameUsers)

nameSocialNetworks = frame[frame.columns[0]].unique()

#### Save in file
fh = open("hello.txt", "w")

### Create networks
for network in nameSocialNetworks:
    fh.write("create (`"+network+"`:Social {nom:\""+network+"\"})\n")
fh.write("\n\n\n")

### Create users
for user in nameUsers:
    fh.write("create (`"+user+"`:Personne {nom:\""+user+"\"})\n")
fh.write("\n\n\n")

for index, row in frame.iterrows():
    network = row[0]
    personne1 = row[1]
    personne2 = row[2]
    fh.write("match (n:Personne),(m:Personne) where n.nom=\""+personne1+"\" and m.nom=\""+personne2+"\" create (n)-[:KNOWS]->(m)\n")
fh.write("\n\n\n")



# print(pd.unique(frame[[frame.columns[1], frame.columns[2]]].values.ravel()))
grouped = frame.groupby(frame.columns[0])

for name, group in grouped:
    # print(name + " : " + group)
    nameGroupUsersJoin = group[group.columns[1]].append(group[group.columns[2]]).reset_index(drop=True)
    nameGroupUsers = nameGroupUsersJoin.unique()

    for user in nameGroupUsers:
        fh.write("match (n:Personne),(m:Social) where n.nom=\""+user+"\" and m.nom=\""+name+"\" create (n)-[:SIGNIN]->(m)\n")

    fh.write("\n\n\n")

#### Close the file
fh.close()

### Split the file for online console neo4j
dir = './outputNeo4jConsole'
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)
os.system("split -d -l 200 hello.txt ./outputNeo4jConsole/hello_split.")
