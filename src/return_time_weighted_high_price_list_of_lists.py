import numpy as np
import os

def is_non_zero_file(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False

class InsertEntry():
    def __init__(self, id_num, price):
        self.id_num = id_num
        self.price = price
    
    def __str__(self):
        return str([self.id_num, self.price])

class OrderBook():
    def __init__(self):
        self.value = []
        self.high_price = None
        self.latest_time = 0
        self.delta_t = 0
        self.elapsed_time = 0
        self.time_scaled_high_price = 0
     
    def __str__(self):
         return str([str(i) for i in self.value])
        
    def insert(self,entry):
        self.value.append(entry)
    
    def erase(self,id_num):
        for i, o in enumerate(self.value):
            if o.id_num == id_num:
                del self.value[i]
                break

    def get_high_price(self):
        try:
            self.high_price = max([entry.price for entry in self.value if len(self.value)>0])
        except ValueError: # catches case when orderbook is empty, sets high value to NaN (as requested)
            self.high_price = np.nan
    
    def update_elapsed_time(self):
        self.elapsed_time = self.elapsed_time + self.delta_t
        
    def update_time_scaled_high_price(self):
        self.time_scaled_high_price = self.time_scaled_high_price + self.high_price*self.delta_t

if __name__ == "__main__":
    orderbook = OrderBook()
    file_path = '/Users/camcairns/Dropbox/py_modules/data_science_projects/OxAM/generated_data.txt'
    if is_non_zero_file(file_path): # check that the text file is not empty
        with open(file_path) as f:
            for i, line in enumerate(f):
                new_line = line.split()
                orderbook.delta_t = float(new_line[0]) - orderbook.latest_time
                orderbook.latest_time = float(new_line[0])
                orderbook.get_high_price()
                if ~np.isnan(orderbook.high_price):
                    orderbook.update_elapsed_time()
                    orderbook.update_time_scaled_high_price()
                else:
                    pass
                if new_line[1] == 'I':
                    entry = InsertEntry(int(new_line[2]),float(new_line[3]))
                    orderbook.insert(entry)
                else:
                    orderbook.erase(int(new_line[2]))
            print 'The time-weighted high price is', orderbook.time_scaled_high_price/orderbook.elapsed_time
            print orderbook.time_scaled_high_price
            print orderbook.elapsed_time
    else:
        print 'ASCII text file is empty! No data to compute time weighted high price.'