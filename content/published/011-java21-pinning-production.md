---
id: '011'
topic: java
title: 'Java 21 virtual threads in production: the pinning trap'
image:
  palette: java
  headline: 'Virtual threads: mind the pinning trap'
  diagram: "flowchart LR\n    VT[\"Virtual<br/>thread\"]:::accent --> SYNC[\"synchronized<br/>block\"\
    ]:::bad\n    SYNC --> PIN[\"Pinned to<br/>carrier\"]:::bad\n    PIN --> STALL[\"\
    Carriers<br/>starved\"]:::bad\n    VT --> LOCK[\"ReentrantLock\"]:::good\n   \
    \ LOCK --> FREE[\"Unmounts<br/>while waiting\"]:::good\n    FREE --> SAFE[\"Carriers<br/>stay\
    \ free\"]:::accent\n    classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d\n\
    \    classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d\n    classDef accent\
    \ fill:#0284c7,stroke:#0369a1,color:#ffffff\n"
  bullets:
  - A blocking synchronized block pins the carrier — a few can starve every core
  - Netflix hit timeouts from pinning long before any CPU maxed out
  - Java 24 (JEP 491) ends synchronized pinning — until then, use ReentrantLock
alt_text: Diagram contrasting a synchronized block that pins a virtual thread to its
  carrier against a ReentrantLock that lets it unmount
status: published
published_at: '2026-08-28T13:35:03+00:00'
linkedin_post_id: urn:li:share:7499097216872165376
---
Netflix flipped on virtual threads and watched healthy services freeze.

No CPU spike, no error — just intermittent timeouts. The culprit had a name: pinning.

A virtual thread only scales because it unmounts from its carrier while it waits. Enter a synchronized block and it can't — it stays nailed to that platform thread. A few pinned carriers, and the pool starves while the cores sit idle.

Picture two paths through the same lock — one grabs a synchronized monitor and pins the carrier; the other takes a ReentrantLock, unmounts cleanly, and leaves it free.

Running virtual threads in production:

1. Hunt pinning early — run with -Djdk.tracePinnedThreads=full and watch for stack traces under load.
2. Swap synchronized on blocking paths for ReentrantLock; the hot spots hide in libraries and pools.
3. Drop ThreadLocal for per-request state — it can pin and bloats the heap at millions of threads.

The bigger lesson: a new runtime moves the bottleneck, it doesn't delete it. Java 24's JEP 491 ends synchronized pinning — but audit before you trust it.

Ever chased a freeze no CPU graph could explain? 👇

📚 Part 2 of 3 — Java 21 for Microservices. Next: the Java 21 features beyond threads that reshape your service.

#Java #Microservices
