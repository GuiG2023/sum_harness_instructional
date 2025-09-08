//
// (C) 2022-2023, E. Wes Bethel
// benchmark-* harness for running different versions of the sum study
//    over different problem sizes
//
// usage: no command line arguments
// set problem sizes, block sizes in the code below
/************************************************************
 * Name    : Guiran Liu
 * Student : 923620812
 * Course  : CSC 746 High Performance Computing
 * HW#     : Homework 1
 * File    : benchmark.cpp
 *
 * Description:
 *   This file calls setup() and sum() for different problem sizes
 *   and measures elapsed time for sum().
 ************************************************************/
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>
#include <cstring>

#include "sums.h"

/* The benchmarking program */
int main(int argc, char **argv)
{
   std::cout << std::fixed << std::setprecision(8); // as prof mentioned in class, set more digits to see the small sum result

#define MAX_PROBLEM_SIZE 1 << 28 //  256M
   std::vector<int64_t> problem_sizes{MAX_PROBLEM_SIZE >> 5, MAX_PROBLEM_SIZE >> 4, MAX_PROBLEM_SIZE >> 3, MAX_PROBLEM_SIZE >> 2, MAX_PROBLEM_SIZE >> 1, MAX_PROBLEM_SIZE};

   float *A = (float *)malloc(sizeof(float) * MAX_PROBLEM_SIZE);

   int n_problems = problem_sizes.size();

   const char *exe = std::strrchr(argv[0], '/'); // get the executable name
   exe = exe ? exe + 1 : argv[0];

   printf("method,N,time_sec\n"); // print the header for csv file

   /* For each test size */
   for (int64_t n : problem_sizes)
   {
      float t;
      printf("Working on problem size N=%lld \n", n);

      // invoke user code to set up the problem
      setup(n, &A[0]);

      // insert your timer code here
      auto t0 = std::chrono::high_resolution_clock::now(); // start timer :as prof mentioned in class, we should time only the sum() method,not inculude setup()

      // invoke method to perform the sum
      t = sum(n, &A[0]);

      // insert your end timer code here, and print out elapsed time for this problem size
      auto t1 = std::chrono::high_resolution_clock::now();                       // end timer here
      double elapsed = std::chrono::duration<double>(t1 - t0).count();           // count the elapsed time
      std::cout << " Elapsed time is : " << elapsed << " seconds." << std::endl; // print out the elapsed time
      printf("%s,%lld,%.9f\n", exe, (long long)n, elapsed);                      // print out in csv format
      // printf(" Sum result = %lf \n", t);

   } // end loop over problem sizes
}

// EOF
