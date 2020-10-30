set FACILITIES;#identification n facilities
set CUSTOMERS;#identification m customers

param supply {FACILITIES}>=0;       #supply capacity bjof facilities
param demand {CUSTOMERS}>=0;#customers’ demands dj
param supplycost{CUSTOMERS, FACILITIES}>=0;    #cost cijof supplying customer ifrom facility j
param fixcost{FACILITIES}>=0;#cost of opening facility j

var y {CUSTOMERS,FACILITIES} binary;   #yij=1 customer iallocated to facility j
var x {j in FACILITIES} binary;#xj = facility j open

minimize Total_Cost:
    sum{i in CUSTOMERS, j in FACILITIES} supplycost[i,j ]*y[i,j]+sum{j in FACILITIES} fixcost[j]*x[j];

subject to customer_allocation{i in CUSTOMERS}:
    sum {j in FACILITIES} y[i,j ]=1;

subject to capacity_constraint{j in FACILITIES}:
    sum {i in CUSTOMERS} demand[i]*y[i,j]<=supply[j]*x[j];
