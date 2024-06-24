
import os
from GoFieldFormat import GoFieldFormat
from Config import KEY_MODIFIER_NAME
from Config import EXCEL_DIR
from Config import GoCodeDir

class GoCodeGen:

    @staticmethod
    def Tab(count):
        return "    " * count;


    # 代码生成函数
    @staticmethod
    def Process(filepath, fields, table):

        # -----------------------table cfg class-----------------------
        filecontent = ""

        tablebasename = os.path.basename(filepath)
        tablebasename = tablebasename.split(".")[0]
        tablebasename = tablebasename.split("_")[0]
        tableclassname = tablebasename + "Cfg"
        filecontent += "type " + tableclassname + " struct {\n"

        for index in fields:
            fielddesc = table.cell(0, index).value
            fieldtype = table.cell(2, index).value
            fieldname = table.cell(3, index).value
            fieldvar = GoFieldFormat.Type2format[fieldtype][1]
            if fieldname == "id" or fieldname == "ID" :
                fieldname = "TableID"
            if fieldname == "Type" :
                fieldname += "N"
            filecontent += GoCodeGen.Tab(1) + fieldname + " " + fieldvar + " " + '`json:"' + fieldname + '"`'
            filecontent += GoCodeGen.Tab(1) + "//" + fielddesc + "\n"
            
            
 
        filecontent += "}\n"

        return filecontent

    # 生成配置管理类
    @staticmethod
    def GenConfigMangerCode(txt):
        path = GoCodeDir + "Table.go"

        filecontent = "\n"
        filecontent += "//-----------------------------------------------\n"
        filecontent += "//              生成代码不要修改\n"
        filecontent += "//-----------------------------------------------\n"
        filecontent += "\n"
        filecontent += "package table\n"
        filecontent += "\n"

        filecontent += txt


        # 保存
        file = open(path, "wb")
        file.write(filecontent.encode())
        file.close()
