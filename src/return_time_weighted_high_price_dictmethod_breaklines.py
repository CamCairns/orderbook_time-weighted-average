import numpy as np
import os

def is_non_zero_file(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False

def unpack_new_line(line):
    if line.split()[1] == 'I':
        new_timestamp, new_flag, new_id_num, new_price = line.split()
        new_price = float(new_price)
    else:
        new_timestamp, new_flag, new_id_num = line.split()
        new_price = None
    new_timestamp = int(new_timestamp)
    new_id_num = int(new_id_num)
    return new_timestamp, new_flag, new_id_num, new_price

class OrderBook():
    def __init__(self):
        self.ledger = {}
        self.high_price = None
        self.latest_time = 0
        self.delta_t = 0
        self.elapsed_time = 0
        self.time_scaled_high_price = 0
        self.recalculate_max_high_flag = True
     
    def __str__(self):
         return str(self.ledger)
        
    def insert(self,id_num,price):
        self.recalculate_max_high_flag = True if (price > self.high_price) or (np.isnan(self.high_price)) else False
        self.ledger[id_num] = price
    
    def erase(self,id_num):
        self.recalculate_max_high_flag = True if self.ledger[id_num] == self.high_price else False
        del self.ledger[id_num]

    def get_high_price(self):
        if self.recalculate_max_high_flag:
            try:
                self.high_price = max(self.ledger.values())
            except ValueError: # catches case when orderbook is empty, sets high value to NaN (as requested)
                self.high_price = np.nan
        else:
            pass
    
    def update_elapsed_time(self):
        self.elapsed_time = self.elapsed_time + self.delta_t
        
    def update_time_scaled_high_price(self):
        self.time_scaled_high_price = self.time_scaled_high_price + self.high_price*self.delta_t

if __name__ == "__main__":
    orderbook = OrderBook()
    file_path = '/Users/camcairns/Dropbox/py_modules/data_science_projects/OxAM/generated_data.txt'
    if is_non_zero_file(file_path):
        with open(file_path) as f:
            for line in f:
                new_timestamp, new_flag, new_id_num, new_price = unpack_new_line(line)
                orderbook.delta_t = new_timestamp - orderbook.latest_time
                orderbook.latest_time = new_timestamp
                orderbook.get_high_price()
#                 print orderbook.high_price
                if np.isnan(orderbook.high_price):
                   pass
                else:
                    orderbook.update_elapsed_time()
                    orderbook.update_time_scaled_high_price()
                if new_flag == 'I':
                    orderbook.insert(new_id_num,new_price)
                else:
                    orderbook.erase(new_id_num)
            print 'The time-weighted high price is', orderbook.time_scaled_high_price/orderbook.elapsed_time
            print orderbook.time_scaled_high_price
            print orderbook.elapsed_time
    else:
        print 'ASCII text file is empty! No data to compute time weighted high price.'
