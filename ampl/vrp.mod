param N; #amount of customers
param V; #amount of vehicle

param demand {1..N}>=0; #customers demands
param vehicle_capacity {1..V} >= 0; #vehicle capacity
param cost {i in 0..N, j in 0..N, k in 1..V: i<>j}; #cost of routes

var Use {i in 0..N, j in 0..N, k in 1..V: i<>j} binary; #usage matrix for routes
var Delivery {i in 0..N, j in 0..N, k in 1..V: i<>j} >=0; #k vehicle load from i to j

minimize Total_Cost: #objective function
    sum{i in 0..N, j in 0..N, k in 1..V: i<>j} cost[i,j,k] * Use[i,j,k];

subject to Out {i in 1..N}: #each customer should be visited once
	sum{k in 1..V, j in 0..N: i<>j} Use[i,j,k] = 1;

subject to StartFinish {k in 1..V}: #each vehicle must start and finish from/in satellite
	sum{i in 1..N} Use[0,i,k] = sum {i in 1..N} Use[i,0,k];

subject to Cycle_Continuity_1 {i in 0..N, k in 1..V}: #defining continuity route
	sum {j in 0..N: i<>j} Use[i,j,k] = sum {j in 0..N: i<>j} Use[j,i,k];

subject to End_Delivery{i in 1..N, k in 1..V}: #empty vehicle after last customer on route
	Delivery[i,0,k] = 0;	

subject to Delivery_Continuity {i in 0..N, j in 1..N, k in 1..V: i<>j}: #defining continuity delivery
	Delivery[i,j,k] >= demand[j]*Use[i,j,k];

subject to Total_Delivery{i in 1..N}: #calculation total delivery
	sum {j in 0..N, k in 1..V: i<>j}Delivery[j,i,k] - sum {j in 0..N, k in 1..V: i<>j}Delivery[i,j,k] = demand[i];

subject to Capacity {i in 0..N, j in 0..N, k in 1..V: i<>j}: #vehicle capacity restriction
	Delivery[i,j,k] <= vehicle_capacity[k] * Use[i,j,k];

