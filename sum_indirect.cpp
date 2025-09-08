/************************************************************
 * Name    : Guiran Liu
 * Student : 923620812
 * Course  : CSC 746 High Performance Computing
 * HW#     : Homework 1
 * File    : sum_indirect.cpp
 *
 * Description:
 *   Implementation of the indirect sum method.
 *   Initializes array A with random indices in [0..N-1].
 *   Computes the sum by pointer chasing: k = A[k],
 *   exhibiting random, data-dependent memory accesses.
 *   Designed to stress memory latency.
 *
 * * Note: In the initial implementation of the indirect sum method,
 * I used srand48(12345)/lrand48() to seed and generate random indices.
 * This followed the instructor’s slides (CP#1 Algorithms: "A[i] initialized
 * to random values (OK to use system library calls in setup())").
 * However, due to compatibility issues on macOS/Clang, I later revised
 * the code to use the C++11 <random> library (mt19937 with a fixed seed).
 * GPT helped me debug this and clarify both the reproducibility concern (fixed seed) and
 * the portability fix (switching away from lrand48).
 * This note is kept here for reference.

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
   std::mt19937_64 gen(12345); // use the Mersenne Twister 19937 generator, seed with a fixed value for reproducibility
   std::uniform_int_distribution<int64_t> dis(0, N - 1);
   for (int64_t i = 0; i < N; i++)
   {
      A[i] = dis(gen); // initialize A with random indices in [0..N-1]
   }
   printf(" inside sum_indirect problem_setup, N=%lld \n", N);
}

float sum(int64_t N, float A[])
{
   printf(" inside sum_indirect perform_sum, N=%lld \n", N);
   float sum = 0.0;
   int index = 0;
   for (int i = 0; i < N; i++)
   {
      index = A[index]; // follow the pointer by using the value at A[index] as the next index
      sum += index;     // add all the value into sum

      // float v = A[index];
      // sum += v;
      // index = (int)v;

      // NOTE: In my initial version I updated the index first and then added the index value（as codes shows）.
      // After debugging and chat with GPT, it saids my first version may not fully follow the professor’s
      // definition (accumulate A[indx] where indx = A[indx]) although i think i am not wrong . By first accumulating A[indx]
      // and then updating the index, the implementation better matches the intended algorithm on slides.
      // finally，i keep this note and go back my first version and test both，because gpt is not always right.
   }
   return sum;
}
