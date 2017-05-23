#!/usr/bin env python3
#coding=utf-8
'''
generate sampleData and resultData for report, using python
'''
import sys,re, io

rawres = sys.argv[1]
samplefh = open('{rawres}_sampleData.txt'.format(rawres=rawres.rstrip('.txt') ), 'w', encoding='utf-16')
resultfh = open('{rawres}_resultData.txt'.format(rawres=rawres.rstrip('.txt') ), 'w', encoding='utf-16')
samplefh.write('snp位点\t基因\t批次\t所属样本\t基因型\t检测结果\n')
resultfh.write('样本编号\t所属项目(动态项目名称必须正确)\t检测结果\t实验批次\n')
datecode = sys.argv[2]

taocanSampleDat = {
    'A': {'rs1042522': 'TP53'},
    'B' : {'rs1042522':'TP53', 'rs9939609':'FTO', 'rs2736100':'rs2736100' },
#     'C-男性' : ['rs1042522', 'rs9939609', 'rs2736100'],'C-女性' : ['rs1042522', 'rs9939609', 'rs2736100'],
#     'D-男性' : ['rs1042522', 'rs9939609', 'rs2736100'],'D-女性': ['rs1042522', 'rs9939609', 'rs2736100'],
#     'E-男性': ['rs1042522', 'rs9939609', 'rs2736100'],'E-女性': ['rs1042522', 'rs9939609', 'rs2736100'],
#     'F-男性': ['rs1042522', 'rs9939609', 'rs2736100'],'F-女性': ['rs1042522', 'rs9939609', 'rs2736100'],
}


taocanResultDat = {
    'A': ['抗肿瘤基因检测'],
    'B': ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测'],
    'C-男性' : ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', '肝癌（1基因）', '肺癌（1基因）', '前列腺癌（1基因）'],
    'C-女性': ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', '乳腺癌（2基因）', '卵巢癌（1基因）', '子宫内膜癌（1基因）'],
    'D-男性': ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', '肝癌（1基因）', '肺癌（1基因）', '前列腺癌（2基因）', '结直肠癌（10基因）', '胃癌（7基因）', '肾癌（7基因）', '胰腺癌（11基因）', '乳腺癌（12基因）', '软骨肉瘤（2基因）'],
    "D-女性" : ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', "结直肠癌（10基因）","胃癌（7基因）","肾癌（7基因）","胰腺癌（11基因）","乳腺癌（12基因）","卵巢癌（13基因）","子宫内膜癌（13基因）","肝癌（1基因）","肺癌（1基因）","软骨肉瘤（2基因）"],
    "E-男性" : ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', "肝癌（1基因）","肺癌（1基因）","结直肠癌（18基因）","胃癌（10基因）","肾癌（18基因）","前列腺癌（10基因）","胰腺癌（15基因）","乳腺癌（21基因）","黑色素瘤（2基因）","甲状腺癌（2基因）","视网膜母细胞瘤（1基因）","软骨肉瘤（2基因）"],
    "E-女性" : ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', "肝癌（1基因）","肺癌（1基因）","结直肠癌（18基因）","胃癌（10基因）","肾癌（18基因）","胰腺癌（15基因）","乳腺癌（21基因）","黑色素瘤（2基因）","甲状腺癌（2基因）","视网膜母细胞瘤（1基因）","软骨肉瘤（2基因）","卵巢癌（13基因）","子宫内膜癌（13基因）"],
    "F-男性" : ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', "肝癌（1基因）","肺癌（1基因）","结直肠癌（18基因）","胃癌（10基因）","肾癌（18基因）","前列腺癌（10基因）","胰腺癌（15基因）","乳腺癌（21基因）","黑色素瘤（2基因）","多发性内分泌瘤（3基因）","甲状腺癌（2基因）","甲状旁腺癌（2基因）","多发性神经纤维瘤","嗜铬细胞瘤（10基因）","视网膜母细胞瘤（1基因）","软骨肉瘤（2基因）"],
    "F-女性" : ['抗肿瘤基因检测', '肥胖基因检测', '衰老基因检测', "肝癌（1基因）","肺癌（1基因）","结直肠癌（18基因）","胃癌（10基因）","肾癌（18基因）","胰腺癌（15基因）","乳腺癌（21基因）","黑色素瘤（2基因）","多发性内分泌瘤（3基因）","甲状腺癌（2基因）","甲状旁腺癌（2基因）","多发性神经纤维瘤","嗜铬细胞瘤（10基因）","视网膜母细胞瘤（1基因）","软骨肉瘤（2基因）","卵巢癌（13基因）","子宫内膜癌（13基因）"]
}

gene2pheno = {
    'rs1042522' : {'GG': '患肿瘤的风险较高', 'GC': '存在一定患肿瘤风险', 'CG': '存在一定患肿瘤风险', 'CC': '患肿瘤的风险正常'},
    'rs9939609': {'TT': '肥胖风险较低', 'AT': '肥胖风险较高', 'TA':'肥胖风险较高', 'AA': '肥胖风险较高'},
    'rs2736100': {'GT': '衰老速度正常', 'TG': '衰老速度正常', 'TT': '衰老速度增加', 'GG': '衰老速度较缓慢'},
    'rs9275319': {'AG':'略高于普通风险', 'GA':'略高于普通风险', 'AA':'略高于普通风险', 'GG':'普通风险'},  #肝癌
    'rs36600': {'CC': '普通风险', 'CT':'略高于普通风险', 'TC':'略高于普通风险', 'TT':'略高于普通风险'}, #肺癌
    'rs817826': {'TT':'普通风险', 'TC':'略高于普通风险', 'CT':'略高于普通风险', 'CC':'略高于普通风险'}, #前列腺癌
    'rs1800440': {'AA':'普通风险', 'AC':'略高于普通风险', 'CA':'略高于普通风险', 'CC':'略高于普通风险'}, #略高于普通风险
    'rs1799949': {'CC':'普通风险', 'CT':'略高于普通风险', 'TC':'略高于普通风险', 'TT':'略高于普通风险'}, #卵巢癌
    'rs1799950': {'AA':'普通风险', 'AG':'略高于普通风险', 'GA':'略高于普通风险', 'GG':'略高于普通风险'}, #乳腺癌 BC2
    'rs1801499': {'TT':'普通风险', 'CT':'略高于普通风险', 'TC':'略高于普通风险', 'CC':'略高于普通风险'}, #乳腺癌 BC3
}
with open(rawres) as f:
    for line in f:
        temp = line.rstrip().split()
        barcode = temp[3]
        taocanType = temp[4]


        if taocanType == 'A':
            genetype = list(temp[6])
            sampleline = 'rs1042522\tTP53\t{0}\t{1}\t"{2}"\t{3}\n'.format(datecode, barcode, ','.join(genetype), gene2pheno['rs1042522'][temp[6] ] )
            resultline = '{0}\t抗肿瘤基因检测\t\t{1}\n'.format(barcode, datecode)

        elif taocanType == 'B':
            genetype = re.findall(r'[ATGC]{2}',line)
            sampleline=''
            for i,rscode in enumerate(taocanSampleDat['B']):
                sampleline += '{rs}\t{gene}\t{dat}\t{barcd}\t{genetp}\t{pheno}\n'.format(rs=rscode, gene=taocanSampleDat['B'][rscode], dat=datecode, barcd=barcode, genetp='{0},{1}'.format(genetype[i][0], genetype[i][1] ), pheno=gene2pheno[rscode][genetype[i] ] )
        samplefh.write(sampleline)
        resultfh.write(resultline)


samplefh.close()
resultfh.close()


'''

'''
