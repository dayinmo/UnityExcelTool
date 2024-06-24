
import os
import struct
from FieldFormat import FieldFormat
from Config import DataFileName

class ConfigDataGen:

    # 保存文件
    @staticmethod
    def Save(inbytes, datapath):
        datapath += DataFileName

        filedir = os.path.dirname(datapath)
        if os.path.exists(filedir) == False:
            os.makedirs(filedir)

        byteslen = len(inbytes)
        savebytes = struct.pack('i', byteslen)
        savebytes += inbytes
        file = open(datapath, 'wb+')
        file.write(savebytes)
        file.close()
    
    @staticmethod
    def Encode2Bytes(format, val):

        if format == "i":
            if isinstance(val, int):
                bytes = struct.pack(format, int(val))
            else :
                bytes = struct.pack(format, int(0))
        elif format == "f":
            if isinstance(val, float):
                bytes = struct.pack(format, float(val))
            else :
                bytes = struct.pack(format, float(0))
        elif format == "?":
            if isinstance(val, float):
                bytes = struct.pack(format, float(val))
            else :
                bytes = struct.pack(format, bool(0))
        elif format == "s":
            newval = str(val).encode()
            vallen = len(newval)
            lenbyte = struct.pack("i", vallen)

            strformat = str(vallen) + format
            valbyte = struct.pack(strformat, newval)

            bytes = lenbyte + valbyte
            
        return bytes

    # 文件生成函数
    @staticmethod
    def Process(fields, table, languageTables):

        allbytes = bytes()

        count = 0
        for row in range(5, table.nrows):
            count += 1

            for col in range(table.ncols):
                if col in fields:
                    val = table.cell(row, col).value
                    type = table.cell(2, col).value
                    format = FieldFormat.Type2format[type][0]
                    ctype = table.cell(row, col).ctype  # 表格的数据类型
                    if ctype == 2 and val % 1 == 0.0:  # ctype为2且为浮点
                        val = int(val)  # 浮点转成整型
                    allbytes += ConfigDataGen.Encode2Bytes(format, val)

                    for x in languageTables:
                        for xcol in range(x.ncols):
                            if x.cell(3, xcol).value == table.cell(3, col).value :
                                if row < x.nrows :
                                    allbytes += ConfigDataGen.Encode2Bytes(format, x.cell(row, xcol).value)
                                else :
                                    allbytes += ConfigDataGen.Encode2Bytes(format, "")
                          
        outbytes = struct.pack('i', count)
        outbytes += allbytes

        return outbytes

