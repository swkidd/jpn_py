from lxml import etree

chars = [
    '\u30A2', #a
    '\u30A4', #i
    '\u30A6', #u
    '\u30A8', #e
    '\u30AA', #o
    
    "[\u30AB\u30AC]", #ka ga
    "[\u30AD\u30AE]", #ki gi
    "[\u30AF\u30B0]", #ku gu
    "[\u30B1\u30B2]", #ke ge
    "[\u30B3\u30B4]", #ko go
   
    "[\u30B5\u30B6]", #sa za
    "[\u30B7\u30B8]", #si zi
    "[\u30B9\u30BA]", #su zu
    "[\u30BB\u30BC]", #se ze
    "[\u30BD\u30BE]", #so zo
    
    "[\u30BF\u30C0]", #ta da
    "[\u30C1\u30C2]", #ti di
    "[\u30C4\u30C5]", #tu du
    "[\u30C6\u30C7]", #te de
    "[\u30C8\u30C9]", #to do
    
    '\u30CA', #na
    '\u30CB', #ni
    '\u30CC', #nu
    '\u30CD', #ne
    '\u30CE', #no
    
    "[\u30CF\u30D0\u30D1]", #ha ba pa
    "[\u30D2\u30D3\u30D4]", #hi bi pi
    "[\u30D5\u30D6\u30D7]", #hu bu pu
    "[\u30D8\u30D9\u30DA]", #he be pe
    "[\u30DB\u30DC\u30DD]", #ho bo po
    
    '\u30DE', #ma
    '\u30DF', #mi
    '\u30E0', #mu
    '\u30E1', #me
    '\u30E2', #mo
    
    '\u30E4', #ya
    '\u30E6', #yu
    '\u30E8', #yo
    
    '\u30E9', #ra
    '\u30EA', #ri
    '\u30EB', #ru
    '\u30EC', #re
    '\u30ED', #ro
    
    '\u30EF', #wa
    
    '\u30F3', #n
]

tree = etree.parse('kanjidic2.xml')
root = tree.getroot()
ns = {"re": "http://exslt.org/regular-expressions"}

count = {}
readings = {}
groups = {}
joyo = ".//misc[./grade<=8]"
for char in chars:
    search = f"re:match(text(), '^{char}')"
    onreading = f".//reading[@r_type='ja_on' and {search}]"
    query = f"./character[{joyo} and {onreading}]"
    res = root.xpath(query, namespaces=ns)
    count[char] = len(res)
    kans = [ i for n in [x.xpath(".//literal/text()") for x in res] for i in n ]
    groups[char] = kans
    for e in res:
        keys = e.xpath(f"{onreading}/text()", namespaces=ns)
        value = e.xpath(f"literal/text()")
        for key in keys:
            if key in readings:
                if value[0] not in readings[key]:
                    readings[key] = readings[key] + value
            else:
                readings[key] = value

sortedcount = {k: v for k, v in sorted(count.items(), key=lambda item: item[1])}
sortedreadings = {k: v for k, v in sorted(readings.items(), key=lambda item: len(item[1]))}
sortedgroups = {k: v for k, v in sorted(groups.items(), key=lambda item: len(item[1]))}
for k in sortedgroups:
    print(k, '\t', len(sortedgroups[k]),'\t', ''.join(sortedgroups[k]))
#for k in sortedreadings:
#    print(k, '\t', ''.join(sortedreadings[k]))
#can remove kanji readings that do not show up in a common word (which isnt usually written in kana)