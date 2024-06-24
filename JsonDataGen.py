
import os
import struct
from Config import JsonFileName
from Config import KEY_MODIFIER_NAME
import json

class JsonDataGen:

    # 保存文件
    @staticmethod
    def Save(result, datapath):
        datapath += JsonFileName

        filedir = os.path.dirname(datapath)
        if os.path.exists(filedir) == False:
            os.makedirs(filedir)

        txt = json.dumps(result, indent=4)
        file = open(datapath, 'w', encoding='utf-8')
        file.write(txt)
        file.close()

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
     
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
 
        return False
    
    # 文件生成函数
    @staticmethod
    def Process(fields, table, languageTables):
        # 获得keylist
        keylist = []
        for index in fields:
            value = table.cell(4, index).value
            if value == KEY_MODIFIER_NAME:
                keylist.append(index)

        # 根据keylist判断
        keylen = keylist.__len__()
        uselist = (keylen != 1)

        result = {}
        if uselist:
            result = []
        else:
            result = {}
        

        count = 0
        for row in range(5, table.nrows):
            rowid = table.cell(row, 0).value
            if table.cell(row, 0).ctype == 2 and rowid % 1 == 0.0:  # ctype为2且为浮点
                rowid = int(table.cell(row, 0).value)  # 浮点转成整型
            rowinfo = {}
            for col in range(table.ncols):
                fieldname = table.cell(3, col).value
                if fieldname == "id" or fieldname == "ID" :
                    fieldname = "TableID"
                if fieldname == "Type" :
                    fieldname += "N"
                if col in fields:
                    fieldtype = table.cell(2, col).value
                    val = table.cell(row, col).value

                    ctype = table.cell(row, col).ctype  # 表格的数据类型
                    if ctype == 2 and val % 1 == 0.0:  # ctype为2且为浮点
                        val = int(val)  # 浮点转成整型
                    if fieldtype == "int" :
                        if isinstance(val, int):
                            val = int(val)
                        elif JsonDataGen.is_number(str(val)):
                            val = int(val)
                        else :
                            val = 0
                    elif fieldtype == "string" :
                        val = str(val)
                    elif fieldtype == "float" :
                        if isinstance(val, float):
                            val = float(val)
                        elif JsonDataGen.is_number(str(val)):
                            val = float(val)
                        else:
                            val = 0
                    elif fieldtype == "bool" :
                        if isinstance(val, bool):
                            val = bool(val)
                        elif JsonDataGen.is_number(str(val)):
                            val = float(val)
                        else:
                            val = False
                    elif fieldtype == "list[int]" :
                        arr = []
                        strs = str(val).split(";")
                        for str1 in strs:
                            if JsonDataGen.is_number(str(str1)) :
                                arr.append(int(str1))
                        val = arr
                    elif fieldtype == "list[int][int]" :
                        arr1 = []
                        if len(val) > 0 :
                            strs1 = str(val).split("|")
                            for str1 in strs1:
                                strs2 = str1.split(";")
                                arr2 = []
                                for str2 in strs2:
                                    if JsonDataGen.is_number(str(str2)) :
                                        arr2.append(int(str2))
                                arr1.append(arr2)
                        val = arr1
                    elif fieldtype == "list[float]" :
                        arr = []
                        strs = str(val).split(";")
                        for str1 in strs:  
                            if JsonDataGen.is_number(str(str1)) :
                                arr.append(float(str1))
                        val = arr
                    elif fieldtype == "list[string]" :
                        arr = []
                        if len(val) > 0 :
                            strs = str(val).split(";")
                            for str1 in strs:
                                arr.append(str1)
                        val = arr
                    elif fieldtype == "map[int|int]" :
                        dic = {}
                        strs = str(val).split("|")
                        for str1 in strs:
                            keyvalue = str1.split(";")
                            if JsonDataGen.is_number(str(keyvalue[0])) and len(keyvalue) > 1 and JsonDataGen.is_number(str(keyvalue[1])) :
                                dic[int(keyvalue[0])] = int(keyvalue[1])
                        val = dic
                    elif fieldtype == "map[int|float]" :
                        dic = {}
                        strs = str(val).split("|")
                        for str1 in strs:
                            keyvalue = str1.split(";")
                            if JsonDataGen.is_number(str(keyvalue[0])) and len(keyvalue) > 1 and JsonDataGen.is_number(str(keyvalue[1])) :
                                dic[int(keyvalue[0])] = float(keyvalue[1])
                        val = dic
                    elif fieldtype == "map[int|string]" :
                        dic = {}
                        strs = str(val).split("|")
                        for str1 in strs:
                            keyvalue = str1.split(";")
                            if JsonDataGen.is_number(str(keyvalue[0])) :
                                dic[int(keyvalue[0])] = keyvalue[1]
                        val = dic
                    elif fieldtype == "map[string|int]" :
                        dic = {}
                        strs = str(val).split("|")
                        for str1 in strs:
                            keyvalue = str1.split(";")
                            if len(keyvalue) > 1 :
                                dic[keyvalue[0]] = int(keyvalue[1])
                        val = dic
                    elif fieldtype == "map[string|float]" :
                        dic = {}
                        strs = str(val).split("|")
                        for str1 in strs:
                            keyvalue = str1.split(";")
                            if len(keyvalue) > 1 :
                                dic[keyvalue[0]] = float(keyvalue[1])
                        val = dic
                    elif fieldtype == "map[string|string]" :
                        dic = {}
                        strs = str(val).split("|")
                        for str1 in strs:
                            keyvalue = str1.split(";")
                            if len(keyvalue) > 1 :
                                dic[keyvalue[0]] = keyvalue[1]
                        val = dic

                    rowinfo[fieldname] = val

                    for x in languageTables:
                        for xcol in range(x.ncols):
                            if x.cell(3, xcol).value == fieldname :
                                if row < x.nrows :
                                    rowinfo[x.name + "" + fieldname] = x.cell(row, xcol).value
                                else :
                                    rowinfo[x.name + "" + fieldname] = ""
            count += 1
            # 将字典存入列表
            if uselist:
                result.append(rowinfo)
            else:
                result[rowid] = rowinfo
        return result

