---
id: "010"
topic: java
title: "Java 21 virtual threads: blocking code that finally scales"
image:
  palette: java
  headline: "Virtual threads: blocking code that scales"
  diagram: |
    flowchart LR
        REQ["10k requests"]:::accent --> POOL["200-thread<br/>pool"]:::bad
        POOL --> BLOCK["Stalls on<br/>I/O waits"]:::bad
        REQ --> VT["Virtual<br/>thread each"]:::good
        VT --> SCALE["Millions of<br/>cheap waits"]:::good
        SCALE --> WIN["3k &rarr; 12k<br/>req/s"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Platform pool ~3,100 req/s vs virtual threads ~12,400 — same blocking code"
    - "Cheap for I/O waits, useless for CPU-bound work — pick the right spot"
    - "Never pool them: one virtual thread per task, that is the whole point"
alt_text: "Diagram comparing a saturated 200-thread pool against a virtual-thread-per-request model that scales throughput"
status: ready
---
3,100 to 12,400 requests per second. Same code, one switch.

That's virtual threads on an I/O-bound service — the headline of Java 21 for microservices. For a decade we hid blocking I/O behind thread pools and reactive code nobody enjoyed debugging; virtual threads end that trade-off.

Picture the same flood of requests on two roads — one squeezes through a 200-thread pool that stalls on every network wait; the other gives each request its own virtual thread and keeps scaling.

How to adopt it safely:

1. Turn it on where you wait on I/O — DB, HTTP, queues. That's where the win lives.
2. Keep CPU-bound work on platform threads; they add nothing when the core is busy.
3. Stop pooling — one virtual thread per task. Pooling something this cheap rebuilds the bottleneck.

The bigger lesson: Java 21 doesn't make code faster, it makes simple code scale. The new ceiling is connection pools and rate limits, not thread counts.

Where are thread pools still capping your throughput? 👇

📚 Part 1 of 3 — Java 21 for Microservices. Next: the pinning trap that froze services at Netflix.

#Java #Microservices
