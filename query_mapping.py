import sqlparse


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
    prq = []
    tbq = []
    jnq = []
    rgq = []
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


