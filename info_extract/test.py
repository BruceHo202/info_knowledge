from stanfordcorenlp import StanfordCoreNLP
import settings
import os
import re
text_dir = 'C:\\Users\\mac\\allSourceText'
FIRE = 0
EAR_Q = 1
TRAFF = 2
TERRO = 3
FOOD = 4

def pattern_match(patterns, text):
    ''' 匹配给定模板，返回匹配列表
    '''
    result = []

    for pattern in patterns:
        match_list = re.findall(pattern, text)
        if match_list:
            result.append(match_list[0])
    return result


def pattern_cause(type):
    ''' 事故原因提取模板
    '''
    if type == FIRE:
        patterns = []
        key_words = ['起火', '事故', '火灾','爆炸','目前']
        pattern = re.compile('.*?(?:{0})原因(.*?)[,.?:;!，。？：；！]'.format('|'.join(key_words)))
        patterns.append(pattern)
        patterns.append(re.compile(r'(\d+事故因)'))
        patterns.append(re.compile(r'由于.*引发'))

        return patterns
    if type == EAR_Q:
        patterns = []
        pattern = re.compile('[一二三四五六七八九十].[一二三四五六七八九十]级|\\d\\.\\d级')
        patterns.append(pattern)
        return patterns
    if type == TRAFF:
        patterns = []
        pattern = re.compile('(?<=[。，])(?:.*)撞上(?:.*)(?=[。，])')
        patterns.append(pattern)
        pattern = re.compile('(?<=[。，])(?:.*)(?:.*)相[撞碰]')
        patterns.append(pattern)
        return patterns
    if type == TERRO:
        patterns = []
        pattern = re.compile('(?<=[。，])(?:.*)恐怖(?:.*)(?=[。，])')
        patterns.append(pattern)
        pattern = re.compile('(?<=[。，])(?:.*)袭击(?:.*)(?=[。，])')
        patterns.append(pattern)
        pattern = re.compile('(?<=[。，])(?:.*)发生(?:.*)爆炸(?:.*)(?=[。，])')
        patterns.append(pattern)
        return patterns
    if type == FOOD:
        patterns = []
        pattern = re.compile('(?<=[。，])(?:.*)[(食物中毒)(呕吐)](?:.*)(?=[。，])')
        patterns.append(pattern)
        return patterns

def pattern_lose():
    ''' 定义损失模板
    '''
    patterns = []

    key_words = ['伤亡', '损失']
    pattern = re.compile('.*?(未造成.*?(?:{0}))[,.?:;!，。？：；]'.format('|'.join(key_words)))
    patterns.append(pattern)

    patterns.append(re.compile(r'(\d+(?:\w+)死亡)'))
    patterns.append(re.compile(r'(\d+(?:\w+)身亡)'))
    patterns.append(re.compile(r'(\d+(?:\w+)受伤)'))
    patterns.append(re.compile(r'(\d+(?:\w+)烧伤)'))
    patterns.append(re.compile(r'(\d+(?:\w+)坠楼身亡)'))
    patterns.append(re.compile(r'(\d+(?:\w+)遇难)'))
    patterns.append(re.compile(r'(\d+(?:\w+)被灼伤)'))
    patterns.append(re.compile(r'(\d+死)'))
    patterns.append(re.compile(r'(\d+伤)'))
    patterns.append(re.compile(r'\d+(?:\w*)住院'))
    # patterns = ",".join(str(i) for i in patterns)
    # print(pattern)
    return patterns

class StanfordNER():
    ''' 调用stanfordnlp工具做ner
    '''
    def __init__(self, text):
        # 创建stanfordnlp工具，做ner
        nlp = StanfordCoreNLP('C:\\Users\\mac\\stanford-corenlp-4.2.2',lang="zh")
        self.ner_result = nlp.ner(text)
        nlp.close()#运行结束关闭模型否则占用大量内存


