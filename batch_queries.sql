select
    customer.nation,
    supplier.nation,
    date_dim.year,
    sum(revenue) as revenue
from
    lineorder
    left join date_dim on lineorder.orderdate = date_dim.datekey
    left join customer on lineorder.custkey = customer.custkey
    left join supplier on lineorder.suppkey = supplier.suppkey
where
    customer.region = 'ASIA'
    and supplier.region = 'ASIA'
    and date_dim.year >= 1992
    and date_dim.year <= 1997
group by
    customer.nation,
    supplier.nation,
    date_dim.year
order by
    date_dim.year asc,
    revenue desc;
    
-- QUERY 1.1
select
    sum(lo.extendedprice * lo.discount) as revenue
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
where
    d.year = 1993
    and lo.discount between 1
    and 3
    and lo.quantity < 25;
    
    
--QUERY 1.2
select
    sum(lo.extendedprice * lo.discount) as revenue
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
where
    d.yearmonthnum = 199401
    and lo.discount between 4
    and 6
    and lo.quantity between 26
    and 35;

--QUERY 1.3
select
    sum(lo.extendedprice * lo.discount) as revenue
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
where
    d.weeknuminyear = 6
    and d.year = 1994
    and lo.discount between 5
    and 7
    and lo.quantity between 26
    and 35;
    
--QUERY 2.1
select
    sum(lo.revenue),
    d.year,
    p.brand1
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
    join part p on lo.partkey = p.partkey
    join supplier s on lo.suppkey = s.suppkey
where
    p.category = 'MFGR#12'
    and s.region = 'AMERICA'
group by
    d.year,
    p.brand1
order by
    d.year,
    p.brand1;
    
--QUERY 2.2
select
    sum(lo.revenue),
    d.year,
    p.brand1
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
    join part p on lo.partkey = p.partkey
    join supplier s on lo.suppkey = s.suppkey
where
    p.brand1 between 'MFGR#2221'
    and 'MFGR#2228'
    and s.region = 'ASIA'
group by
    d.year,
    p.brand1
order by
    d.year,
    p.brand1;
    
--QUERY 2.3
select
    sum(lo.revenue),
    d.year,
    p.brand1
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
    join part p on lo.partkey = p.partkey
    join supplier s on lo.suppkey = s.suppkey
where
    p.brand1 = 'MFGR#2221'
    and s.region = 'EUROPE'
group by
    d.year,
    p.brand1
order by
    d.year,
    p.brand1;
    
--QUERY 3.1
select
    c.nation,
    s.nation,
    d.year,
    sum(lo.revenue) as revenue
from
    lineorder lo
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join date_dim d on lo.orderdate = d.datekey
where
    c.region = 'ASIA'
    and s.region = 'ASIA'
    and d.year >= 1992
    and d.year <= 1997
group by
    c.nation,
    s.nation,
    d.year
order by
    d.year asc,
    revenue desc;
    
--QUERY 3.2
select
    c.city,
    s.city,
    d.year,
    sum(lo.revenue) as revenue
from
    lineorder lo
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join date_dim d on lo.orderdate = d.datekey
where
    c.nation = 'UNITED STATES'
    and s.nation = 'UNITED STATES'
    and d.year >= 1992
    and d.year <= 1997
group by
    c.city,
    s.city,
    d.year
order by
    d.year asc,
    revenue desc;


--QUERY 3.3
select
    c.city,
    s.city,
    d.year,
    sum(lo.revenue) as revenue
from
    lineorder lo
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join date_dim d on lo.orderdate = d.datekey
where
    (
        c.city = 'UNITED KI1'
        or c.city = 'UNITED KI5'
    )
    and (
        s.city = 'UNITED KI1'
        or s.city = 'UNITED KI5'
    )
    and d.year >= 1992
    and d.year <= 1997
group by
    c.city,
    s.city,
    d.year
order by
    d.year asc,
    revenue desc;
    
--QUERY 3.4
select
    c.city,
    s.city,
    d.year,
    sum(lo.revenue) as revenue
from
    lineorder lo
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join date_dim d on lo.orderdate = d.datekey
where
    (
        c.city = 'UNITED KI1'
        or c.city = 'UNITED KI5'
    )
    and (
        s.city = 'UNITED KI1'
        or s.city = 'UNITED KI5'
    )
    and d.yearmonth = 'Dec1997'
group by
    c.city,
    s.city,
    d.year
order by
    d.year asc,
    revenue desc;
    
    
--QUERY 4.1
select
    d.year,
    c.nation,
    sum(lo.revenue - lo.supplycost) as profit
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join part p on lo.partkey = p.partkey
where
    c.region = 'AMERICA'
    and s.region = 'AMERICA'
    and (
        p.mfgr = 'MFGR#1'
        or p.mfgr = 'MFGR#2'
    )
group by
    d.year,
    c.nation
order by
    d.year,
    c.nation;
    
--QUERY 4.2
select
    d.year,
    s.nation,
    p.category,
    sum(lo.revenue - lo.supplycost) as profit
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join part p on lo.partkey = p.partkey
where
    c.region = 'AMERICA'
    and s.region = 'AMERICA'
    and (
        d.year = 1997
        or d.year = 1998
    )
    and (
        p.mfgr = 'MFGR#1'
        or p.mfgr = 'MFGR#2'
    )
group by
    d.year,
    s.nation,
    p.category
order by
    d.year,
    s.nation,
    p.category;
    
    
--QUERY 4.3
select
    d.year,
    s.city,
    p.brand1,
    sum(lo.revenue - lo.supplycost) as profit
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
    join customer c on lo.custkey = c.custkey
    join supplier s on lo.suppkey = s.suppkey
    join part p on lo.partkey = p.partkey
where
    c.region = 'AMERICA'
    and s.nation = 'UNITED STATES'
    and (
        d.year = 1997
        or d.year = 1998
    )
    and p.category = 'MFGR#14'
group by
    d.year,
    s.city,
    p.brand1
order by
    d.year,
    s.city,
    p.brand1;

