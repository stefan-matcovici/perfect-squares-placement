/*********************************************
 * OPL 12.9.0.0 Model
 * Author: smatcovici
 * Creation Date: Oct 14, 2019 at 3:21:06 PM
 *********************************************/
int NoSquares = ...;
int MasterSquareSize = ...;
int SquareSizes[1..NoSquares] = ...;
dvar float X[1..NoSquares];
dvar float Y[1..NoSquares];
int n;
int m;

minimize 0;

//  sum ( i in 1..NoSquares)
//    (X[i] + SquareSizes[i]) * (Y[i] + SquareSizes[i]);

subject to {

	forall ( i in 1..NoSquares-1) {
	  X[i] >= 0;
	  Y[i] >= 0;
	  X[i] <= MasterSquareSize;
	  Y[i] <= MasterSquareSize;
 	}
 	
// 	forall (i,j in 1..NoSquares-1: i>j) {
// 		max() 	
// 	 	
// 	}

	forall ( i in 1..NoSquares-1) {
		forall (j in i+1..NoSquares) {
//		    X[i] >= X[j] + SquareSizes[j] || X[i] + SquareSizes[i] <= X[j] || Y[i] + SquareSizes[i] >= Y[j] || Y[i] <= Y[j] + SquareSizes[j];
	   		 maxl(X[i], X[j]) - minl(X[i]+SquareSizes[i], X[j]+SquareSizes[j]) >= 0 || maxl(Y[i], Y[j]) - minl(Y[i]+SquareSizes[i], Y[j]+SquareSizes[j]) >=0 ;

	   }	
	 }       	 
 }