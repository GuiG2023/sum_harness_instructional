/************************************************************
 * Name    : Guiran Liu
 * Student : 923620812
 * Course  : CSC 746 High Performance Computing
 * HW#     : Homework 1
 * File    : sum_vector.cpp
 *
 * Description:
 *   Implementation of the vector sum method.
 *   Initializes array A with values [0..N-1], then computes
 *   the sum with linear, sequential memory accesses.
 *   Serves as a bandwidth-friendly baseline.
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
   printf(" inside sum_vector problem_setup, N=%lld \n", N);
   for (int64_t i = 0; i < N; i++)
   {
      A[i] = i; // initialize A with values [0..N-1]
   }
}

float sum(int64_t N, float A[])
{
   printf(" inside sum_vector perform_sum, N=%lld \n", N);
   float sum = 0.0;
   for (int64_t i = 0; i < N; i++)
   {
      sum += A[i]; // accumulate A[i] into sum
   }
   return sum;
}
