View0
create materialized view View0 as select c.nation as c_nation , c.region as c_region , d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , p.mfgr as p_mfgr , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue - lo.supplycost) as profit   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey group by c.nation,c.region,d.year,p.brand1,p.category,p.mfgr,s.city,s.nation,s.region
 == Original Queries  == 
select d.year, s.city, p.brand1, sum(lo.revenue - lo.supplycost) as profit from lineorder lo join date_dim d on lo.orderdate = d.datekey join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join part p on lo.partkey = p.partkey where c.region = 'AMERICA' and s.nation = 'UNITED STATES' and ( d.year = 1997 or d.year = 1998 ) and p.category = 'MFGR#14' group by d.year, s.city, p.brand1 order by d.year, s.city, p.brand1;
select d.year, c.nation, sum(lo.revenue - lo.supplycost) as profit from lineorder lo join date_dim d on lo.orderdate = d.datekey join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join part p on lo.partkey = p.partkey where c.region = 'AMERICA' and s.region = 'AMERICA' and ( p.mfgr = 'MFGR#1' or p.mfgr = 'MFGR#2' ) group by d.year, c.nation order by d.year, c.nation;
select d.year, s.nation, p.category, sum(lo.revenue - lo.supplycost) as profit from lineorder lo join date_dim d on lo.orderdate = d.datekey join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join part p on lo.partkey = p.partkey where c.region = 'AMERICA' and s.region = 'AMERICA' and ( d.year = 1997 or d.year = 1998 ) and ( p.mfgr = 'MFGR#1' or p.mfgr = 'MFGR#2' ) group by d.year, s.nation, p.category order by d.year, s.nation, p.category;
 == Translated Quereis == 
