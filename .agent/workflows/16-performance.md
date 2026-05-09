---
title: "PERFORMANCE"
description: "Profiling and bottleneck elimination."
order: 8
---

# Workflow: Performance Optimization



**Trigger**: User requests performance improvement, or profiling data shows bottlenecks.



## Purpose

Systematic performance optimization that measures before and after, and rejects changes that don't achieve meaningful improvement.



---



## Step 1: Measure Baseline

- Identify the metric to optimize (latency, throughput, memory, bundle size, startup time)

- Establish a reproducible measurement method

- Record baseline measurements (minimum 3 runs, take median)



## Step 2: Identify Bottleneck

- **Algorithmic**: Check time complexity. O(nÂ²) in a hot path? Replace with O(n log n) or O(n).

- **I/O Bound**: Unnecessary file reads, unoptimized queries, missing connection pooling

- **Memory**: Excessive allocations, missing object pooling, unbounded caches

- **Rendering**: Layout thrashing, unnecessary repaints, large DOM trees



## Step 3: Apply Language-Specific Optimizations



### Python

- Replace loops with vectorized operations (numpy/pandas)

- Use `__slots__` for memory-critical classes

- Profile with `cProfile` + `snakeviz`



### Rust

- Avoid unnecessary allocations (use `&str` over `String`, `&[T]` over `Vec<T>`)

- Use `rayon` for data parallelism

- Profile with `cargo flamegraph`



### JavaScript/TypeScript

- Minimize bundle size (tree shaking, code splitting, lazy loading)

- Use `requestAnimationFrame` for visual updates

- Profile with Chrome DevTools Performance tab



### C

- Enable compiler optimizations (`-O2` or `-O3`)

- Minimize cache misses (struct-of-arrays vs array-of-structs)

- Profile with `perf` or `gprof`



### Go

- Use `sync.Pool` for frequently allocated objects

- Minimize allocations in hot paths (pre-allocate slices)

- Profile with `go tool pprof`



## Step 4: Verify Improvement

- Re-run baseline measurement

- **Threshold**: Change must show â‰¥15% improvement on the target metric

- If improvement < 15%: **discard the change** (complexity cost exceeds benefit)

- If improvement â‰¥ 15%: commit with performance data in commit message



## Step 5: Regression Guard

- Add a benchmark test that codifies the new performance expectation

- Document the optimization in code comments explaining WHY this approach is faster

