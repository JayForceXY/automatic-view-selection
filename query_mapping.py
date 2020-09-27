import sqlparse
import TPCH_DDL
import re
import query_binary_mapping

#This function gets a where statement and extracts the columns used - Internpreter
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

#Translation of JOIN_COMPONENTS into SQL_CODE - Interpreter
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
#Translation of JOIN_COMPONENTS into SQL_CODE  - Interpreter
def select_statement (select_def ):
    tmp = ''
    for column in select_def :
        seprator = (' , ', '  ')[column == select_def[-1]]
        if not is_aggregation_op(column):

            tmp+= column + ' as '+ column.replace('.','_')+seprator #Care if last item you need to remove ,
        else:
            tmp+=column+seprator
    return tmp

#Checks if a statement is has an aggregation operation - Interpreter
def is_aggregation_op ( statement ):
    tmp = statement.split('(')
    return( tmp[0].lower() in ['sum','min','max','avg','count'] )


#This function uses sqlparse to parse sql statement and extract projections, restrictions and joins - Interpreter
def sql_to_la( sqlquery , keep_where_statement = False) :
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

    if not keep_where_statement and rgq:
        rgq = get_ranges_from_where_statement ( rgq[0] )

    return prq, jnq, rgq







#This function gets a query set, hashes queries based on join tables, and returns a dictionary hash -> similar queries index from query set - Clustering
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

#This function takes queries set, find similar queries and creates 2 dictionnaries dict1 maps view_name ->[similar_queries_index] dict2 view_name ->[union of similar queries ] - Clustering
def queries_view_mapping( queries ):
    query_set = [sql_to_la(querie) for querie in queries] # Transform every Query into list of prj[] jnq[] rgq[]
    similar_queries = find_similar_queries(query_set)  # Hashes Queries and maps similar queries to lists
    similar_queries_indexes = similar_queries.values() #Returns a list ( List (similar queries indexes ) )
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


#Creates the COMPONENTS of Select and join Statements for the Materialized view by joining select and join statements of all similar queries - Creation
def view_statements_definition_creation ( view_name_view_definition_mapper ):


    select_statement = []
    join_statement = []
    SQL = []


    for view_name,view_definition in view_name_view_definition_mapper.items():

       join_statement = [item.strip() for item in view_definition[1]]
       select_statement=view_definition[0] + view_definition[2]
       select_statement=[item.strip() for item in select_statement]
       select_statement = list(dict.fromkeys(select_statement)) #Eliminate duplication
       SQL.append ( [sorted(select_statement), sorted(join_statement)] )
       view_name_view_definition_mapper[view_name] = SQL
       select_statement = []
       join_statement = []
       SQL = []

    return view_name_view_definition_mapper


#Create final materialized view_code - Creation
def view_sql_code (view_name_view_definition_mapper,view_name_view_queries_mapper,queries,use_predicate = False ):
    for view_name, view_statements in view_name_view_definition_mapper.items():
        sql_code='create materialized view '+view_name +' as '

        select_arguments = select_statement(view_statements[0][0])
        join_arguments = ','.join ( view_statements[0][1] )
        sql_code += 'select ' + select_arguments + ' from lineorder lo '
        where = ('',' where ')[use_predicate]
        if use_predicate:

            for query in view_name_view_queries_mapper[view_name]:
                z, y, rgq = sql_to_la ( queries[query], keep_where_statement=True )
                for stmt in rgq :
                    or_stmt = (' ', ' or ')[query != view_name_view_queries_mapper[view_name][-1]]
                    stmt = stmt.replace(';', ' '  )
                    where += '(' + stmt.replace ( 'where', '' ) + ')' + or_stmt

        groupby_statement = [element for element in view_statements[0][0] if(not is_aggregation_op(element))]
        groupby_statement = sorted(list(dict.fromkeys(groupby_statement)))
        groupby_statement = ','.join(groupby_statement)

        if join_arguments :
            sql_code+=join_key_statement(join_arguments)
        sql_code+= where+' group by ' + groupby_statement
        view_name_view_definition_mapper[view_name] = sql_code

    return view_name_view_definition_mapper




#Final Function - Takes SQL-Commands, one boolean set to False by default to suggest views with or without predicate
def suggest_materialized_views (commands , view_with_predicat = True) :

     views,view_name_similar_queries_mapper,queries = queries_view_mapping( commands ) #Maps_out view_name -> view_components, View_name -> similar_queries

     view_name_view_definition_mapper = view_statements_definition_creation( views ) #Maps_out view_name -> view_statement_definition
     view_name_view_code = view_sql_code(view_name_view_definition_mapper,view_name_similar_queries_mapper,queries,view_with_predicat) #Returns the SQL code for Materialize view queries


     return view_name_view_code,view_name_similar_queries_mapper,queries


def suggest_materialized_views_clustering_approach( commands, view_with_predicat=True ) :
    views, view_name_similar_queries_mapper, queries = query_binary_mapping.queries_view_mapping(commands) # Maps_out view_name -> view_components, View_name -> similar_queries

    view_name_view_definition_mapper = view_statements_definition_creation ( views )  # Maps_out view_name -> view_statement_definition
    view_name_view_code = view_sql_code ( view_name_view_definition_mapper, view_name_similar_queries_mapper, queries,
                                          view_with_predicat )  # Returns the SQL code for Materialize view queries

    return view_name_view_code, view_name_similar_queries_mapper, queries


# To Add an optional module of query re-writing

def query_rewriting(views_code,views_queries,queries):
    translated_queries_dict = dict()
    for view_name, view_code in views_code.items ( ) :


        # print ( "queries of " + view_name )
        queries_translated_for_view = ''
        for q in views_queries[view_name] :  # Query_rewrtiting_module
            # print(queries[q])
            select, join, where = sql_to_la ( queries[q], True )
            # print(select)
            # print ( '= ORIGINAL QUERY = ' )
            # print ( queries[q] )
            groupby_orderby = ''
            select = ','.join ( select )
            select = select.replace ( '.', '_' )
            where = ','.join ( where )
            if 'group by' in queries[q] :
                groupby_orderby = queries[q].split ( 'group by' )
                # print('1=', groupby_orderby)
                groupby_orderby = groupby_orderby[-1]
                # print ( '2=', groupby_orderby )
                groupby_orderby = groupby_orderby.replace ( '.', '_' )
                # print ( '3=', groupby_orderby )
                groupby_orderby = ' group by ' + groupby_orderby
                # print('4=',groupby_orderby)
            where = where.replace ( '.', '_' )

            select = re.sub ( r"sum.*as", 'sum(', select )

            queries_translated_for_view += 'select ' + select + ' from ' + view_name + ' ' + where + groupby_orderby
            # print(queries_translated_for_view)
        translated_queries_dict[view_name] = queries_translated_for_view
    return views_code,translated_queries_dict,queries
