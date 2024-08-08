部位ID_名称_map = {0: '头盔', 1: '身体', 2: '腕甲', 3: '腰甲', 4: '腿部'}
部位ID_路径_map = {0: 'helm', 1: 'body', 2: 'arm', 3: 'wst', 4: 'leg'}
部位路径_ID_map = {v: k for k, v in 部位ID_路径_map.items()}

PP_MAPPING = [{'001_0000': '皮制头饰', '002_0000': '猎人头盔', '002_0010': '猎人头盔β', '003_0000': '骨制头盔',
               '004_0000': '合金头盔', '007_0000': '巨蜂头盔', '007_0001': '精英巨蜂头盔α', '008_0000': '贼龙头盔',
               '008_0001': '精英贼龙头盔α', '009_0000': '搔鸟头盔', '009_0001': '精英搔鸟头盔α',
               '010_0000': '毒妖鸟头盔', '010_0001': '精英毒妖鸟头盔α', '010_0010': '毒妖鸟头盔β',
               '010_0101': '精英妖水头盔α', '011_0000': '泥鱼龙头盔', '011_0001': '精英泥鱼龙头盔α',
               '012_0000': '土砂龙头盔', '012_0001': '精英土砂龙头盔α', '013_0000': '飞雷龙头盔',
               '013_0001': '精英飞雷龙头盔α', '013_0101': '精英朱毒头盔α', '014_0000': '锁甲头饰',
               '015_0000': '突击龙角α', '017_0000': '巨甲虫头盔', '017_0001': '精英巨甲虫头盔α', '018_0000': '原型头盔',
               '019_0000': '独角仙护头', '020_0000': '蛮颚龙头盔', '020_0001': '精英蛮颚龙头盔α',
               '020_0010': '蛮颚龙头盔β', '020_0011': '精英蛮颚龙头盔β', '020_0101': '精英雷颚头盔α',
               '020_0111': '精英雷颚头盔β', '021_0000': '雌火龙头盔', '021_0001': '精英雌火龙头盔α',
               '021_0010': '雌火龙头盔β', '021_0011': '精英雌火龙头盔β', '021_0100': '火龙心头盔α',
               '021_0101': '精英火龙心头盔α', '021_0110': '火龙心头盔β', '021_0111': '精英火龙心头盔β',
               '021_0200': '精英金黄澄月头盔α', '021_0210': '精英金黄澄月头盔β', '022_0000': '痹贼龙头盔',
               '022_0001': '精英痹贼龙头盔α', '023_0000': '眩鸟头盔', '023_0001': '精英眩鸟头盔α',
               '024_0000': '浮空龙头盔', '024_0001': '精英浮空龙头盔α', '024_0101': '精英浮梦头盔α',
               '025_0000': '矿石头盔', '026_0000': '死神首脑', '027_0000': '风漂龙头盔', '027_0001': '精英风漂龙头盔α',
               '027_0010': '风漂龙头盔β', '027_0011': '精英风漂龙头盔β', '027_0500': '精英霜漂头盔α',
               '027_0510': '精英霜漂头盔β', '028_0000': '骨锤龙头盔', '028_0001': '精英骨锤龙头盔α',
               '028_0010': '骨锤龙头盔β', '029_0000': '惨爪龙头盔', '029_0001': '精英惨爪头盔α',
               '029_0010': '惨爪龙头盔β', '029_0011': '精英惨爪头盔β', '029_0101': '精英亡爪头盔α',
               '029_0111': '精英亡爪头盔β', '030_0000': '战纹头盔α', '030_0010': '战纹头盔β', '030_0020': '战纹头盔γ',
               '030_0500': '精英狂纹头盔α', '030_0510': '精英狂纹头盔β', '031_0000': '铸铁头盔',
               '032_0000': '乌尔德头盔α', '032_0010': '乌尔德头盔β', '032_0020': '乌尔德头盔γ',
               '032_0500': '精英死灭头盔α', '032_0510': '精英死灭头盔β', '033_0000': '火龙头盔',
               '033_0001': '精英火龙头盔α', '033_0010': '火龙头盔β', '033_0011': '精英火龙头盔β',
               '033_0100': '火龙魂头盔α', '033_0101': '精英火龙魂头盔α', '033_0110': '火龙魂头盔β',
               '033_0111': '精英火龙魂头盔β', '033_0200': '精英银白耀日头盔α', '033_0210': '精英银白耀日头盔β',
               '034_0000': '角龙头盔', '034_0001': '精英角龙头盔α', '034_0010': '角龙头盔β',
               '034_0011': '精英角龙头盔β', '034_0100': '暴君角龙头盔α', '034_0101': '精英暴君角龙头盔α',
               '034_0110': '暴君角龙头盔β', '034_0111': '精英暴君角龙头盔β', '035_0000': '麒麟角',
               '035_0001': '精英麒麟角α', '035_0010': '麒麟角β', '035_0011': '精英麒麟角β', '035_0020': '麒麟角γ',
               '036_0000': '旅团帽', '037_0000': '爆碎羽饰', '038_0000': '铸岛熔岩头饰α', '038_0010': '铸岛熔岩头饰β',
               '038_0020': '铸岛熔岩头饰γ', '039_0000': '岩贼龙头盔α', '039_0001': '精英岩贼龙头盔α',
               '040_0000': '熔岩龙头盔α', '040_0001': '精英熔岩龙头盔α', '040_0010': '熔岩龙头盔β',
               '041_0000': '爆锤龙头盔α', '041_0001': '精英爆锤龙头盔α', '041_0010': '爆锤龙头盔β',
               '042_0000': '爆鳞龙头盔α', '042_0010': '爆鳞龙头盔β', '042_0500': '精英矜持头盔α',
               '042_0510': '精英矜持头盔β', '043_0000': '大马士革头盔α', '043_0010': '大马士革头盔β',
               '044_0000': '杜宾头盔α', '045_0000': '冥灯幽火头饰α', '045_0010': '冥灯幽火头饰β',
               '045_0020': '冥灯幽火头饰γ', '046_0000': '帝王皇冠α', '046_0001': '精英帝王皇冠α',
               '046_0010': '帝王皇冠β', '046_0011': '精英帝王皇冠β', '046_0020': '帝王皇冠γ', '047_0000': '钢龙强力α',
               '047_0001': '精英钢龙强力α', '047_0010': '钢龙强力β', '047_0011': '精英钢龙强力β',
               '047_0020': '钢龙强力γ', '048_0000': '公会十字头饰α', '049_0000': '绚辉龙铠罗头盔α',
               '049_0001': '精英绚辉龙铠罗头盔α', '049_0010': '绚辉龙铠罗头盔β', '049_0011': '精英绚辉龙铠罗头盔β',
               '049_0020': '绚辉龙铠罗头盔γ', '050_0000': '残虐头盔α', '050_0010': '残虐头盔β',
               '050_0500': '精英贪欲头盔α', '050_0510': '精英贪欲头盔β', '051_0000': '皇后琴弦α',
               '051_0001': '精英皇后扇形头盔α', '051_0010': '皇后琴弦β', '051_0011': '精英皇后扇形头盔β',
               '051_0020': '皇后琴弦γ', '052_0000': '精英煌黑龙智慧α', '052_0010': '精英煌黑龙智慧β',
               '053_0000': '追踪者头饰α', '054_0000': '骷髅面罩α', '055_0000': '艾露猫头套α', '056_0000': '蘑菇猪头套α',
               '057_0000': '燕尾蝶男护头', '057_0010': '燕尾蝶男护头β', '058_0000': '猫蜥龙护目镜',
               '059_0000': '封龙耳饰α', '060_0000': '知性眼镜α', '061_0000': '龙王的独眼α', '062_0000': '墨镜α',
               '063_0000': '封印的眼罩α', '064_0000': '摇曳鳗头套α', '065_0000': '扒手龙头套α',
               '066_0000': '黎明武士寂头部', '066_0010': '黎明武士誉头部', '067_0000': '铠武者头部',
               '069_0000': '隆面罩', '070_0000': '樱面罩α', '071_0000': '但丁假发α', '072_0000': '苍星之将头盔α',
               '072_0001': '苍世武士服装头部', '073_0000': '腾龙战盔α', '074_0000': '盛开头饰',
               '075_0000': '潜水员修诺', '076_0000': '收获头饰', '077_0000': '猎户星头饰', '078_0000': '盛装头饰',
               '080_0000': '精英迅龙头盔α', '080_0010': '精英迅龙头盔β', '081_0000': '精英斩龙头盔α',
               '081_0010': '精英斩龙头盔β', '081_0100': '精英斩黄头盔α', '081_0110': '精英斩黄头盔β',
               '082_0000': '精英碎龙头盔α', '082_0010': '精英碎龙头盔β', '082_0500': '精英铁腕头盔α',
               '082_0510': '精英铁腕头盔β', '083_0000': '精英轰龙头盔α', '083_0010': '精英轰龙头盔β',
               '083_0100': '精英轰吼头盔α', '083_0110': '精英轰吼头盔β', '084_0000': '精英猛牛龙头盔α',
               '084_0010': '精英猛牛龙头盔β', '085_0000': '精英雪崩头盔α', '085_0010': '精英雪崩头盔β',
               '085_0020': '精英雪崩头盔γ', '086_0000': '精英触角头盔α', '086_0010': '精英触角头盔β',
               '086_0020': '精英触角头盔γ', '087_0000': '精英龙纹刻印封冠α', '087_0010': '精英龙纹刻印封冠β',
               '088_0000': '精英迦楼罗头盔α', '088_0010': '精英迦楼罗头盔β', '089_0000': '精英冰牙龙头盔α',
               '089_0010': '精英冰牙龙头盔β', '089_0500': '精英霜刃冰牙龙头盔α', '089_0510': '精英霜刃冰牙龙头盔β',
               '091_0000': '机械服装头部', '092_0000': '公会成果服装头部', '093_0000': '黑带服装头部',
               '094_0000': '公会宫殿服装头部', '095_0000': '敏捷耳饰服装', '095_0010': '佯动耳饰服装',
               '096_0000': '精灵鹿头套服装', '097_0000': '草食龙头套服装', '098_0000': '企鹅头套服装',
               '099_0000': '骷髅方巾服装', '100_0000': '封印的龙骸布服装', '101_0000': '龙人族之耳服装',
               '102_0000': '精英冰豺狼围巾α', '104_0000': '精英弧锁头盔α', '104_0010': '精英弧锁头盔β',
               '105_0000': '冰狼服装头部', '106_0000': '浴场服装头', '107_0000': '精英雷狼龙头盔α',
               '107_0010': '精英雷狼龙头盔β', '107_0100': '精英狱狼龙头盔α', '107_0110': '精英狱狼龙头盔β',
               '108_0000': '精英黑狼鸟头盔α', '108_0010': '精英黑狼鸟头盔β', '109_0000': '精英金色毛发α',
               '109_0010': '精英金色毛发β', '109_0500': '精英齐天毛发α', '109_0510': '精英齐天毛发β',
               '110_0000': '精英冰鱼龙头盔α', '111_0000': '兔耳朵服装', '112_0000': '柔毛秧鸡服装',
               '113_0000': '温泉银猴服装', '113_0001': '温泉金猴服装', '114_0000': '飞雷龙围巾服装',
               '116_0000': '甲虫服装头部', '117_0000': '蝴蝶服装头部', '118_0000': '杰洛特面罩α',
               '119_0000': '希里面罩α', '120_0000': '巴耶克服装头部', '121_0000': '防卫队头盔α',
               '122_0000': '结云服装头', '123_0000': '银骑士服装头部', '124_0000': '蔷薇服装头部',
               '125_0000': '热情服装头部', '126_0000': '魔界之主服装头部', '127_0000': '风火轮服装头部',
               '128_0000': '阿斯特拉服装头部', '129_0000': '精英龙头头盔α', '129_0010': '精英龙头头盔β',
               '130_0000': '里昂服装头部', '131_0000': '克莱尔服装头部', '132_0010': '精英阿尔忒弥斯面罩α',
               '133_0000': '狩猎女神服装头部'},
              {'001_0000': '皮制服饰', '002_0000': '猎人铠甲', '002_0010': '猎人铠甲β', '003_0000': '骨制铠甲',
               '004_0000': '合金铠甲', '007_0000': '巨蜂铠甲', '007_0001': '精英巨蜂铠甲α', '008_0000': '贼龙铠甲',
               '008_0001': '精英贼龙铠甲α', '009_0000': '搔鸟铠甲', '009_0001': '精英搔鸟铠甲α',
               '010_0000': '毒妖鸟铠甲', '010_0001': '精英毒妖鸟铠甲α', '010_0010': '毒妖鸟铠甲β',
               '010_0101': '精英妖水铠甲α', '011_0000': '泥鱼龙铠甲', '011_0001': '精英泥鱼龙铠甲α',
               '012_0000': '土砂龙铠甲', '012_0001': '精英土砂龙铠甲α', '013_0000': '飞雷龙铠甲',
               '013_0001': '精英飞雷龙铠甲α', '013_0101': '精英朱毒铠甲α', '014_0000': '锁甲服饰',
               '016_0000': '酸翼龙斗篷α', '017_0000': '巨甲虫铠甲', '017_0001': '精英巨甲虫铠甲α',
               '018_0000': '原型铠甲', '019_0000': '独角仙上身', '020_0000': '蛮颚龙铠甲',
               '020_0001': '精英蛮颚龙铠甲α', '020_0010': '蛮颚龙铠甲β', '020_0011': '精英蛮颚龙铠甲β',
               '020_0101': '精英雷颚铠甲α', '020_0111': '精英雷颚铠甲β', '021_0000': '雌火龙铠甲',
               '021_0001': '精英雌火龙铠甲α', '021_0010': '雌火龙铠甲β', '021_0011': '精英雌火龙铠甲β',
               '021_0100': '火龙心铠甲α', '021_0101': '精英火龙心铠甲α', '021_0110': '火龙心铠甲β',
               '021_0111': '精英火龙心铠甲β', '021_0200': '精英金黄澄月铠甲α', '021_0210': '精英金黄澄月铠甲β',
               '022_0000': '痹贼龙铠甲', '022_0001': '精英痹贼龙铠甲α', '023_0000': '眩鸟铠甲',
               '023_0001': '精英眩鸟铠甲α', '024_0000': '浮空龙铠甲', '024_0001': '精英浮空龙铠甲α',
               '024_0101': '精英浮梦铠甲α', '025_0000': '矿石铠甲', '026_0000': '死神肌肉', '027_0000': '风漂龙铠甲',
               '027_0001': '精英风漂龙铠甲α', '027_0010': '风漂龙铠甲β', '027_0011': '精英风漂龙铠甲β',
               '027_0500': '精英霜漂铠甲α', '027_0510': '精英霜漂铠甲β', '028_0000': '骨锤龙铠甲',
               '028_0001': '精英骨锤龙铠甲α', '028_0010': '骨锤龙铠甲β', '029_0000': '惨爪龙铠甲',
               '029_0001': '精英惨爪铠甲α', '029_0010': '惨爪龙铠甲β', '029_0011': '精英惨爪铠甲β',
               '029_0101': '精英亡爪铠甲α', '029_0111': '精英亡爪铠甲β', '030_0000': '战纹铠甲α',
               '030_0010': '战纹铠甲β', '030_0020': '战纹铠甲γ', '030_0500': '精英狂纹铠甲α',
               '030_0510': '精英狂纹铠甲β', '031_0000': '铸铁铠甲', '032_0000': '乌尔德铠甲α',
               '032_0010': '乌尔德铠甲β', '032_0020': '乌尔德铠甲γ', '032_0500': '精英死灭铠甲α',
               '032_0510': '精英死灭铠甲β', '033_0000': '火龙铠甲', '033_0001': '精英火龙铠甲α',
               '033_0010': '火龙铠甲β', '033_0011': '精英火龙铠甲β', '033_0100': '火龙魂铠甲α',
               '033_0101': '精英火龙魂铠甲α', '033_0110': '火龙魂铠甲β', '033_0111': '精英火龙魂铠甲β',
               '033_0200': '精英银白耀日铠甲α', '033_0210': '精英银白耀日铠甲β', '034_0000': '角龙铠甲',
               '034_0001': '精英角龙铠甲α', '034_0010': '角龙铠甲β', '034_0011': '精英角龙铠甲β',
               '034_0100': '暴君角龙铠甲α', '034_0101': '精英暴君角龙铠甲α', '034_0110': '暴君角龙铠甲β',
               '034_0111': '精英暴君角龙铠甲β', '035_0000': '麒麟服饰', '035_0001': '精英麒麟服饰α',
               '035_0010': '麒麟服饰β', '035_0011': '精英麒麟服饰β', '035_0020': '麒麟服饰γ', '036_0000': '旅团战衣',
               '038_0000': '铸岛熔岩皮α', '038_0010': '铸岛熔岩皮β', '038_0020': '铸岛熔岩皮γ',
               '039_0000': '岩贼龙铠甲α', '039_0001': '精英岩贼龙铠甲α', '040_0000': '熔岩龙铠甲α',
               '040_0001': '精英熔岩龙铠甲α', '040_0010': '熔岩龙铠甲β', '041_0000': '爆锤龙铠甲α',
               '041_0001': '精英爆锤龙铠甲α', '041_0010': '爆锤龙铠甲β', '042_0000': '爆鳞龙铠甲α',
               '042_0010': '爆鳞龙铠甲β', '042_0500': '精英矜持铠甲α', '042_0510': '精英矜持铠甲β',
               '043_0000': '大马士革铠甲α', '043_0010': '大马士革铠甲β', '044_0000': '杜宾铠甲α',
               '045_0000': '冥灯幽火皮α', '045_0010': '冥灯幽火皮β', '045_0020': '冥灯幽火皮γ', '046_0000': '帝王铠甲α',
               '046_0001': '精英帝王铠甲α', '046_0010': '帝王铠甲β', '046_0011': '精英帝王铠甲β',
               '046_0020': '帝王铠甲γ', '047_0000': '钢龙恐惧α', '047_0001': '精英钢龙恐惧α', '047_0010': '钢龙恐惧β',
               '047_0011': '精英钢龙恐惧β', '047_0020': '钢龙恐惧γ', '048_0000': '公会十字战衣α',
               '049_0000': '绚辉龙铠罗铠甲α', '049_0001': '精英绚辉龙铠罗铠甲α', '049_0010': '绚辉龙铠罗铠甲β',
               '049_0011': '精英绚辉龙铠罗铠甲β', '049_0020': '绚辉龙铠罗铠甲γ', '050_0000': '残虐铠甲α',
               '050_0010': '残虐铠甲β', '050_0500': '精英贪欲铠甲α', '050_0510': '精英贪欲铠甲β',
               '051_0000': '皇后铠甲α', '051_0001': '精英皇后铠甲α', '051_0010': '皇后铠甲β',
               '051_0011': '精英皇后铠甲β', '051_0020': '皇后铠甲γ', '052_0000': '精英煌黑龙灵魂α',
               '052_0010': '精英煌黑龙灵魂β', '053_0000': '追踪者服饰α', '057_0000': '燕尾蝶男上身',
               '057_0010': '燕尾蝶男上身β', '066_0000': '黎明武士寂身体', '066_0010': '黎明武士誉身体',
               '067_0000': '铠武者身体', '069_0000': '隆身体', '070_0000': '樱身体α', '071_0000': '但丁风衣α',
               '072_0000': '苍星之将铠甲α', '072_0001': '苍世武士服装身体', '073_0000': '腾龙战铠α',
               '074_0000': '盛开服饰', '075_0000': '潜水员服装', '076_0000': '收获装甲', '077_0000': '猎户星服饰',
               '078_0000': '盛装战衣', '080_0000': '精英迅龙铠甲α', '080_0010': '精英迅龙铠甲β',
               '081_0000': '精英斩龙铠甲α', '081_0010': '精英斩龙铠甲β', '081_0100': '精英斩黄铠甲α',
               '081_0110': '精英斩黄铠甲β', '082_0000': '精英碎龙铠甲α', '082_0010': '精英碎龙铠甲β',
               '082_0500': '精英铁腕铠甲α', '082_0510': '精英铁腕铠甲β', '083_0000': '精英轰龙铠甲α',
               '083_0010': '精英轰龙铠甲β', '083_0100': '精英轰吼铠甲α', '083_0110': '精英轰吼铠甲β',
               '084_0000': '精英猛牛龙铠甲α', '084_0010': '精英猛牛龙铠甲β', '085_0000': '精英雪崩铠甲α',
               '085_0010': '精英雪崩铠甲β', '085_0020': '精英雪崩铠甲γ', '086_0000': '精英触角铠甲α',
               '086_0010': '精英触角铠甲β', '086_0020': '精英触角铠甲γ', '087_0000': '精英龙纹刻印封铠α',
               '087_0010': '精英龙纹刻印封铠β', '088_0000': '精英迦楼罗铠甲α', '088_0010': '精英迦楼罗铠甲β',
               '089_0000': '精英冰牙龙铠甲α', '089_0010': '精英冰牙龙铠甲β', '089_0500': '精英霜刃冰牙龙铠甲α',
               '089_0510': '精英霜刃冰牙龙铠甲β', '091_0000': '机械服装身体', '092_0000': '公会成果服装身体',
               '093_0000': '黑带服装身体', '094_0000': '公会宫殿服装身体', '103_0000': '精英冬翼龙斗篷α',
               '104_0000': '精英弧锁铠甲α', '105_0000': '冰狼服装身体', '106_0000': '浴场服装身体',
               '107_0000': '精英雷狼龙铠甲α', '107_0010': '精英雷狼龙铠甲β', '107_0100': '精英狱狼龙铠甲α',
               '107_0110': '精英狱狼龙铠甲β', '108_0000': '精英黑狼鸟铠甲α', '108_0010': '精英黑狼鸟铠甲β',
               '109_0000': '精英金色羽织α', '109_0010': '精英金色羽织β', '109_0500': '精英齐天衣α',
               '109_0510': '精英齐天衣β', '110_0000': '精英冰鱼龙铠甲α', '115_0000': '精英健美身体α',
               '115_0001': '健美γ服装身体', '116_0000': '甲虫服装身体', '117_0000': '蝴蝶服装身体',
               '118_0000': '杰洛特身体α', '119_0000': '希里身体α', '120_0000': '巴耶克服装身体',
               '121_0000': '防卫队铠甲α', '122_0000': '结云服装身体', '123_0000': '银骑士服装身体',
               '124_0000': '蔷薇服装身体', '125_0000': '热情服装身体', '126_0000': '魔界之主服装身体',
               '127_0000': '风火轮服装身体', '128_0000': '阿斯特拉服装身体', '129_0000': '精英龙皮α',
               '129_0010': '精英龙皮β', '130_0000': '里昂服装身体', '131_0000': '克莱尔服装身体',
               '132_0010': '精英阿尔忒弥斯身体α', '133_0000': '狩猎女神服装身体', '500_0000': '内衣α服装身体',
               '501_0000': '内衣β服装身体'},
              {'001_0000': '皮制手套', '002_0000': '猎人腕甲', '002_0010': '猎人腕甲β', '003_0000': '骨制腕甲',
               '004_0000': '合金腕甲', '005_0000': '冠突龙护手', '007_0000': '巨蜂腕甲', '007_0001': '精英巨蜂腕甲α',
               '008_0000': '贼龙腕甲', '008_0001': '精英贼龙腕甲α', '009_0000': '搔鸟腕甲', '009_0001': '精英搔鸟腕甲α',
               '010_0000': '毒妖鸟腕甲', '010_0001': '精英毒妖鸟腕甲α', '010_0010': '毒妖鸟腕甲β',
               '010_0101': '精英妖水腕甲α', '011_0000': '泥鱼龙腕甲', '011_0001': '精英泥鱼龙腕甲α',
               '012_0000': '土砂龙腕甲', '012_0001': '精英土砂龙腕甲α', '013_0000': '飞雷龙腕甲',
               '013_0001': '精英飞雷龙腕甲α', '013_0101': '精英朱毒腕甲α', '014_0000': '锁甲手套',
               '017_0000': '巨甲虫腕甲', '017_0001': '精英巨甲虫腕甲α', '018_0000': '原型腕甲',
               '019_0000': '独角仙护袖', '020_0000': '蛮颚龙腕甲', '020_0001': '精英蛮颚龙腕甲α',
               '020_0010': '蛮颚龙腕甲β', '020_0011': '精英蛮颚龙腕甲β', '020_0101': '精英雷颚腕甲α',
               '020_0111': '精英雷颚腕甲β', '021_0000': '雌火龙腕甲', '021_0001': '精英雌火龙腕甲α',
               '021_0010': '雌火龙腕甲β', '021_0011': '精英雌火龙腕甲β', '021_0100': '火龙心腕甲α',
               '021_0101': '精英火龙心腕甲α', '021_0110': '火龙心腕甲β', '021_0111': '精英火龙心腕甲β',
               '021_0200': '精英金黄澄月腕甲α', '021_0210': '精英金黄澄月腕甲β', '022_0000': '痹贼龙腕甲',
               '022_0001': '精英痹贼龙腕甲α', '023_0000': '眩鸟腕甲', '023_0001': '精英眩鸟腕甲α',
               '024_0000': '浮空龙腕甲', '024_0001': '精英浮空龙腕甲α', '024_0101': '精英浮梦腕甲α',
               '025_0000': '矿石腕甲', '026_0000': '死神双手', '027_0000': '风漂龙腕甲', '027_0001': '精英风漂龙腕甲α',
               '027_0010': '风漂龙腕甲β', '027_0011': '精英风漂龙腕甲β', '027_0500': '精英霜漂腕甲α',
               '027_0510': '精英霜漂腕甲β', '028_0000': '骨锤龙腕甲', '028_0001': '精英骨锤龙腕甲α',
               '028_0010': '骨锤龙腕甲β', '029_0000': '惨爪龙腕甲', '029_0001': '精英惨爪腕甲α',
               '029_0010': '惨爪龙腕甲β', '029_0011': '精英惨爪腕甲β', '029_0101': '精英亡爪腕甲α',
               '029_0111': '精英亡爪腕甲β', '030_0000': '战纹腕甲α', '030_0010': '战纹腕甲β', '030_0020': '战纹腕甲γ',
               '030_0500': '精英狂纹腕甲α', '030_0510': '精英狂纹腕甲β', '031_0000': '铸铁腕甲',
               '032_0000': '乌尔德腕甲α', '032_0010': '乌尔德腕甲β', '032_0020': '乌尔德腕甲γ',
               '032_0500': '精英死灭腕甲α', '032_0510': '精英死灭腕甲β', '033_0000': '火龙腕甲',
               '033_0001': '精英火龙腕甲α', '033_0010': '火龙腕甲β', '033_0011': '精英火龙腕甲β',
               '033_0100': '火龙魂腕甲α', '033_0101': '精英火龙魂腕甲α', '033_0110': '火龙魂腕甲β',
               '033_0111': '精英火龙魂腕甲β', '033_0200': '精英银白耀日腕甲α', '033_0210': '精英银白耀日腕甲β',
               '034_0000': '角龙腕甲', '034_0001': '精英角龙腕甲α', '034_0010': '角龙腕甲β',
               '034_0011': '精英角龙腕甲β', '034_0100': '暴君角龙腕甲α', '034_0101': '精英暴君角龙腕甲α',
               '034_0110': '暴君角龙腕甲β', '034_0111': '精英暴君角龙腕甲β', '035_0000': '麒麟长腕甲',
               '035_0001': '精英麒麟长腕甲α', '035_0010': '麒麟长腕甲β', '035_0011': '精英麒麟长腕甲β',
               '035_0020': '麒麟长腕甲γ', '036_0000': '旅团腕甲', '038_0000': '铸岛熔岩钢爪α',
               '038_0010': '铸岛熔岩钢爪β', '038_0020': '铸岛熔岩钢爪γ', '039_0000': '岩贼龙腕甲α',
               '039_0001': '精英岩贼龙腕甲α', '040_0000': '熔岩龙腕甲α', '040_0001': '精英熔岩龙腕甲α',
               '040_0010': '熔岩龙腕甲β', '041_0000': '爆锤龙腕甲α', '041_0001': '精英爆锤龙腕甲α',
               '041_0010': '爆锤龙腕甲β', '042_0000': '爆鳞龙腕甲α', '042_0010': '爆鳞龙腕甲β',
               '042_0500': '精英矜持腕甲α', '042_0510': '精英矜持腕甲β', '043_0000': '大马士革腕甲α',
               '043_0010': '大马士革腕甲β', '044_0000': '杜宾腕甲α', '045_0000': '冥灯幽火钢爪α',
               '045_0010': '冥灯幽火钢爪β', '045_0020': '冥灯幽火钢爪γ', '046_0000': '帝王腕甲α',
               '046_0001': '精英帝王腕甲α', '046_0010': '帝王腕甲β', '046_0011': '精英帝王腕甲β',
               '046_0020': '帝王腕甲γ', '047_0000': '钢龙刚强α', '047_0001': '精英钢龙刚强α', '047_0010': '钢龙刚强β',
               '047_0011': '精英钢龙刚强β', '047_0020': '钢龙刚强γ', '048_0000': '公会十字腕甲α',
               '049_0000': '绚辉龙铠罗腕甲α', '049_0001': '精英绚辉龙铠罗腕甲α', '049_0010': '绚辉龙铠罗腕甲β',
               '049_0011': '精英绚辉龙铠罗腕甲β', '049_0020': '绚辉龙铠罗腕甲γ', '050_0000': '残虐腕甲α',
               '050_0010': '残虐腕甲β', '050_0500': '精英贪欲腕甲α', '050_0510': '精英贪欲腕甲β',
               '051_0000': '皇后腕甲α', '051_0001': '精英皇后腕甲α', '051_0010': '皇后腕甲β',
               '051_0011': '精英皇后腕甲β', '051_0020': '皇后腕甲γ', '052_0000': '精英煌黑龙长腕α',
               '052_0010': '精英煌黑龙长腕β', '053_0000': '追踪者手套α', '057_0000': '燕尾蝶男护袖',
               '057_0010': '燕尾蝶男护袖β', '066_0000': '黎明武士寂腕部', '066_0010': '黎明武士誉腕部',
               '067_0000': '铠武者腕部', '069_0000': '隆腕甲', '070_0000': '樱腕甲α', '071_0000': '但丁手套α',
               '072_0000': '苍星之将腕甲α', '072_0001': '精英苍世武士袖α', '073_0000': '腾龙腕甲α',
               '074_0000': '盛开手套', '075_0000': '潜水员腕甲', '076_0000': '收获手套', '077_0000': '猎户星腕甲',
               '078_0000': '盛装手套', '080_0000': '精英迅龙腕甲α', '080_0010': '精英迅龙腕甲β',
               '081_0000': '精英斩龙腕甲α', '081_0010': '精英斩龙腕甲β', '081_0100': '精英斩黄腕甲α',
               '081_0110': '精英斩黄腕甲β', '082_0000': '精英碎龙腕甲α', '082_0010': '精英碎龙腕甲β',
               '082_0500': '精英铁腕腕甲α', '082_0510': '精英铁腕腕甲β', '083_0000': '精英轰龙腕甲α',
               '083_0010': '精英轰龙腕甲β', '083_0100': '精英轰吼腕甲α', '083_0110': '精英轰吼腕甲β',
               '084_0000': '精英猛牛龙腕甲α', '084_0010': '精英猛牛龙腕甲β', '085_0000': '精英雪崩腕甲α',
               '085_0010': '精英雪崩腕甲β', '085_0020': '精英雪崩腕甲γ', '086_0000': '精英触角腕甲α',
               '086_0010': '精英触角腕甲β', '086_0020': '精英触角腕甲γ', '087_0000': '精英龙纹刻印封甲α',
               '087_0010': '精英龙纹刻印封甲β', '088_0000': '精英迦楼罗腕甲α', '088_0010': '精英迦楼罗腕甲β',
               '089_0000': '精英冰牙龙腕甲α', '089_0010': '精英冰牙龙腕甲β', '089_0500': '精英霜刃冰牙龙腕甲α',
               '089_0510': '精英霜刃冰牙龙腕甲β', '091_0000': '机械服装腕部', '092_0000': '公会成果服装腕部',
               '093_0000': '黑带服装腕部', '094_0000': '公会宫殿服装腕部', '104_0000': '精英弧锁腕甲α',
               '105_0000': '冰狼服装腕部', '106_0000': '浴场服装腕', '107_0000': '精英雷狼龙腕甲α',
               '107_0010': '精英雷狼龙腕甲β', '107_0100': '精英狱狼龙腕甲α', '107_0110': '精英狱狼龙腕甲β',
               '108_0000': '精英黑狼鸟腕甲α', '108_0010': '精英黑狼鸟腕甲β', '109_0000': '精英金色臂甲α',
               '109_0010': '精英金色臂甲β', '109_0500': '精英齐天臂甲α', '109_0510': '精英齐天臂甲β',
               '110_0000': '精英冰鱼龙腕甲α', '115_0000': '精英健美腕甲α', '115_0001': '健美γ服装腕部',
               '116_0000': '甲虫服装腕部', '117_0000': '蝴蝶服装腕部', '118_0000': '杰洛特腕甲α',
               '119_0000': '希里腕甲α', '120_0000': '巴耶克服装腕部', '121_0000': '防卫队手甲α',
               '122_0000': '结云服装腕部', '123_0000': '银骑士服装腕部', '124_0000': '蔷薇服装腕部',
               '125_0000': '热情服装腕部', '126_0000': '魔界之主服装腕部', '127_0000': '风火轮服装腕部',
               '128_0000': '阿斯特拉服装腕部', '129_0000': '精英龙钢爪α', '129_0010': '精英龙钢爪β',
               '130_0000': '里昂服装腕部', '131_0000': '克莱尔服装腕部', '132_0010': '精英阿尔忒弥斯腕部α',
               '133_0000': '狩猎女神服装腕部', '500_0000': '内衣α服装腕部', '501_0000': '内衣β服装腕部'},
              {'001_0000': '皮制皮带', '002_0000': '猎人腰甲', '002_0010': '猎人腰甲β', '003_0000': '骨制腰甲',
               '004_0000': '合金腰甲', '007_0000': '巨蜂腰甲', '007_0001': '精英巨蜂腰甲α', '008_0000': '贼龙腰甲',
               '008_0001': '精英贼龙腰甲α', '009_0000': '搔鸟腰甲', '009_0001': '精英搔鸟腰甲α',
               '010_0000': '毒妖鸟腰甲', '010_0001': '精英毒妖鸟腰甲α', '010_0010': '毒妖鸟腰甲β',
               '010_0101': '精英妖水腰甲α', '011_0000': '泥鱼龙腰甲', '011_0001': '精英泥鱼龙腰甲α',
               '012_0000': '土砂龙腰甲', '012_0001': '精英土砂龙腰甲α', '013_0000': '飞雷龙腰甲',
               '013_0001': '精英飞雷龙腰甲α', '013_0101': '精英朱毒腰甲α', '014_0000': '锁甲皮带',
               '017_0000': '巨甲虫腰甲', '017_0001': '精英巨甲虫腰甲α', '018_0000': '原型腰甲',
               '019_0000': '独角仙护腰具', '020_0000': '蛮颚龙腰甲', '020_0001': '精英蛮颚龙腰甲α',
               '020_0010': '蛮颚龙腰甲β', '020_0011': '精英蛮颚龙腰甲β', '020_0101': '精英雷颚腰甲α',
               '020_0111': '精英雷颚腰甲β', '021_0000': '雌火龙腰甲', '021_0001': '精英雌火龙腰甲α',
               '021_0010': '雌火龙腰甲β', '021_0011': '精英雌火龙腰甲β', '021_0100': '火龙心腰甲α',
               '021_0101': '精英火龙心腰甲α', '021_0110': '火龙心腰甲β', '021_0111': '精英火龙心腰甲β',
               '021_0200': '精英金黄澄月腰甲α', '021_0210': '精英金黄澄月腰甲β', '022_0000': '痹贼龙腰甲',
               '022_0001': '精英痹贼龙腰甲α', '023_0000': '眩鸟腰甲', '023_0001': '精英眩鸟腰甲α',
               '024_0000': '浮空龙腰甲', '024_0001': '精英浮空龙腰甲α', '024_0101': '精英浮梦腰甲α',
               '025_0000': '矿石腰甲', '026_0000': '死神脐带', '027_0000': '风漂龙腰甲', '027_0001': '精英风漂龙腰甲α',
               '027_0010': '风漂龙腰甲β', '027_0011': '精英风漂龙腰甲β', '027_0500': '精英霜漂腰甲α',
               '027_0510': '精英霜漂腰甲β', '028_0000': '骨锤龙腰甲', '028_0001': '精英骨锤龙腰甲α',
               '028_0010': '骨锤龙腰甲β', '029_0000': '惨爪龙腰甲', '029_0001': '精英惨爪腰甲α',
               '029_0010': '惨爪龙腰甲β', '029_0011': '精英惨爪腰甲β', '029_0101': '精英亡爪腰甲α',
               '029_0111': '精英亡爪腰甲β', '030_0000': '战纹腰甲α', '030_0010': '战纹腰甲β', '030_0020': '战纹腰甲γ',
               '030_0500': '精英狂纹腰甲α', '030_0510': '精英狂纹腰甲β', '031_0000': '铸铁腰甲',
               '032_0000': '乌尔德腰甲α', '032_0010': '乌尔德腰甲β', '032_0020': '乌尔德腰甲γ',
               '032_0500': '精英死灭腰甲α', '032_0510': '精英死灭腰甲β', '033_0000': '火龙腰甲',
               '033_0001': '精英火龙腰甲α', '033_0010': '火龙腰甲β', '033_0011': '精英火龙腰甲β',
               '033_0100': '火龙魂腰甲α', '033_0101': '精英火龙魂腰甲α', '033_0110': '火龙魂腰甲β',
               '033_0111': '精英火龙魂腰甲β', '033_0200': '精英银白耀日腰甲α', '033_0210': '精英银白耀日腰甲β',
               '034_0000': '角龙腰甲', '034_0001': '精英角龙腰甲α', '034_0010': '角龙腰甲β',
               '034_0011': '精英角龙腰甲β', '034_0100': '暴君角龙腰甲α', '034_0101': '精英暴君角龙腰甲α',
               '034_0110': '暴君角龙腰甲β', '034_0111': '精英暴君角龙腰甲β', '035_0000': '麒麟腰环',
               '035_0001': '精英麒麟腰环α', '035_0010': '麒麟腰环β', '035_0011': '精英麒麟腰环β',
               '035_0020': '麒麟腰环γ', '036_0000': '旅团腰甲', '038_0000': '铸岛熔岩脊椎α',
               '038_0010': '铸岛熔岩脊椎β', '038_0020': '铸岛熔岩脊椎γ', '039_0000': '岩贼龙腰甲α',
               '039_0001': '精英岩贼龙腰甲α', '040_0000': '熔岩龙腰甲α', '040_0001': '精英熔岩龙腰甲α',
               '040_0010': '熔岩龙腰甲β', '041_0000': '爆锤龙腰甲α', '041_0001': '精英爆锤龙腰甲α',
               '041_0010': '爆锤龙腰甲β', '042_0000': '爆鳞龙腰甲α', '042_0010': '爆鳞龙腰甲β',
               '042_0500': '精英矜持腰甲α', '042_0510': '精英矜持腰甲β', '043_0000': '大马士革腰甲α',
               '043_0010': '大马士革腰甲β', '044_0000': '杜宾腰甲α', '045_0000': '冥灯幽火脊椎α',
               '045_0010': '冥灯幽火脊椎β', '045_0020': '冥灯幽火脊椎γ', '046_0000': '帝王腰甲α',
               '046_0001': '精英帝王腰甲α', '046_0010': '帝王腰甲β', '046_0011': '精英帝王腰甲β',
               '046_0020': '帝王腰甲γ', '047_0000': '钢龙安稳α', '047_0001': '精英钢龙安稳α', '047_0010': '钢龙安稳β',
               '047_0011': '精英钢龙安稳β', '047_0020': '钢龙安稳γ', '048_0000': '公会十字腰甲α',
               '049_0000': '绚辉龙铠罗腰甲α', '049_0001': '精英绚辉龙铠罗腰甲α', '049_0010': '绚辉龙铠罗腰甲β',
               '049_0011': '精英绚辉龙铠罗腰甲β', '049_0020': '绚辉龙铠罗腰甲γ', '050_0000': '残虐腰甲α',
               '050_0010': '残虐腰甲β', '050_0500': '精英贪欲腰甲α', '050_0510': '精英贪欲腰甲β',
               '051_0000': '皇后腰甲α', '051_0001': '精英皇后腰甲α', '051_0010': '皇后腰甲β',
               '051_0011': '精英皇后腰甲β', '051_0020': '皇后腰甲γ', '052_0000': '精英煌黑龙神力α',
               '052_0010': '精英煌黑龙神力β', '053_0000': '追踪者皮带α', '057_0000': '燕尾蝶男护腰具',
               '057_0010': '燕尾蝶男护腰具β', '066_0000': '黎明武士寂腰部', '066_0010': '黎明武士誉腰部',
               '067_0000': '铠武者腰部', '069_0000': '隆的腰', '070_0000': '樱的腰α', '071_0000': '但丁皮带α',
               '072_0000': '苍星之将腰带α', '072_0001': '精英苍世武士带α', '073_0000': '腾龙腰甲α',
               '074_0000': '盛开风衣', '075_0000': '潜水员皮带', '076_0000': '收获护裙', '077_0000': '猎户星风衣',
               '078_0000': '盛装大衣', '080_0000': '精英迅龙腰甲α', '080_0010': '精英迅龙腰甲β',
               '081_0000': '精英斩龙腰甲α', '081_0010': '精英斩龙腰甲β', '081_0100': '精英斩黄腰甲α',
               '081_0110': '精英斩黄腰甲β', '082_0000': '精英碎龙腰甲α', '082_0010': '精英碎龙腰甲β',
               '082_0500': '精英铁腕腰甲α', '082_0510': '精英铁腕腰甲β', '083_0000': '精英轰龙腰甲α',
               '083_0010': '精英轰龙腰甲β', '083_0100': '精英轰吼腰甲α', '083_0110': '精英轰吼腰甲β',
               '084_0000': '精英猛牛龙腰甲α', '084_0010': '精英猛牛龙腰甲β', '085_0000': '精英雪崩腰甲α',
               '085_0010': '精英雪崩腰甲β', '085_0020': '精英雪崩腰甲γ', '086_0000': '精英触角腰甲α',
               '086_0010': '精英触角腰甲β', '086_0020': '精英触角腰甲γ', '087_0000': '精英龙纹刻印封带α',
               '087_0010': '精英龙纹刻印封带β', '088_0000': '精英迦楼罗腰甲α', '088_0010': '精英迦楼罗腰甲β',
               '089_0000': '精英冰牙腰甲α', '089_0010': '精英冰牙龙腰甲β', '089_0500': '精英霜刃冰牙龙腰甲α',
               '089_0510': '精英霜刃冰牙龙腰甲β', '091_0000': '机械服装腰部', '092_0000': '公会成果服装腰部',
               '093_0000': '黑带服装腰部', '094_0000': '公会宫殿服装腰部', '104_0000': '精英弧锁腰甲α',
               '105_0000': '冰狼服装腰部', '106_0000': '浴场服装腰', '107_0000': '精英雷狼龙腰甲α',
               '107_0010': '精英雷狼龙腰甲β', '107_0100': '精英狱狼龙腰甲α', '107_0110': '精英狱狼龙腰甲β',
               '108_0000': '精英黑狼鸟腰甲α', '108_0010': '精英黑狼鸟腰甲β', '109_0000': '精英金色腰带α',
               '109_0010': '精英金色腰带β', '109_0500': '精英齐天腰带α', '109_0510': '精英齐天腰带β',
               '110_0000': '精英冰鱼龙腰甲α', '115_0000': '精英健美腰部α', '115_0001': '健美γ服装腰部',
               '116_0000': '甲虫服装腰部', '117_0000': '蝴蝶服装腰部', '118_0000': '杰洛特的腰α',
               '119_0000': '希里的腰α', '120_0000': '巴耶克服装腰部', '121_0000': '防卫队腰甲α',
               '122_0000': '结云服装腰部', '123_0000': '银骑士服装腰部', '124_0000': '蔷薇服装腰部',
               '125_0000': '热情服装腰部', '126_0000': '魔界之主服装腰部', '127_0000': '风火轮服装腰部',
               '128_0000': '精英阿斯特拉裙α', '129_0000': '精英龙脊椎α', '129_0010': '精英龙脊椎β',
               '130_0000': '里昂服装腰部', '131_0000': '克莱尔服装腰部', '132_0010': '精英阿尔忒弥斯腰部α',
               '133_0000': '狩猎女神服装腰部', '500_0000': '内衣α服装腰部', '501_0000': '内衣β服装腰部'},
              {'001_0000': '皮制长裤', '002_0000': '猎人护腿', '002_0010': '猎人护腿β', '003_0000': '骨制护腿',
               '004_0000': '合金护腿', '006_0000': '咬鱼靴', '007_0000': '巨蜂护腿', '007_0001': '精英巨蜂护腿α',
               '008_0000': '贼龙护腿', '008_0001': '精英贼龙护腿α', '009_0000': '搔鸟护腿', '009_0001': '精英搔鸟护腿α',
               '010_0000': '毒妖鸟护腿', '010_0001': '精英毒妖鸟护腿α', '010_0010': '毒妖鸟护腿β',
               '010_0101': '精英妖水护腿α', '011_0000': '泥鱼龙护腿', '011_0001': '精英泥鱼龙护腿α',
               '012_0000': '土砂龙护腿', '012_0001': '精英土砂龙护腿α', '013_0000': '飞雷龙护腿',
               '013_0001': '精英飞雷龙护腿α', '013_0101': '精英朱毒护腿α', '014_0000': '锁甲长裤',
               '017_0000': '巨甲虫护腿', '017_0001': '精英巨甲虫护腿α', '018_0000': '原型护腿', '019_0000': '独角仙脚',
               '020_0000': '蛮颚龙护腿', '020_0001': '精英蛮颚龙护腿α', '020_0010': '蛮颚龙护腿β',
               '020_0011': '精英蛮颚龙护腿β', '020_0101': '精英雷颚护腿α', '020_0111': '精英雷颚护腿β',
               '021_0000': '雌火龙护腿', '021_0001': '精英雌火龙护腿α', '021_0010': '雌火龙护腿β',
               '021_0011': '精英雌火龙护腿β', '021_0100': '火龙心护腿α', '021_0101': '精英火龙心护腿α',
               '021_0110': '火龙心护腿β', '021_0111': '精英火龙心护腿β', '021_0200': '精英金黄澄月护腿α',
               '021_0210': '精英金黄澄月护腿β', '022_0000': '痹贼龙护腿', '022_0001': '精英痹贼龙护腿α',
               '023_0000': '眩鸟护腿', '023_0001': '精英眩鸟护腿α', '024_0000': '浮空龙护腿',
               '024_0001': '精英浮空龙护腿α', '024_0101': '精英浮梦护腿α', '025_0000': '矿石护腿',
               '026_0000': '死神脚跟', '027_0000': '风漂龙护腿', '027_0001': '精英风漂龙护腿α',
               '027_0010': '风漂龙护腿β', '027_0011': '精英风漂龙护腿β', '027_0500': '精英霜漂护腿α',
               '027_0510': '精英霜漂护腿β', '028_0000': '骨锤龙护腿', '028_0001': '精英骨锤龙护腿α',
               '028_0010': '骨锤龙护腿β', '029_0000': '惨爪龙护腿', '029_0001': '精英惨爪护腿α',
               '029_0010': '惨爪龙护腿β', '029_0011': '精英惨爪护腿β', '029_0101': '精英亡爪护腿α',
               '029_0111': '精英亡爪护腿β', '030_0000': '战纹护腿α', '030_0010': '战纹护腿β', '030_0020': '战纹护腿γ',
               '030_0500': '精英狂纹护腿α', '030_0510': '精英狂纹护腿β', '031_0000': '铸铁护腿',
               '032_0000': '乌尔德护腿α', '032_0010': '乌尔德护腿β', '032_0020': '乌尔德护腿γ',
               '032_0500': '精英死灭护腿α', '032_0510': '精英死灭护腿β', '033_0000': '火龙护腿',
               '033_0001': '精英火龙护腿α', '033_0010': '火龙护腿β', '033_0011': '精英火龙护腿β',
               '033_0100': '火龙魂护腿α', '033_0101': '精英火龙魂护腿α', '033_0110': '火龙魂护腿β',
               '033_0111': '精英火龙魂护腿β', '033_0200': '精英银白耀日护腿α', '033_0210': '精英银白耀日护腿β',
               '034_0000': '角龙护腿', '034_0001': '精英角龙护腿α', '034_0010': '角龙护腿β',
               '034_0011': '精英角龙护腿β', '034_0100': '暴君角龙护腿α', '034_0101': '精英暴君角龙护腿α',
               '034_0110': '暴君角龙护腿β', '034_0111': '精英暴君角龙护腿β', '035_0000': '麒麟护胫',
               '035_0001': '精英麒麟护胫α', '035_0010': '麒麟护胫β', '035_0011': '精英麒麟护胫β',
               '035_0020': '麒麟护胫γ', '036_0000': '旅团靴', '038_0000': '铸岛熔岩靴α', '038_0010': '铸岛熔岩靴β',
               '038_0020': '铸岛熔岩靴γ', '039_0000': '岩贼龙护腿α', '039_0001': '精英岩贼龙护腿α',
               '040_0000': '熔岩龙护腿α', '040_0001': '精英熔岩龙护腿α', '040_0010': '熔岩龙护腿β',
               '041_0000': '爆锤龙护腿α', '041_0001': '精英爆锤龙护腿α', '041_0010': '爆锤龙护腿β',
               '042_0000': '爆鳞龙护腿α', '042_0010': '爆鳞龙护腿β', '042_0500': '精英矜持护腿α',
               '042_0510': '精英矜持护腿β', '043_0000': '大马士革护腿α', '043_0010': '大马士革护腿β',
               '044_0000': '杜宾护腿α', '045_0000': '冥灯幽火靴α', '045_0010': '冥灯幽火靴β', '045_0020': '冥灯幽火靴γ',
               '046_0000': '帝王护腿α', '046_0001': '精英帝王护腿α', '046_0010': '帝王护腿β',
               '046_0011': '精英帝王护腿β', '046_0020': '帝王护腿γ', '047_0000': '钢龙踏实α',
               '047_0001': '精英钢龙踏实α', '047_0010': '钢龙踏实β', '047_0011': '精英钢龙踏实β',
               '047_0020': '钢龙踏实γ', '048_0000': '公会十字靴α', '049_0000': '绚辉龙铠罗护腿α',
               '049_0001': '精英绚辉龙铠罗护腿α', '049_0010': '绚辉龙铠罗护腿β', '049_0011': '精英绚辉龙铠罗护腿β',
               '049_0020': '绚辉龙铠罗护腿γ', '050_0000': '残虐护腿α', '050_0010': '残虐护腿β',
               '050_0500': '精英贪欲护腿α', '050_0510': '精英贪欲护腿β', '051_0000': '皇后护腿α',
               '051_0001': '精英皇后护腿α', '051_0010': '皇后护腿β', '051_0011': '精英皇后护腿β',
               '051_0020': '皇后护腿γ', '052_0000': '精英煌黑龙细鳞α', '052_0010': '精英煌黑龙细鳞β',
               '053_0000': '追踪者长裤α', '057_0000': '燕尾蝶男脚', '057_0010': '燕尾蝶男脚β',
               '066_0000': '黎明武士寂脚部', '066_0010': '黎明武士誉脚部', '067_0000': '铠武者脚部',
               '069_0000': '隆护腿', '070_0000': '樱护腿α', '071_0000': '但丁皮裤靴α', '072_0000': '苍星之将腿甲α',
               '072_0001': '苍世武士服装脚部', '073_0000': '腾龙护腿α', '074_0000': '盛开靴', '075_0000': '潜水员靴',
               '076_0000': '收获护腿', '077_0000': '猎户星靴', '078_0000': '盛装靴', '080_0000': '精英迅龙护腿α',
               '080_0010': '精英迅龙护腿β', '081_0000': '精英斩龙护腿α', '081_0010': '精英斩龙护腿β',
               '081_0100': '精英斩黄护腿α', '081_0110': '精英斩黄护腿β', '082_0000': '精英碎龙护腿α',
               '082_0010': '精英碎龙护腿β', '082_0500': '精英铁腕护腿α', '082_0510': '精英铁腕护腿β',
               '083_0000': '精英轰龙护腿α', '083_0010': '精英轰龙护腿β', '083_0100': '精英轰吼护腿α',
               '083_0110': '精英轰吼护腿β', '084_0000': '精英猛牛龙护腿α', '084_0010': '精英猛牛龙护腿β',
               '085_0000': '精英雪崩护腿α', '085_0010': '精英雪崩护腿β', '085_0020': '精英雪崩护腿γ',
               '086_0000': '精英触角护腿α', '086_0010': '精英触角护腿β', '086_0020': '精英触角护腿γ',
               '087_0000': '精英龙纹刻印封靴α', '087_0010': '精英龙纹刻印封靴β', '088_0000': '精英迦楼罗护腿α',
               '088_0010': '精英迦楼罗护腿β', '089_0000': '精英冰牙龙护腿α', '089_0010': '精英冰牙龙护腿β',
               '089_0500': '精英霜刃冰牙龙护腿α', '089_0510': '精英霜刃冰牙龙护腿β', '091_0000': '机械服装脚部',
               '092_0000': '精英公会成果靴α', '093_0000': '黑带服装脚部', '094_0000': '公会宫殿服装脚部',
               '104_0000': '精英弧锁护腿α', '105_0000': '冰狼服装脚部', '106_0000': '浴场服装脚',
               '107_0000': '精英雷狼龙护腿α', '107_0010': '精英雷狼龙护腿β', '107_0100': '精英狱狼龙护腿α',
               '107_0110': '精英狱狼龙护腿β', '108_0000': '精英黑狼鸟护腿α', '108_0010': '精英黑狼鸟护腿β',
               '109_0000': '精英金色下裳α', '109_0010': '精英金色下裳β', '109_0500': '精英齐天腿甲α',
               '109_0510': '精英齐天腿甲β', '110_0000': '精英冰鱼龙护腿α', '115_0000': '精英健美护腿α',
               '115_0001': '健美γ服装脚部', '116_0000': '甲虫服装脚部', '117_0000': '蝴蝶服装脚部',
               '118_0000': '杰洛特护腿α', '119_0000': '希里护腿α', '120_0000': '巴耶克服装脚部',
               '121_0000': '守护者靴α', '122_0000': '结云服装脚部', '123_0000': '银骑士服装脚部',
               '124_0000': '精英蔷薇靴α', '125_0000': '精英热情靴α', '126_0000': '魔界之主服装脚部',
               '127_0000': '精英风火轮靴α', '128_0000': '精英阿斯特拉裤α', '129_0000': '精英龙靴α',
               '129_0010': '精英龙靴β', '130_0000': '里昂服装脚部', '131_0000': '克莱尔服装脚部',
               '132_0010': '精英阿尔忒弥斯脚部α', '133_0000': '狩猎女神服装脚部', '500_0000': '内衣α服装脚部',
               '501_0000': '内衣β服装脚部'}]

