'''
Author: Wang Fei(wangfei15@cmschina.com.cn)
Date: 2022-11-07 22:42:31
LastEditors: Wang Fei(wangfei15@cmschina.com.cn)
LastEditTime: 2022-11-07 22:42:36
Description: 
'''

import json

from clang.cindex import Index
from clang.cindex import Config
from clang.cindex import TypeKind
from clang.cindex import CursorKind

class TinyPara():
    def __init__(self) -> None:
        self.__name_key = "name"
        self.__type_key = "type"
        self.__comment_key = "comment"
        self.__paras_key = "paras"
        self.decl = {self.__name_key:"", self.__type_key:"", self.__comment_key:"", self.__paras_key:[]}
    
    @property
    def name(self):
        return self.decl[self.__name_key]
    @name.setter
    def name(self, name):
        self.decl[self.__name_key] = name

    @property
    def type(self):
        return self.decl[self.__type_key]
    @type.setter
    def type(self, type):
        self.decl[self.__type_key] = type

    @property
    def comment(self):
        return self.decl[self.__comment_key]
    @comment.setter
    def comment(self, comment):
        self.decl[self.__comment_key] = comment
    
    def show(self):
        print(json.dumps(self.decl, indent=4,ensure_ascii=False, sort_keys=False,separators=(',', ':')))

class TinyStruct(TinyPara):
    """_summary_ 解析后的结构体
            struct = {
                "name":"xxx", 
                "comment":"xxx", 
                "type":"xxx", 
                "paras":[
                    {"name":"int", "type":"a", "comment":""},
                    {"name":"string", "type":"b", "comment":""}
                ]
            }
    """    

    def __init__(self) -> None:
        super().__init__()
        self.__struct_paras_key = "paras"
        self.decl[self.__struct_paras_key] = []
    
    def getParas(self):
        return self.decl[self.__struct_paras_key]
    
    def getParaNames(self):
        names= []
        for para in self.decl[self.__struct_paras_key]:
            names.append(para[self._TinyPara__name_key])
        return names
    
    def addPara(self, name, type, comment=""):
        self.decl[self.__struct_paras_key].append(
            {self._TinyPara__name_key:name, self._TinyPara__type_key:type, self._TinyPara__comment_key:comment})

class CppParser():
    def __init__(self) -> None:
        """_summary_ 加载clang lib
        """        
        # libclang_path = "/usr/lib/llvm-6.0/lib/libclang-6.0.so.1"
        libclang_path = "/usr/lib/llvm-10/lib/libclang-10.so.1"
        if Config.loaded == True:
            pass
        else:
            Config.set_library_file(libclang_path)

    @staticmethod
    def showNodeInfo(node):
        """_summary_ 输出Clang AST节点信息

        Args:
            node (_type_): _description_
        """        
        print('''spelling:{}, kind:{}, brief_comment:{}, type.spelling:{}, type.kind:{}'''.format(
            node.spelling, node.kind, node.brief_comment, node.type.spelling, node.type.kind))

    def ShowAST(self, cursor):
        """_summary_ 遍历输出所有节点信息

        Args:
            cursor (_type_): _description_
        """        
        for cur in cursor.get_children():
            self.showNodeInfo(cur)
            self.ShowAST(cur)

    def ParserStruct(self, file_path):
        """_summary_ 解析单个结构体

        Args:
            file_path (_type_): _description_

        Returns:
            _type_: _description_
        """        
        struct = TinyStruct()
        index = Index.create()
        tu = index.parse(file_path)
        struct_root = tu.cursor

        for node in list(struct_root.get_children()):
            if node.kind == CursorKind.STRUCT_DECL:
                struct.name = str(node.spelling) if str(node.spelling) != "" else str(node.type.spelling)
                struct.type = str(node.kind)
                struct.comment = str(node.brief_comment)
                for struct_node in list(node.get_children()):
                    # 解析每个结构体变量 && 过滤掉结构体函数
                    if struct_node.kind != CursorKind.FIELD_DECL or struct_node.type.kind == TypeKind.FUNCTIONNOPROTO:
                        continue
                    struct.addPara(str(struct_node.spelling), str(struct_node.type.kind), str(struct_node.brief_comment))
        
        # self.ShowAST(struct_root)
        return struct
