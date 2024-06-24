
import os
import xlrd
from Config import EXCEL_DIR
from Config import EXCEL_EXT
from Config import SERVER_TABLE_FIELD_FILTER
from Config import GoCodeDir
from JsonDataGen import JsonDataGen
from GoCodeGen import  GoCodeGen

class Excel2Json:
    # 构造函数
    def __init__(self):
        self.mExcelFiles = []  # 所有的excel文件

    # 外部处理函数
    def Process(self):
        self.RecursiveSearchExcel(EXCEL_DIR)
        self.ProcessExcelExportJson()

    # 递归查找文件
    def RecursiveSearchExcel(self, path):
        for pathdir in os.listdir(path):  # 遍历当前目录
            fullpath = os.path.join(path, pathdir)

            if os.path.isdir(fullpath):
                self.RecursiveSearchExcel(fullpath)
            elif os.path.isfile(fullpath):
                if os.path.splitext(fullpath)[1] == EXCEL_EXT:
                    self.mExcelFiles.append(fullpath)

    # 处理excel文件
    def ProcessExcelExportJson(self):

        result = {}

        gostruct = ""

        # 处理每个文件
        for filename in self.mExcelFiles:
            print("导出Json-文件名:%s" %filename)
            data = xlrd.open_workbook(filename)

            table = data.sheets()[0]
            languageKeys = ["EN"]
            languageTables = []
            for x in data.sheets():
                if x != table and x.name in languageKeys:
                    languageTables.append(x)
            fields = self.FilterFieldData(table, SERVER_TABLE_FIELD_FILTER)
            tablebasename = os.path.basename(filename)
            tablebasename = tablebasename.split(".")[0]
            tablebasename = tablebasename.split("_")[0]
            tableclassname = tablebasename + "Cfg"
            # 数据
            result[tableclassname] = JsonDataGen.Process(fields, table, languageTables)

            # 代码
            gostruct += GoCodeGen.Process(filename, fields, table)

        # 后处理
        JsonDataGen.Save(result, GoCodeDir)
        GoCodeGen.GenConfigMangerCode(gostruct)

    # 筛选字段数据
    def FilterFieldData(self, table, fieldfilter):
        fields = []
        for index in range(table.ncols):
            row = table.cell(1, index).value
            for field in fieldfilter:
                if row == field:
                    fields.append(index)

        return fields