select d_year, s_city, p_brand1, sum( profit from View0 where c_region = 'AMERICA' and s_nation = 'UNITED STATES' and ( d_year = 1997 or d_year = 1998 ) and p_category = 'MFGR#14'  group by  d_year, s_city, p_brand1 order by d_year, s_city, p_brand1
select d_year, c_nation, sum( profit from View0 where c_region = 'AMERICA' and s_region = 'AMERICA' and ( p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2' )  group by  d_year, c_nation order by d_year, c_nation
select d_year, s_nation, p_category, sum( profit from View0 where c_region = 'AMERICA' and s_region = 'AMERICA' and ( d_year = 1997 or d_year = 1998 ) and ( p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2' )  group by  d_year, s_nation, p_category order by d_year, s_nation, p_category

View1
create materialized view View1 as select d.weeknuminyear as d_weeknuminyear , d.year as d_year , d.yearmonthnum as d_yearmonthnum , lo.discount as lo_discount , lo.quantity as lo_quantity , sum(lo.extendedprice * lo.discount) as revenue   from lineorder lo  join date_dim d on lo.orderdate = d.datekey group by d.weeknuminyear,d.year,d.yearmonthnum,lo.discount,lo.quantity
 == Original Queries  == 
select sum(lo.extendedprice * lo.discount) as revenue from lineorder lo join date_dim d on lo.orderdate = d.datekey where d.year = 1993 and lo.discount between 1 and 3 and lo.quantity < 25;
select sum(lo.extendedprice * lo.discount) as revenue from lineorder lo join date_dim d on lo.orderdate = d.datekey where d.weeknuminyear = 6 and d.year = 1994 and lo.discount between 5 and 7 and lo.quantity between 26 and 35;
select sum(lo.extendedprice * lo.discount) as revenue from lineorder lo join date_dim d on lo.orderdate = d.datekey where d.yearmonthnum = 199401 and lo.discount between 4 and 6 and lo.quantity between 26 and 35;
select sum(lo.extendedprice * lo.discount) as revenue from lineorder lo join date_dim d on lo.orderdate = d.datekey where d.year = 1993 and lo.discount between 1 and 3 and lo.quantity < 25;
 == Translated Quereis == 
select sum( revenue from View1 where d_year = 1993 and lo_discount between 1 and 3 and lo_quantity < 25
select sum( revenue from View1 where d_weeknuminyear = 6 and d_year = 1994 and lo_discount between 5 and 7 and lo_quantity between 26 and 35
select sum( revenue from View1 where d_yearmonthnum = 199401 and lo_discount between 4 and 6 and lo_quantity between 26 and 35
select sum( revenue from View1 where d_year = 1993 and lo_discount between 1 and 3 and lo_quantity < 25

View2
create materialized view View2 as select d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , s.nation as s_nation , s.region as s_region , sum(lo.revenue) as revenue   from lineorder lo  join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey group by d.year,p.brand1,p.category,s.nation,s.region
 == Original Queries  == 
select sum(lo.revenue) as revenue, d.year, p.brand1 from lineorder lo join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey where p.category = 'MFGR#12' and s.region = 'AMERICA' group by d.year, p.brand1 order by d.year, p.brand1;
select sum(lo.revenue) as revenue, d.year, p.brand1 from lineorder lo join supplier s on lo.suppkey = s.suppkey join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey  where p.brand1 = 'MFGR#2221' and s.region = 'EUROPE' and s.nation = 'FRANCE' group by d.year, p.brand1 order by d.year, p.brand1;
select sum(lo.revenue) as revenue, d.year, p.brand1 from lineorder lo join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey where p.brand1  =  'MFGR#2221' and s.region = 'EUROPE' group by d.year, p.brand1 order by d.year, p.brand1;
select sum(lo.revenue) as revenue, d.year, p.brand1 from lineorder lo join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey where p.brand1 between 'MFGR#2221' and 'MFGR#2228' and s.region = 'ASIA' group by d.year, p.brand1 order by d.year, p.brand1;
 == Translated Quereis == 
select sum( revenue), d_year, p_brand1 from View2 where p_category = 'MFGR#12' and s_region = 'AMERICA'  group by  d_year, p_brand1 order by d_year, p_brand1
select sum( revenue, d_year, p_brand1 from View2 where p_brand1 = 'MFGR#2221' and s_region = 'EUROPE' and s_nation = 'FRANCE'  group by  d_year, p_brand1 order by d_year, p_brand1
select sum( revenue, d_year, p_brand1 from View2 where p_brand1  =  'MFGR#2221' and s_region = 'EUROPE'  group by  d_year, p_brand1 order by d_year, p_brand1
select sum( revenue, d_year, p_brand1 from View2 where p_brand1 between 'MFGR#2221' and 'MFGR#2228' and s_region = 'ASIA'  group by  d_year, p_brand1 order by d_year, p_brand1

View3
create materialized view View3 as select c.city as c_city , c.name as c_name , c.nation as c_nation , c.region as c_region , d.year as d_year , d.yearmonth as d_yearmonth , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue) as revenue   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join supplier s on lo.suppkey = s.suppkey group by c.city,c.name,c.nation,c.region,d.year,d.yearmonth,s.city,s.nation,s.region
 == Original Queries  == 
select c.nation, s.nation, d.year, sum(lo.revenue) as revenue from lineorder lo join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join date_dim d on lo.orderdate = d.datekey where c.region = 'ASIA' and s.region = 'ASIA' and d.year >= 1992 and d.year <= 1997 group by c.nation, s.nation, d.year order by d.year asc, revenue desc;
select c.city, s.city, d.year, sum(lo.revenue) as revenue from lineorder lo join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join date_dim d on lo.orderdate = d.datekey where c.nation = 'UNITED STATES' and s.nation = 'UNITED STATES' and d.year >= 1992 and d.year <= 1997 group by c.city, s.city, d.year order by d.year asc, revenue desc;
select c.city, s.city, d.year, sum(lo.revenue) as revenue from lineorder lo join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join date_dim d on lo.orderdate = d.datekey where ( c.city = 'UNITED KI1' or c.city = 'UNITED KI5' ) and ( s.city = 'UNITED KI1' or s.city = 'UNITED KI5' ) and d.yearmonth = 'Dec1997' group by c.city, s.city, d.year order by d.year asc, revenue desc;
select c.city,c.name, s.city, d.year, sum(lo.revenue) as revenue from lineorder lo join customer c on lo.custkey = c.custkey join supplier s on lo.suppkey = s.suppkey join date_dim d on lo.orderdate = d.datekey where ( c.city = 'UNITED KI1' or c.city = 'UNITED KI5' ) and ( s.city = 'UNITED KI1' or s.city = 'UNITED KI5' ) and d.year >= 1992 and d.year <= 1997 group by c.city, s.city, d.year order by d.year asc, revenue desc;
 == Translated Quereis == 
select c_nation, s_nation, d_year, sum( revenue from View3 where c_region = 'ASIA' and s_region = 'ASIA' and d_year >= 1992 and d_year <= 1997  group by  c_nation, s_nation, d_year order by d_year asc, revenue desc
select c_city, s_city, d_year, sum( revenue from View3 where c_nation = 'UNITED STATES' and s_nation = 'UNITED STATES' and d_year >= 1992 and d_year <= 1997  group by  c_city, s_city, d_year order by d_year asc, revenue desc
select c_city, s_city, d_year, sum( revenue from View3 where ( c_city = 'UNITED KI1' or c_city = 'UNITED KI5' ) and ( s_city = 'UNITED KI1' or s_city = 'UNITED KI5' ) and d_yearmonth = 'Dec1997'  group by  c_city, s_city, d_year order by d_year asc, revenue desc
select c_city,c_name, s_city, d_year, sum( revenue from View3 where ( c_city = 'UNITED KI1' or c_city = 'UNITED KI5' ) and ( s_city = 'UNITED KI1' or s_city = 'UNITED KI5' ) and d_year >= 1992 and d_year <= 1997  group by  c_city, s_city, d_year order by d_year asc, revenue desc

