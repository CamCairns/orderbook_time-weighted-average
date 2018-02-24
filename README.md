# README

Simple orderbook program + bash executable that reads input data from a file and prints out the time-weighted average of the highest price.

The input data is in simple ASCII text format as follows:

     1000 I 100 10.0
     2000 I 101 13.0
     2200 I 102 13.0
     2400 E 101
     2500 E 102
     4000 E 100

Where each line consists of either 3 or 4 fields, separated by spaces:

* Timestamp (an integer, milliseconds since start of trading) 
* Operation (a single character, `I` = Insert, `E` = Erase)
* Id (a 32-bit integer)
* [Insert operations only] Price (a double-precision float)

eg. in the data above, there are three time periods during wHich the high price is valid:
	
	1000-2000 10.0 2000-2500 13.0 2500-4000 10.0
	
So the time-weighted average price is $$((10 * 1000) + (13 * 500) + (10 * 1500)) / 3000 = 10.5$$

If there are time periods in which there are no orders in the orderbook these time periods do not contribute to the output value. Returns NaN if the orderbook is empty.

### Assumptions

- The timestamps are monotonically increasing
- Each order id appears exactly twice (one insert and one erase)
- Erase messages always appear after their corresponding insert
- The prices are always finite