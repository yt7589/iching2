#!/bin/bash

bash scripts/build.sh

date

echo "---------------------------------------------------------------------------------------------------------------------------------------------------------"
echo " Benchmark before and after optimization for Logger string handling. "
echo "---------------------------------------------------------------------------------------------------------------------------------------------------------"
./cmake-build-release/logger_benchmark

echo "---------------------------------------------------------------------------------------------------------------------------------------------------------"
echo " Benchmark before and after optimization for release builds. "
echo "---------------------------------------------------------------------------------------------------------------------------------------------------------"
./cmake-build-release/release_benchmark

echo "---------------------------------------------------------------------------------------------------------------------------------------------------------"
echo " Benchmark using std::arrays and std::unordered_maps as hash maps. "
echo "---------------------------------------------------------------------------------------------------------------------------------------------------------"
./cmake-build-release/hash_benchmark