View0
create materialized view View0 as select c.nation as c_nation , c.region as c_region , d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , p.mfgr as p_mfgr , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue - lo.supplycost) as profit   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey group by c.nation,c.region,d.year,p.brand1,p.category,p.mfgr,s.city,s.nation,s.region
====
View1
create materialized view View11 as select d.weeknuminyear as d_weeknuminyear , d.year as d_year , d.yearmonthnum as d_yearmonthnum , lo.discount as lo_discount , lo.quantity as lo_quantity , sum(lo.extendedprice * lo.discount) as revenue   from lineorder lo  join date_dim d on lo.orderdate = d.datekey group by d.weeknuminyear,d.year,d.yearmonthnum,lo.discount,lo.quantity
====
View2
create materialized view View2 as select d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , s.nation as s_nation , s.region as s_region , sum(lo.revenue)   from lineorder lo  join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey group by d.year,p.brand1,p.category,s.nation,s.region
====
View3
create materialized view View3 as select c.city as c_city , c.name as c_name , c.nation as c_nation , c.region as c_region , d.year as d_year , d.yearmonth as d_yearmonth , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue) as revenue   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join supplier s on lo.suppkey = s.suppkey group by c.city,c.name,c.nation,c.region,d.year,d.yearmonth,s.city,s.nation,s.region
====
