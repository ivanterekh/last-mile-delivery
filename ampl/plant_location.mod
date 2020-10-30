param N;
param M;

set FACILITIES = {1..N};#identification n facilities
set CUSTOMERS = {1..M};#identification m customers

param capacity {FACILITIES}>=0;       #supply capacity bjof facilities
param demand {CUSTOMERS}>=0;#customers’ demands dj
param distance{FACILITIES, CUSTOMERS}>=0;    #cost cijof supplying customer ifrom facility j
param fixcost{FACILITIES}>=0;#cost of opening facility j
param routing_cost; # cost per hour of driving

var y {CUSTOMERS,FACILITIES} binary;   #yij=1 customer iallocated to facility j
var x {j in FACILITIES} binary;#xj = facility j open

minimize Total_Cost:
    sum{i in CUSTOMERS, j in FACILITIES} distance[j,i]*y[i,j]*routing_cost*30/3600+sum{j in FACILITIES} fixcost[j]*x[j];

subject to customer_allocation{i in CUSTOMERS}:
    sum {j in FACILITIES} y[i,j]=1;

subject to capacity_constraint{j in FACILITIES}:
    sum {i in CUSTOMERS} demand[i]*y[i,j]<=capacity[j]*x[j];
