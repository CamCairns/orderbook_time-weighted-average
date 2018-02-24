import numpy as np
import pandas as pd 

rows_list = []
timestamp_list = []
timestamp = 0
for i in xrange(20000):
    price = 20*np.random.random_sample() # random price between 0 and 20
    dictI = {'flag':'I','id':i,'price':price} # generate a monotonically increasing timestamp elsewhere and append at the end
    dictE = {'flag':'E','id':i,'price':''}
    
    rand_indexI = np.random.randint(0,len(rows_list)+1) # generate a random index for inserts (in the range of the current number of rows)
    rand_indexE = np.random.randint(rand_indexI+1,len(rows_list)+2) # generate a random index for erasures that is always greater then rand_indexI
    rows_list.insert(rand_indexI, dictI)
    rows_list.insert(rand_indexE, dictE)
    for i in range(2):
        timestamp = timestamp + np.random.randint(0,5000)
        timestamp_list.append(timestamp)

df = pd.DataFrame(rows_list)
df['timestamp'] = timestamp_list

cols = ['timestamp','flag','id','price']
df = df[cols]

df.to_csv('./generated_data.txt', sep=' ', index=False, header=False)