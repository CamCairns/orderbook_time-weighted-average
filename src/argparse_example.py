#!/usr/bin/env python
# -*- coding: utf-8 -*-

def mul(A, B):
    a, b, c = A
    d, e, f = B
    return a*d + b*e, a*e + b*f, b*e + c*f

def pow(A, n):
    if n == 1:     return A
    if n & 1 == 0: return pow(mul(A, A), n//2)
    else:          return mul(A, pow(mul(A, A), (n-1)//2))

def fib(n):
    if n < 2: return n
    return pow((1,1,0), n-1)[0]

if __name__ == "__main__":
    import argparse
    import os 

    def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        elif not os.path.getsize(arg) > 0:
            parser.error("The file %s is empty!" % arg)
        else:
            return arg

    parser = argparse.ArgumentParser(description="less script")
    parser.add_argument("filename", help="write report to FILENAME", metavar="FILE",type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()
    print args.filename
    
#     f = open(args.filename, 'r')
#     for i in xrange(10):
#         print f.readline()
#     