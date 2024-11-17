import yaml, os, sys, re, getopt

os.chdir(os.path.split(os.path.realpath(__file__))[0])
fconfig = open("config", "r", encoding="utf-8")
Config = yaml.load(fconfig, Loader=yaml.FullLoader)

Rule = {}

Rule = {
    "Outline": "-Edge_Cuts",
    "Top_Cu": "-F_Cu",
    "Bottom_Cu": "-B_Cu",
    "Top_SilkScreen": "-F_Silkscreen",
    "Bottom_SilkScreen": "-B_Silkscreen",
    "Top_SolderMask": "-F_Mask",
    "Bottom_SolderMask": "-B_Mask",
    "Top_SolderPaste": "-F_Paste",
    "Bottom_SolderPaste": "-B_Paste",
}

Rule_Inner = {
    "InnerLayer1_Cu": "-In1_Cu",
    "InnerLayer2_Cu": "-In2_Cu",
    "InnerLayer3_Cu": "-In3_Cu",
    "InnerLayer4_Cu": "-In4_Cu",
}


# 从命令行参数-i <xxx>获取workdir -o <xxx>获取destdir
opts, args = getopt.getopt(sys.argv[1:], "i:o:")
for opt, arg in opts:
    if opt == "-i":
        WorkDir = arg
    elif opt == "-o":
        DestDir = arg

WorkDirFiles = os.listdir(WorkDir)

if not DestDir:
    DestDir = os.path.join(WorkDir, "output")
if not os.path.exists(DestDir):
    os.mkdir(DestDir)

# 创建PCB下单必读文档
with open(os.path.join(DestDir, Config["TextFileName"]), "w") as textFile:
    textFile.write(Config["TextFileContent"])

# 检验必要文件是否齐全/重复匹配
for key, value in Rule.items():
    matchFile = []
    rePattern = re.compile(pattern=value)

    for fileName in WorkDirFiles:
        if rePattern.search(fileName):
            matchFile.append(fileName)

    if len(matchFile) < 1 and key != "Outline":
        raise Exception(key + "匹配失败")
    elif len(matchFile) > 1:
        raise Exception(key + "重复匹配")
    else:
        print(key + " -> " + matchFile[0])

# 改名和加头操作
for key, value in Rule.items():
    matchFile = ""
    rePattern = re.compile(pattern=value)

    for fileName in WorkDirFiles:
        if rePattern.search(fileName):
            matchFile = fileName

    with open(os.path.join(WorkDir, matchFile), "r") as file:
        fileData = file.read()
    with open(os.path.join(DestDir, Config["FileName"][key]), "w") as file:
        file.write(Config["Header"])
        file.write(fileData)

# 若内层存在，处理内层
for key, value in Rule_Inner.items():
    matchFile = []
    rePattern = re.compile(pattern=value)

    for fileName in WorkDirFiles:
        if rePattern.search(fileName):
            matchFile.append(fileName)

    if len(matchFile) < 1:
        continue
    elif len(matchFile) > 1:
        raise Exception(key + "重复匹配")
    else:
        print(key + " -> " + matchFile[0])

    with open(os.path.join(WorkDir, matchFile[0]), "r") as file:
        fileData = file.read()
    with open(os.path.join(DestDir, Config["FileName"][key]), "w") as file:
        file.write(Config["Header"])
        file.write(fileData)

# 复制钻孔文件
for fileName in WorkDirFiles:
    if fileName.endswith("-NPTH.drl"):
        with open(os.path.join(WorkDir, fileName), "r") as file:
            fileData = file.read()
        with open(os.path.join(DestDir, "Drill_NPTH_Through.DRL"), "w") as file:
            file.write(Config["DrillHeader"])
            file.write(fileData)
    elif fileName.endswith("-PTH.drl"):
        with open(os.path.join(WorkDir, fileName), "r") as file:
            fileData = file.read()
        with open(os.path.join(DestDir, "Drill_PTH_Through.DRL"), "w") as file:
            file.write(Config["DrillHeader"])
            file.write(fileData)

fconfig.close()
exit()
