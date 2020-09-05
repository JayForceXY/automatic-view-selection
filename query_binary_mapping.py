


def binary_mapping_table(table_attributes,r_attributes):

    table_attributes = table_attributes[::-1]
    bmf=[]
    for attribute in table_attributes:
        bmf.append(int(attribute in r_attributes))
    return bmf


#AT THE END
def which_table_is (attribute):

    s = attribute.split('.')
    table=''

    if s[0] == 'c' :
        table ='customer'

    if s[0] == 'd':
        table = 'date'

    if s[0] == 'p':
        table = 'part'

    if s[0] == 'lo':
        table = 'lineorder'

    if s[0] == 's':
        table = 'supplier'

    return table


