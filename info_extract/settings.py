# 组织 地名
ORG = ['ORGANIZATION']
LOC = ['LOCATION', 'FACILITY', 'CITY', 'STATE_OR_PROVINCE', 'GPE']

# 火灾事件
FIRE_TRIGGER = {
    '森林': '森林火灾事故',
    '爆燃': '燃气爆燃事故',
    '火灾': '火灾事故',
    '起火': '火灾事故',
    '泄漏': '燃气泄漏事故',
    '中毒': '燃气中毒事故'
}
FIRE_TIME = ['DATE', 'TIME', 'NUMBER', 'MISC']
FIRE_LOC = ['LOCATION', 'FACILITY', 'STATE_OR_PROVINCE']

#EARTH_QUAKE
EAR_QUAKE_TRIGGER = {
    '地震': '地震事故',
    '摇晃': '地震摇晃',
    '震感': '地震事故'
}

#TRAFFIC
TRAFF_TRIGGER = {
    '车': '交通事故',
    '中巴': '交通事故',
    '水泥罐车': '交通事故',
    '辆': '交通事故',
    '相撞': '交通事故',
    '撞上': '交通事故',
    '开车': '交通事故',
    '交通事故': '交通事故'
}
TERRO_TRIGGER = {
    '恐怖': '恐怖袭击',
    '武装': '恐怖袭击',
    '炸弹': '恐怖袭击-炸弹',
    '自杀': '自杀式恐袭击',
    '爆炸': '恐怖袭击'
}
FOOD_TRIGGER = {
    '中毒': '食物中毒',
    '食物': '食物中毒',
    '呕吐': '食物中毒',
    '恶心': '食物中毒'
}


# 参数相关消息
MSG_NO_PARSE = '入参必要字段为空'
MSG_ERROR_PARSE = '不支持的入参'
MSG_SUCCESS = '调用成功'
CODE_ERROR = 'ERROR'
CODE_SUCCESS = 'OK'
FUNC_LIST = ['ner', 'event', 'graph']


