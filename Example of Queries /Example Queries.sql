select
    sum(lo.revenue) as revenue,
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
    
select
    sum(lo.revenue) as revenue,
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

select
    sum(lo.revenue) as revenue,
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
