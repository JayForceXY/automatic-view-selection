import sqlparse
import TPCH_DDL

def get_ranges_from_where_statement( wherestatement ) :
    #This function gets the predicate attributes from the where statement
    #The assumption is that operator,attribute and value of predicate are separated with one space


    OPERATORS = ['=', '>', '<', '>=', '<=', 'in', 'not', 'between', 'is null', 'is not null', 'like',
                              'exists', '!=', '<>']
    tmp_str = wherestatement.split ( )  # This is to split any space
    i = 0
    rgq = []
    for stmt in tmp_str :
        # This IF statement is to identify when COMPARAISON OPERTATOR is found, then stores the column before it
        if stmt.lower ( ) in  OPERATORS:
            rgq.append ( tmp_str[i - 1] )
        i += 1

        rgq = list ( dict.fromkeys ( rgq ) )

    return rgq


def sql_to_la( sqlquery ) :
    #sql.parse returns a series of tokens
    parsed = sqlparse.parse ( sqlquery )
    tokenized = parsed[0]
    projection = False
    join = False
    restricton = False
    table_select= False

    prq = [] #projection variables
    tbq = []
    jnq = [] #Join tables
    rgq = [] #Attributes in predicate

    # DEFINING AGGREGATION, JOINS, RANGES AND PROJECTIONS DEPENDING ON TOKEN VALUE

    for token in tokenized.tokens :
        value_of_token = str ( token.value )
        if (not value_of_token.isspace ( )) :

            if projection :
                prq.append ( value_of_token )
                projection = False
            if join :
                jnq.append ( value_of_token )
                join = False
            if restricton :
                rgq.append ( value_of_token )
            # if table_select:
            #     tbq.append(value_of_token)
            #     table_select=False

            if (value_of_token.lower ( ) == 'select') :
                #Whatever comes after select is a projection token
                projection = True
            if (value_of_token.lower ( ) == 'join') :
                # Whatever comes after select is a join token
                join = True
            # if (value_of_token.lower ( ) == 'from') :
            #     # Whatever comes after select is a join token
            #     table_select = True


            if (not value_of_token.lower ( ).find ( 'where' )) :
                # the where statement is stored in one string with all of the ranges
                # get_ranges_from_where_statement( wherestatement ) gets ranges from it
                rgq.append ( value_of_token )

    rgq = get_ranges_from_where_statement ( rgq[0] )

    return prq, jnq, rgq



def find_similar_queries (query_set):

    #for every query in the set, hash the value of join tables sorted by alphabetical order
    #Store similar queries in the
    mapping_similarity = dict()
    i=0
    for query in query_set :

        joined_tables = sorted(query[1])

        tables_joined = ''

        for table in joined_tables :
            st = table.split ( )[0]

            tables_joined += st

        if hash ( tables_joined ) in mapping_similarity :
            mapping_similarity[hash ( tables_joined )].append ( i )
        else :
            mapping_similarity[hash ( tables_joined )] = [i]
        i += 1
    return mapping_similarity

def view_definition(queries):
    query_set = [sql_to_la(querie) for querie in queries] # Transform every Query into list of prj[] jnq[] rgq[]
    similar_queries = find_similar_queries(query_set)  # Hashes Queries and maps similar queries to lists
    similar_queries_indexes = similar_queries.values() #Returns a list ( List (similar queries indexes ) )


    views = []

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

    return [query_set,similar_queries,views]

def combine(list1, list2):
    output =[]

    for element in list1:
        output.append(list1)
    for element in list2:
        if element not in output :
            output.append(list2)
    return output



def view_creation (views_definition):

    select_statement = []
    join_statement = []
    SQL=[]
    for view in views_definition:
       join_statement = [item.strip() for item in view[1]]
       select_statement=view[0] + view[2]
       select_statement=[item.strip() for item in select_statement]
       select_statement = list(dict.fromkeys(select_statement)) #Eliminate duplication
       SQL.append ( [sorted(select_statement), sorted(join_statement)] )


    return SQL


def join_key_statement ( join_table):
        tables = join_table.split(',')
        statement =''
        for table in tables:
            table = " ".join(table.split())
            table_name = table.split(' ')[0]

            #THE CONVENTION IS THAT EACH TABLE IS REFERENCED BY ITS FIRST LETTER AS A CONVENTION
            key = TPCH_DDL.TPCH_DATABASE[table_name][0]
            if key.lower() == 'datekey':
                statement += ' join ' + table_name + ' ' + table_name[0] + ' on ' + 'lo.orderdate' +' = ' + table_name[
                    0] + '.' + key
            else :
                statement += ' join ' + table_name + ' ' + table_name[0] + ' on ' + 'lo.' + key + ' = ' + table_name[
                    0] + '.' + key


        return statement

def select_statement (select_def ):
    tmp = ''
    for column in select_def :
        seprator = (' , ', '  ')[column == select_def[-1]]
        if not is_aggregation_op(column):

            tmp+= column + ' as '+ column.replace('.','_')+seprator #Care if last item you need to remove ,
        else:
            tmp+=column+seprator
    return tmp


def is_aggregation_op ( statement ):
    tmp = statement.split('(')
    return( tmp[0].lower() in ['sum','min','max','avg','count'] )



def view_sql_code (view_statements):

    select_arguments = select_statement(view_statements[0])
    join_arguments = ','.join ( view_statements[1] )
    sql_code = 'select ' + select_arguments + ' from lineorder lo '
    groupby_statement = [element for element in view_statements[0] if(not is_aggregation_op(element))]
    groupby_statement = sorted(list(dict.fromkeys(groupby_statement)))
    groupby_statement = ','.join(groupby_statement)

    if join_arguments :
        sql_code+=join_key_statement(join_arguments)
    sql_code+=' group by ' + groupby_statement
    return sql_code
