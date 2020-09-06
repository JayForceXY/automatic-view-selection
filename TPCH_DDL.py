LINEORDER_ATTRIBUTES = ['orderkey' ,'linenumber' ,'custkey' ,'partkey' ,'suppkey' ,'orderdate' ,'orderpriority'
                        ,'shippriority' ,'quantity' ,'extendedprice' ,'ordertotalprice' ,'discount' ,'revenue'
                        ,'supplycost' ,'tax' ,'commitdate' ,'shipmode']
CUSTOMER_ATTRIBUTES = [ 'custkey','name','address','city','nation','region','phone','mktsegment' ]
SUPPLIER_ATTRIBUTES = ['suppkey','name','address','city','nation','region','phone']
PART_ATTRIBUTES = ['partkey','name','mfgr','category','brand1','color','type','size','container']
DATE_DIM_ATTRIBUTES = ['datekey','datestandard','date','weeknuminyear','monthnuminyear','year','daynuminmonth','yearmonthnum','yearmonth']
TIME_DIM_ATTRIBUTES = ['timekey','hour','minutes']


TPCH_DATABASE = dict ( lineorder=LINEORDER_ATTRIBUTES,customer=CUSTOMER_ATTRIBUTES,supplier=SUPPLIER_ATTRIBUTES,part=PART_ATTRIBUTES,date=DATE_DIM_ATTRIBUTES,time=TIME_DIM_ATTRIBUTES )

