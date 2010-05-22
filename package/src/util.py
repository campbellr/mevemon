#Random helpful functions for mevemon
 
def comma(d):
    """
    Converts a number in the format 1234567 to 1,234,567
    """
    s = '%0.2f' % d
    
    a,b = s.split('.')
    l = []
    while len(a) > 3:
        l.insert(0,a[-3:])
        a = a[0:-3]
    if a:
        l.insert(0,a)

    if type(d) is int:
        return ','.join(l)
    else:
        return ','.join(l)+'.'+b

