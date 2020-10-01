load data local inpath '/home/ahmed/ssb-generator-/tables_sf1/customer.tbl' into table customer;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf1/part.tbl' into table part;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf1/lineorder.tbl' into table lineorder;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf1/supplier.tbl' into table supplier;


load data local inpath '/home/ahmed/ssb-generator-/tables_sf5/customer.tbl' into table customer;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf5/part.tbl' into table part;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf5/date.tbl' into table date_dim;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf5/lineorder.tbl' into table lineorder;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf5/supplier.tbl' into table supplier;



load data local inpath '/home/ahmed/ssb-generator-/tables_sf20/customer.tbl' into table customer;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf20/part.tbl' into table part;

load data local inpath '/home/ahmed/ssb-generator-/tables_sf20/lineorder.tbl' into table lineorder;
load data local inpath '/home/ahmed/ssb-generator-/tables_sf20/supplier.tbl' into table supplier;


load data local inpath '/home/ahmed/StarSchemaBenchmark/date_dim.csv' into table date_dim; 