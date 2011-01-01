"""Random helpful functions for mevemon """
 
def comma(number):
    """Converts a number in the format 1234567 to 1,234,567
    """
    num_string = '%0.2f' % number
    
    #a,b = num_string.split('.')
    decimal_part, fractional_part = num_string.split('.')
    thousands = []
    while len(decimal_part) > 3:
        thousands.insert(0, decimal_part[-3:])
        decimal_part = decimal_part[0:-3]
    if decimal_part:
        thousands.insert(0, decimal_part)

    if type(number) is int:
        return ','.join(thousands)
    else:
        return ','.join(thousands) + '.' + fractional_part

