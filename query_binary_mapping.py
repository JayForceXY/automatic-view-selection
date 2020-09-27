import sqlparse
import query_mapping
import TPCH_DDL
import re
from scipy.cluster.hierarchy import weighted, fcluster
from scipy.spatial.distance import pdist

def binary_mapping_table(table_attributes,r_attributes,initials):
    table_attributes = table_attributes[::-1]
    bmf=[]
    for attribute in table_attributes:
        attribute = initials+attribute
        bmf.append(int(attribute in r_attributes))
    return bmf
def binary_mapping_joins (table, jn_attributes):
    bm = []
    joins_update = []
    for attribute in jn_attributes :
        joins_update.append(attribute.split(' ')[0])

    return (int(table in joins_update))
def binary_mapping_agg ( agg ):
    aggregations = ['max', 'min', 'avg', 'sum', 'count']
    opertations = []
    operands = []
    binary_mapping_opp_code= []
    binary_mapping_operands = []
    for aggregation in agg :
        opertations.append( aggregation.split('(')[0] )
        operands += re.split(r'([\+,\*,\-,\/])',aggregation.split('(')[1])[0::2]


    operations = list(dict.fromkeys(opertations))
    operands = list(dict.fromkeys(operands))
    operands = [operand.strip() for operand in operands]
    operands = [re.sub(r'\).*','',operand) for operand in operands]
    for aggregation in aggregations:
        binary_mapping_opp_code.append(int(aggregation in opertations))

    binary_mapping_operands= binary_mapping_table ( TPCH_DDL.TPCH_DATABASE['lineorder'], operands, 'lo.' )

    return binary_mapping_opp_code,binary_mapping_operands



def binary_mapping_query (query):
    prj, jnq, rgq = query_mapping.sql_to_la ( query )
    prj,agg = detect_aggregation(prj)
    projection_binary_mapping =[]
    restriction_binary_mapping = []
    join_binary_mapping = []
    binary_mapping_opp_code = []
    binary_mapping_operands = []
    for table in TPCH_DDL.TPCH_DATABASE:

        projection_binary_mapping +=binary_mapping_table ( TPCH_DDL.TPCH_DATABASE[table], prj, which_initals_for(table) )
        restriction_binary_mapping += binary_mapping_table(TPCH_DDL.TPCH_DATABASE[table],rgq,which_initals_for(table))
        join_binary_mapping.append(binary_mapping_joins(table,jnq))
        binary_mapping_opp_code , binary_mapping_operands = binary_mapping_agg(agg)

    d=  binary_mapping_opp_code+binary_mapping_operands+projection_binary_mapping+join_binary_mapping+restriction_binary_mapping
    return d

def which_initals_for ( table ) :
    if table =='customer' :
        initial = 'c.'


    if   table == 'date_dim':
        initial = 'd.'


    if table == 'part':

        initial= 'p.'


    if  table == 'lineorder':
        initial = 'lo.'


    if table == 'supplier':
        initial = 's.'

    return initial
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



def detect_aggregation (prj):
    prj_updated = []
    agg = []
    columns = prj[0].split(',')
    for argument in columns :
        argument=argument.strip()
        if argument.split('(')[0] in ['sum','min','max','avg','count']: agg.append(argument)
        else : prj_updated.append(argument)
    return  prj_updated, agg

def clustering_queries (query_set):
    clustering = []
    for command in query_set :
        prj, jnq, rgq = query_mapping.sql_to_la ( command )
        prj, agg = detect_aggregation ( prj )

        clustering.append ( binary_mapping_query ( command ) )
    y = pdist ( clustering )
    Z = weighted ( y )
    results = fcluster(Z,  2.6 , criterion='distance')
    mapping_similarity = dict()
    i = 0
    for cluster in results:
        if hash ( cluster ) in mapping_similarity :
            mapping_similarity[hash ( cluster )].append ( i )
        else :
            mapping_similarity[hash ( cluster )] = [i]

        i+=1
    return mapping_similarity

def queries_view_mapping( queries ):
    query_set = [query_mapping.sql_to_la(querie) for querie in queries] # Transform every Query into list of prj[] jnq[] rgq[]
    similar_queries = clustering_queries ( queries )  # Hashes Queries and maps similar queries to lists
    similar_queries_indexes = similar_queries.values ( )  # Returns a list ( List (similar queries indexes ) )
    views_and_queries = []
    views = []
    view_name=''
    view_name_view_definition_mapper = dict()
    view_name_view_queries_mapper = dict()
    i = 0

    for  similar_queries_index in similar_queries_indexes :
        view_jnq = []
        view_prq = []
        view_rgq = []
        for q in similar_queries_index:
            tmp_view_prq, tmp_view_jnq,tmp_view_rgq = query_set[q]


            if tmp_view_prq:
                items = tmp_view_prq[0].split(',')
            for item in items:
                # print('item ==', item)
                if item not in view_prq : view_prq.append(item)

            if tmp_view_jnq :
                items = tmp_view_jnq
            for item in items :
                if item not in view_jnq : view_jnq.append ( item )

            if tmp_view_rgq:


                items = tmp_view_rgq

            for item in items :
                if item not in view_rgq : view_rgq.append ( item )

        views.append([view_prq,view_jnq,view_rgq])
        view_name = 'View'+ str(i)
        i+=1
        view_name_view_definition_mapper[view_name] = [view_prq,view_jnq,view_rgq]
        view_name_view_queries_mapper[view_name] = similar_queries_index

    return [view_name_view_definition_mapper,view_name_view_queries_mapper,queries]

