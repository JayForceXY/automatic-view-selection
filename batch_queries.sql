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


select
    sum(lo.revenue - lo.supplycost) as profit,
    d.year
from
    lineorder lo
    join date_dim d on lo.orderdate = d.datekey
where
    d.yearmonthnum = 199401
    and lo.discount between 4
    and 6
    and lo.quantity between 26
    and 35;
