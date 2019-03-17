import re  # 正则
from urllib import request

class Spider():

    url = "https://www.panda.tv/cate/lol"
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number"><i class="ricon ricon-eye"></i>([\s\S]*?)</span>'

    # 连接网址  获取内容
    def __fetch_content(self): 
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding="utf-8")
        return htmls

    # 处理内容
    def __analysis(self, htmls):
        root_html =  re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = { 'name': name, 'number': number }
            anchors.append(anchor)
        return anchors
    
    # 数据精炼
    def __refine(self, anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number':anchor['number'][0]
            }
        return map(l, anchors)
    
    # 数据排序
    def __sort(self, anchors):
        anchor = sorted(anchors, key = self.__sort_seed, reverse=True)
        return anchor

    # 上个函数辅助
    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if "万" in anchor['number']:
            number *= 10000
        return number

    # 数据显示
    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank  ' + str(rank + 1)
            + ":" + anchors[rank]['name']
            + "  " + anchors[rank]['number'])

    # 入口函数
    def go(self):
        result = self.__fetch_content()
        anchors = self.__analysis(result)
        res = list(self.__refine(anchors))
        sorts = self.__sort(res)
        self.__show(sorts)

spider = Spider()
spider.go()