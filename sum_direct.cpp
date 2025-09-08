/************************************************************
 * Name    : Guiran Liu
 * Student : 923620812
 * Course  : CSC 746 High Performance Computing
 * HW#     : Homework 1
 * File    : sum_direct.cpp
 *
 * Description:
 *   Implementation of direct sum (no memory access, compute-only).
 ************************************************************/
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>

#include "sums.h"

void setup(int64_t N, float A[])
{
   printf(" inside direct_sum problem_setup, N=%lld \n", N);
}

float sum(int64_t N, float A[])
{
   // we don't access A this method,so purely compute-only
   printf(" inside direct_sum perform_sum, N=%lld \n", N);
   float sum = 0.0;
   for (int64_t i = 0; i < N; i++)
   {
      sum += i; // just do some computation
   }
   return sum;
}
