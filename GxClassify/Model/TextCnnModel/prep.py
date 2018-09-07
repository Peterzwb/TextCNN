
import re

patten = re.compile(r'\d+')
patten1 = re.compile(r'错误编码[【]\d{6}[】]')
patten2 = re.compile(r'[0-9.-]+[万元|元]')


def pre(s):
    if s == None:
        s=''
    s = s.strip('\n')
    s = s.strip()

    s = s.replace('_',',')


    result = patten.findall(s)
    res = [r for r in result if len(r) == 11]
    for r in res:
        s = s.replace(r, 'TEL')
    res = [r for r in result if len(r) == 18 and r.startswith('3')]
    for r in res:
        s = s.replace(r, 'CAD')
    res = patten1.findall(s)
    for r in res:
        s = s.replace(r, '错误编码ERR')
    res = patten2.findall(s)
    for r in res:
        s = s.replace(r, 'MOY')

    result = patten.findall(s)
    for r in result:
        if len(r)>1:
            s = s.replace(r,'')

    s = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", ",", s)
    s = s.lower()
    return s
