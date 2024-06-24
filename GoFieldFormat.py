
class GoFieldFormat:
    Type2format = {
        "int": ("i", "uint32", "packet.PackReadInt32()"),
        "int32": ("i", "int32", "packet.PackReadInt32()"),
        "int64": ("i", "int64", "packet.PackReadInt64()"),
        "float": ("f", "float32", "packet.PackReadFloat()"),
        "bool": ("?", "bool", "packet.PackReadBoolean()"),
        "string": ("s", "string", "packet.PackReadString()"),

        "list[int]": ("s", "[]uint32", "SheetGenCommonFunc.GetListInt(packet.PackReadString())"),
        "list[int][int]": ("s", "[][]uint32", "SheetGenCommonFunc.GetListIntInt(packet.PackReadString())"),
        "list[float]": ("s", "[]float32", "SheetGenCommonFunc.GetListFloat(packet.PackReadString())"),
        "list[string]": ("s", "[]string", "SheetGenCommonFunc.GetListString(packet.PackReadString())"),

        "map[int|int]": ("s", "map[int]int", "SheetGenCommonFunc.GetDictIntInt(packet.PackReadString())"),
        "map[int|float]": ("s", "map[int]float32", "SheetGenCommonFunc.GetDictIntFloat(packet.PackReadString())"),
        "map[int|string]": ("s", "map[int]string", "SheetGenCommonFunc.GetDictIntString(packet.PackReadString())"),

        "map[string|int]": ("s", "map[string]int", "SheetGenCommonFunc.GetDictStringInt(packet.PackReadString())"),
        "map[string|float]": ("s", "map[string]float32", "SheetGenCommonFunc.GetDictStringFloat(packet.PackReadString())"),
        "map[string|string]": ("s", "map[string]string", "SheetGenCommonFunc.GetDictStringString(packet.PackReadString())")
    }