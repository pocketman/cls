def striphtmlandnonunicode(data):
    p1 = re.compile(r'<.*?>')
    p2 = re.compile(r'[^\x00-\x7f]')
    data = p1.sub('', data)
    return p2.sub('', data)
