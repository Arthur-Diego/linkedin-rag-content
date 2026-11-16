---
id: "025"
topic: system design
title: "Rate limiting with a token bucket: bursts allowed, floods rejected"
animation:
  scene: token-bucket
  title: "Rate Limiter"
  subtitle: "Token bucket · capacity 4 · refill 1 token/s"
alt_text: "Animated diagram of a token bucket rate limiter: a burst of requests drains four tokens and passes to the API, the next requests bounce back with HTTP 429, then the bucket refills one token per second and traffic flows again"
status: ready
---
4 tokens. That is all that stands between your API and a flood.

Watch the bucket: each request spends one token. The burst drains it, the next calls get a 429, and one new token per second lets traffic back in.

Capacity sets the burst you tolerate. Refill rate sets the load you can sustain.

Token bucket or sliding window: which one guards your API? 👇

#SystemDesign #RateLimiting #BackendEngineering