PL_MAPPING = {'001_0000': '皮制', '002_0000': '猎人', '002_0010': '猎人β', '003_0000': '骨制', '004_0000': '合金',
              '007_0000': '巨蜂', '007_0001': '精英巨蜂', '008_0000': '贼龙', '008_0001': '精英贼龙',
              '009_0000': '搔鸟', '009_0001': '精英搔鸟', '010_0000': '毒妖鸟', '010_0001': '精英毒妖鸟',
              '010_0010': '毒妖鸟β', '010_0101': '精英妖水', '011_0000': '泥鱼龙', '011_0001': '精英泥鱼龙',
              '012_0000': '土砂龙', '012_0001': '精英土砂龙', '013_0000': '飞雷龙', '013_0001': '精英飞雷龙',
              '013_0101': '精英朱毒', '014_0000': '锁甲', '015_0000': '突击龙', '017_0000': '巨甲',
              '017_0001': '精英巨甲虫', '018_0000': '原型', '019_0000': '独角仙|燕尾蝶', '020_0000': '蛮颚龙',
              '020_0001': '精英蛮颚龙α', '020_0010': '蛮颚龙β', '020_0011': '精英蛮颚龙β', '020_0101': '精英雷颚α',
              '020_0111': '精英雷颚β', '021_0000': '雌火龙', '021_0001': '精英雌火龙α', '021_0010': '雌火龙β',
              '021_0011': '精英雌火龙β', '021_0100': '火龙心α', '021_0101': '精英火龙心α', '021_0110': '火龙心β',
              '021_0111': '精英火龙心β', '021_0200': '精英金黄澄月α', '021_0210': '精英金黄澄月β', '022_0000': '痹贼龙',
              '022_0001': '精英痹贼龙', '023_0000': '眩鸟', '023_0001': '精英眩鸟', '024_0000': '浮空龙',
              '024_0001': '精英浮空龙', '024_0101': '精英浮梦', '025_0000': '矿石', '026_0000': '死神',
              '027_0000': '风漂龙', '027_0001': '精英风漂龙α', '027_0010': '风漂龙β', '027_0011': '精英风漂龙β',
              '027_0500': '精英霜漂α', '027_0510': '精英霜漂β', '028_0000': '骨锤龙', '028_0001': '精英骨锤龙',
              '028_0010': '骨锤龙β', '029_0000': '惨爪龙', '029_0001': '精英惨爪α', '029_0010': '惨爪龙β',
              '029_0011': '精英惨爪β', '029_0101': '精英亡爪α', '029_0111': '精英亡爪β', '030_0000': '战纹α',
              '030_0010': '战纹β', '030_0020': '战纹γ', '030_0500': '精英狂纹α', '030_0510': '精英狂纹β',
              '031_0000': '铸铁', '032_0000': '乌尔德α', '032_0010': '乌尔德β', '032_0020': '乌尔德γ',
              '032_0500': '精英死灭α', '032_0510': '精英死灭β', '033_0000': '火龙', '033_0001': '精英火龙α',
              '033_0010': '火龙β', '033_0011': '精英火龙β', '033_0100': '火龙魂α', '033_0101': '精英火龙魂α',
              '033_0110': '火龙魂β', '033_0111': '精英火龙魂β', '033_0200': '精英银白耀日α',
              '033_0210': '精英银白耀日β', '034_0000': '角龙', '034_0001': '精英角龙α', '034_0010': '角龙β',
              '034_0011': '精英角龙β', '034_0100': '暴君角龙α', '034_0101': '精英暴君角龙α', '034_0110': '暴君角龙β',
              '034_0111': '精英暴君角龙β', '035_0000': '麒麟α|麒麟角', '035_0001': '精英麒麟α', '035_0010': '麒麟β',
              '035_0011': '精英麒麟β', '035_0020': '麒麟γ', '036_0000': '旅团', '037_0000': '爆碎羽饰|羽毛装饰',
              '038_0000': '铸岛熔岩α', '038_0010': '铸岛熔岩β', '038_0020': '铸岛熔岩γ', '039_0000': '岩贼龙',
              '039_0001': '精英岩贼龙', '040_0000': '熔岩龙α', '040_0001': '精英熔岩龙', '040_0010': '熔岩龙β',
              '041_0000': '爆锤龙α', '041_0001': '精英爆锤龙', '041_0010': '爆锤龙β', '042_0000': '爆鳞龙α',
              '042_0010': '爆鳞龙β', '042_0500': '精英矜持α', '042_0510': '精英矜持β', '043_0000': '大马士革α',
              '043_0010': '大马士革β', '044_0000': '杜宾β|杜宾α', '045_0000': '冥灯幽火α', '045_0010': '冥灯幽火β',
              '045_0020': '冥灯幽火γ', '046_0000': '帝王α', '046_0001': '精英帝王α', '046_0010': '帝王β',
              '046_0011': '精英帝王β', '046_0020': '帝王γ', '047_0000': '钢龙α', '047_0001': '精英钢龙α',
              '047_0010': '钢龙β', '047_0011': '精英钢龙β', '047_0020': '钢龙γ', '048_0000': '公会十字',
              '049_0000': '绚辉龙铠罗α', '049_0001': '精英绚辉龙铠罗α', '049_0010': '绚辉龙铠罗β',
              '049_0011': '精英绚辉龙铠罗β', '049_0020': '绚辉龙铠罗γ', '050_0000': '残虐α', '050_0010': '残虐β',
              '050_0500': '精英贪欲α', '050_0510': '精英贪欲β', '051_0000': '皇后α', '051_0001': '精英皇后α',
              '051_0010': '皇后β', '051_0011': '精英皇后β', '051_0020': '皇后γ', '052_0000': '精英煌黑龙α',
              '052_0010': '精英煌黑龙β', '053_0000': '追踪者', '054_0000': '骷髅', '055_0000': '艾露猫',
              '056_0000': '蘑菇猪', '057_0000': '燕尾蝶男|独角仙后', '057_0010': '燕尾蝶男β(男)', '058_0000': '猫蜥龙',
              '059_0000': '水晶|封龙α', '060_0000': '知性眼镜', '061_0000': '龙王的独眼', '062_0000': '墨镜',
              '063_0000': '封印的眼罩', '064_0000': '摇曳鳗', '065_0000': '扒手龙', '066_0000': '黎明武士寂',
              '066_0010': '黎明武士誉', '067_0000': '铠武者', '069_0000': '隆', '070_0000': '樱', '071_0000': '但丁',
              '072_0000': '苍星之将', '072_0001': '苍世武士', '073_0000': '腾龙', '074_0000': '盛开',
              '075_0000': '潜水员', '076_0000': '收获', '077_0000': '猎户星', '078_0000': '盛装',
              '080_0000': '精英迅龙α', '080_0010': '精英迅龙β', '081_0000': '精英斩龙α', '081_0010': '精英斩龙β',
              '081_0100': '精英斩黄α', '081_0110': '精英斩黄β', '082_0000': '精英碎龙α', '082_0010': '精英碎龙β',
              '082_0500': '精英铁腕α', '082_0510': '精英铁腕β', '083_0000': '精英轰龙α', '083_0010': '精英轰龙β',
              '083_0100': '精英轰吼α', '083_0110': '精英轰吼β', '084_0000': '精英猛牛龙α', '084_0010': '精英猛牛龙β',
              '085_0000': '精英雪崩α', '085_0010': '精英雪崩β', '085_0020': '精英雪崩γ', '086_0000': '精英触角α',
              '086_0010': '精英触角β', '086_0020': '精英触角γ', '087_0000': '精英龙纹α', '087_0010': '精英龙纹β',
              '088_0000': '精英迦楼罗α', '088_0010': '精英迦楼罗β', '089_0000': '精英冰牙龙α',
              '089_0010': '精英冰牙龙β', '089_0500': '精英霜刃冰牙龙α', '089_0510': '精英霜刃冰牙龙β',
              '091_0000': '机械', '092_0000': '公会成果', '093_0000': '黑带', '094_0000': '公会宫殿',
              '095_0000': '敏捷', '095_0010': '佯动', '096_0000': '精灵鹿', '097_0000': '草食龙', '098_0000': '企鹅',
              '099_0000': '骷髅方巾', '100_0000': '封印的龙骸布', '101_0000': '龙人族之耳',
              '102_0000': '精英冰豺狼围巾α|精英冰豺龙|精英冰豺狼围巾β', '104_0000': '蒸汽贵族α|精英弧锁α',
              '104_0010': '精英弧锁β|蒸汽贵族β', '105_0000': '冰狼', '106_0000': '浴场', '107_0000': '精英雷狼龙α',
              '107_0010': '精英雷狼龙β', '107_0100': '精英狱狼龙α', '107_0110': '精英狱狼龙β',
              '108_0000': '精英黑狼鸟α', '108_0010': '精英黑狼鸟β', '109_0000': '精英金色α', '109_0010': '精英金色β',
              '109_0500': '精英齐天α', '109_0510': '精英齐天β', '110_0000': '精英冰鱼龙', '111_0000': '兔耳朵',
              '112_0000': '柔毛秧鸡', '113_0000': '温泉银猴', '113_0001': '温泉金猴', '114_0000': '飞雷龙围巾',
              '116_0000': '甲虫', '117_0000': '蝴蝶', '118_0000': '杰洛特', '119_0000': '希里', '120_0000': '巴耶克',
              '121_0000': '防卫队α|守护者', '122_0000': '结云', '123_0000': '银骑士', '124_0000': '蔷薇',
              '125_0000': '热情', '126_0000': '魔界之主', '127_0000': '风火轮', '128_0000': '阿斯特拉',
              '129_0000': '精英龙α', '129_0010': '精英龙β', '130_0000': '里昂', '131_0000': '克莱尔',
              '132_0010': '精英阿尔忒弥斯α ', '133_0000': '狩猎女神|精英阿尔忒弥斯α'}
