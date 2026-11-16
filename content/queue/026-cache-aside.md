---
id: "026"
topic: system design
title: "Cache-aside: one miss pays for every hit that follows"
animation:
  title: "Cache-Aside"
  subtitle: "Read path · the app owns the cache"
  nodes:
    - {id: client, label: Client, sub: "GET /product/42", at: [0, 0], color: blue}
    - {id: app, label: Service, sub: "cache-aside", at: [1, 0], color: violet}
    - {id: cache, label: Redis, sub: "TTL 5 min", at: [2, 0], color: yellow}
    - {id: db, label: PostgreSQL, sub: "source of truth", at: [1, 1], color: green}
  edges:
    - {from: client, to: app, label: read}
    - {from: app, to: client, label: value}
    - {from: app, to: cache, label: "1. get"}
    - {from: cache, to: app, label: "hit / miss"}
    - {from: app, to: db, label: "2. on miss"}
    - {from: db, to: app, label: row}
  tally: {ok: "cache hits", warn: "database reads"}
  steps:
    - caption: "First read: the cache has nothing yet"
      packets:
        - {path: [client, app, cache, app], kind: bad, turns: 2}
    - caption: "Miss: read the database once"
      packets:
        - {path: [app, db, app], kind: warn}
    - caption: "Write the value back with a TTL"
      packets:
        - {path: [app, cache], kind: info}
    - caption: "Next reads never touch the database"
      packets:
        - {path: [client, app, cache, app, client], kind: ok, turns: 2, count: 4, every: 0.5}
alt_text: "Animated diagram of the cache-aside read path: the first read misses Redis, the service reads PostgreSQL once and writes the value back with a TTL, and the following reads are served from the cache without touching the database"
status: ready
---
One miss. Then every read skips the database.

Watch the first request: Redis has nothing, so the service reads PostgreSQL once and writes the value back with a TTL. The next reads are served from memory.

Always set that TTL: a key that never expires turns one stale write into a permanent bug.

What TTL do you use on your hottest keys? 👇

#SystemDesign #Caching #BackendEngineering