class EventExtraction():
    ''' 事件提取类
    '''
    def __init__(self, context, nlp):
        # 初始化事件字典，包含触发词，事件类型
        # 时间，地点，救援组织，事故原因，事故损失
        self.nlp_result = nlp.ner_result
        self.news = context
        self.event = {}

        self.having_event()
        """ 识别触发词 """
        if self.event['trigger'] in settings.FIRE_TRIGGER:
            self.fire_event()
        elif self.event['trigger'] in settings.EAR_QUAKE_TRIGGER:
            self.ear_q_event()
        elif self.event['trigger'] in settings.TRAFF_TRIGGER:
            self.traff_event()
        elif self.event['trigger'] in settings.TERRO_TRIGGER:
            self.terro_event()
        elif self.event['trigger'] in settings.FOOD_TRIGGER:
            self.food_event()
        
        
        print('event: ', self.event['events'])
        print('time: ', self.event['time'])
        print('location: ', self.event['location'])
        print('related organisation: ', self.event['rescue_org'])
        print('event: ', self.event['events'])
        print('short descrip(cause or level): ', self.event['cause'])
        print('loss: ', self.event['loss'])
        return
        
    def fire_event(self):
        ''' 火灾事件
        '''
        # 提取时间、地点、救援组织
        self.event['time'] = self.taking_time()[-1]
        self.event['location'] = self.taking_location()
        self.event['rescue_org'] = self.taking_organization()
        # 匹配事故原因和事故损失
        self.cause = pattern_match(pattern_cause(FIRE), self.news)
        if len(self.cause) == 0:
            self.cause = "正在进一步调查"
        else:
            self.cause = ",".join(str(i) for i in self.cause)
        
        self.lose = pattern_match(pattern_lose(), self.news)
        if len(self.lose) == 0:
            self.lose = "未知"
        else:
            self.lose = ",".join(str(i) for i in self.lose)
        self.event['cause'] = self.cause
        self.event['loss'] = self.lose
    def ear_q_event(self):
       
        # 提取时间、地点、救援组织
        self.event['time'] = self.taking_time()[-1]
        self.event['location'] = self.taking_location()
        self.event['rescue_org'] = self.taking_organization()
        # 匹配事故原因和事故损失
        self.cause = pattern_match(pattern_cause(EAR_Q), self.news)
        if len(self.cause) == 0:
            self.cause = "未知"
        else:
            self.cause = ",".join(str(i) for i in self.cause)
        
        self.lose = pattern_match(pattern_lose(), self.news)
        if len(self.lose) == 0:
            self.lose = "未知"
        else:
            self.lose = ",".join(str(i) for i in self.lose)
        self.event['cause'] = self.cause
        self.event['loss'] = self.lose

    def traff_event(self):
        self.event['time'] = self.taking_time()[-1]
        self.event['location'] = self.taking_location()
        self.event['rescue_org'] = self.taking_organization()
        self.cause = pattern_match(pattern_cause(TRAFF), self.news)
        if len(self.cause) == 0:
            self.cause = "未知"
        else:
            self.cause = ",".join(str(i) for i in self.cause)
        
        self.lose = pattern_match(pattern_lose(), self.news)
        if len(self.lose) == 0:
            self.lose = "未知"
        else:
            self.lose = ",".join(str(i) for i in self.lose)
        self.event['cause'] = self.cause
        self.event['loss'] = self.lose
    def terro_event(self):
        self.event['time'] = self.taking_time()[-1]
        self.event['location'] = self.taking_location()
        self.event['rescue_org'] = self.taking_organization()
        self.cause = pattern_match(pattern_cause(TERRO), self.news)
        if len(self.cause) == 0:
            self.cause = "未知"
        else:
            self.cause = ",".join(str(i) for i in self.cause)
        
        self.lose = pattern_match(pattern_lose(), self.news)
        if len(self.lose) == 0:
            self.lose = "未知"
        else:
            self.lose = ",".join(str(i) for i in self.lose)
        self.event['cause'] = self.cause
        self.event['loss'] = self.lose
    def food_event(self):
        self.event['time'] = self.taking_time()[-1]
        self.event['location'] = self.taking_location()
        self.event['rescue_org'] = self.taking_organization()
        self.cause = pattern_match(pattern_cause(FOOD), self.news)
        if len(self.cause) == 0:
            self.cause = "未知"
        else:
            self.cause = ",".join(str(i) for i in self.cause)
        
        self.lose = pattern_match(pattern_lose(), self.news)
        if len(self.lose) == 0:
            self.lose = "未知"
        else:
            self.lose = ",".join(str(i) for i in self.lose)
        self.event['cause'] = self.cause
        self.event['loss'] = self.lose
    def having_event(self):
        ''' 获取事件
        '''
        fire_trigger_list = ['森林', '爆燃', '火灾', '起火', '泄漏']
        quake_trigger_list = ['地震', '震感', '摇晃']
        traff_trigger_list = ['车', '中巴', '水泥罐车', '辆', '相撞', '撞上', '开车', '交通事故']
        terro_trigger_list = ['恐怖', '武装', '炸弹', '自杀', '爆炸']
        food_trigger_list= ['中毒', '食物', '呕吐', '恶心']
        cnt = dict()
        cnt['fire'] = 0
        cnt['qua'] = 0
        cnt['traf'] = 0
        cnt['terro'] = 0
        cnt['food'] = 0
        fire_set = dict()
        quake_set = dict()
        traff_set = dict()
        terro_set = dict()
        food_set = dict()
        for item in self.nlp_result:
            if item[0] in fire_trigger_list:
                cnt['fire'] += 1
                if item[0] not in fire_set:
                    fire_set[item[0]] = 1
                else:
                    fire_set[item[0]] += 1
            elif item[0] in quake_trigger_list:
                cnt['qua'] += 1
                if item[0] not in quake_set:
                    quake_set[item[0]] = 1
                else:
                    quake_set[item[0]] += 1
            elif item[0] in traff_trigger_list:
                cnt['traf'] += 1
                if item[0] not in traff_set:
                    traff_set[item[0]] = 1
                else:
                    traff_set[item[0]] += 1
            elif item[0] in terro_trigger_list:
                cnt['terro'] += 1
                if item[0] not in terro_set:
                    terro_set[item[0]] = 1
                else:
                    terro_set[item[0]] += 1
            elif item[0] in food_trigger_list:
                cnt['food'] += 1
                if item[0] not in food_set:
                    food_set[item[0]] = 1
                else:
                    food_set[item[0]] += 1
        
        kind = max(cnt, key=cnt.get)
        if kind == 'fire':
            trigger = max(fire_set, key=fire_set.get)
            self.event['trigger'] = trigger
            self.event['events'] = settings.FIRE_TRIGGER[trigger]
            return 
        if kind == 'qua':
            trigger = max(quake_set, key=quake_set.get)
            self.event['trigger'] = trigger
            self.event['events'] = settings.EAR_QUAKE_TRIGGER[trigger]
            return 
        if kind == 'traf':
            trigger = max(traff_set, key=traff_set.get)
            self.event['trigger'] = trigger
            self.event['events'] = settings.TRAFF_TRIGGER[trigger]
            return 
        if kind == 'terro':
            trigger = max(terro_set, key=terro_set.get)
            self.event['trigger'] = trigger
            self.event['events'] = settings.TERRO_TRIGGER[trigger]
            return 
        if kind == 'food':
            trigger = max(food_set, key=food_set.get)
            self.event['trigger'] = trigger
            self.event['events'] = settings.FOOD_TRIGGER[trigger]
            return 
            # if item[0] == '爆炸' or item[0] == '森林' or item[0] == '爆燃' or item[0] == '火灾' or item[0] == '起火' or item[0] == '中毒' or item[0] == '泄漏':
                
            #     if item[0] in settings.FIRE_TRIGGER:
            #         self.event['trigger'] = item[0]
            #         self.event['events'] = settings.FIRE_TRIGGER[item[0]]
            #         return
            # if item[0] == '地震' or item[0] == '震感' or item[0] == '摇晃':
                
            #     if item[0] in settings.EAR_QUAKE_TRIGGER:
            #         self.event['trigger'] = item[0]
            #         self.event['events'] = settings.EAR_QUAKE_TRIGGER[item[0]]
            #         return
            

        # 未发现触发词
        self.event['events'] = None
        self.event['trigger'] = None

    def taking_time(self):
        ''' 获取时间
        '''
        i = 0
        state = False
        time_fire = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in ['DATE', 'TIME']:
                time_fire += self.nlp_result[i][0]
                state = True
            elif self.nlp_result[i][1] in ['NUMBER', 'MISC']:
                time_fire += self.nlp_result[i][0]
            else:
                if state:
                    result.append(time_fire)
                time_fire = ""
                state = False
            i += 1
        if state:
            result.append(time_fire)

        return result


    def taking_location(self):
        ''' 获取地点
        '''
        i = 0
        state = False
        location = ""
        result = []
        while i < len(self.nlp_result):
            if (self.nlp_result[i][1] == 'LOCATION' or
                    self.nlp_result[i][1] == 'FACILITY' or
                    self.nlp_result[i][1] == 'CITY' or
                    self.nlp_result[i][1] == 'GPE'):
                location += self.nlp_result[i][0]
                if not state:
                    state = True
            else:
                if state:
                    result.append(location)
                    location = ""
                    state = False
            i += 1
        if state:
            result.append(location)

        result = list(set(result))
        if len(result) == 0:
            result = "其他"
        else:
            result = ",".join(str(i) for i in result)
        return result


    def taking_organization(self):
        ''' 获取组织
        '''
        i = 0
        state = False
        organization = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in settings.ORG:
                organization += self.nlp_result[i][0]
                if not state:
                    state = True
            else:
                if state:
                    result.append(organization)
                    organization = ""
                    state = False
            i += 1
        if state:
            result.append(organization)

        result = list(set(result))
        if len(result) == 0:
            result = "未知"
        else:
            result = ",".join(str(i) for i in result)
        return result



if __name__ == '__main__':
    result = {}
    file_list = os.listdir(text_dir)
    for file in file_list:
        # file_dir = text_dir + '\\'+ file
        file_dir = text_dir + '\\河南社旗发生交通事故致11人死亡逃逸司机已被控制.txt'
        with open(file_dir, 'r', encoding='utf-8') as f:
            news = f.read()
        f.close
        nlp = StanfordNER(news)
        print(nlp.ner_result)
        # a = 1 / 0
        event = EventExtraction(news, nlp)
        
