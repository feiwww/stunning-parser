'''
Author: Wang Fei(wangfei15@cmschina.com.cn)
Date: 2022-11-06 11:25:22
LastEditors: Wang Fei(wangfei15@cmschina.com.cn)
LastEditTime: 2022-11-07 22:36:59
Description: 
'''

from CppParser import *

file_path = "./SingleStruct.h"
parser = CppParser()
struct = parser.ParserStruct(file_path)
# struct.show()
names = struct.getParaNames()
print(names)

assert(len(struct.getParaNames())== 7)
assert(struct.name == "FundStockTransReq")
