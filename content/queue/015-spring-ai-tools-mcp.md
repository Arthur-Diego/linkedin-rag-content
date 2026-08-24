---
id: "015"
topic: spring ai
title: "Spring AI agents: tool calling, MCP and the scaling trap"
image:
  palette: spring
  headline: "Spring AI agents: tools, MCP, the scaling trap"
  diagram: |
    flowchart LR
        AG["Spring AI<br/>agent"]:::accent --> MCP["MCP tool<br/>calling"]:::good
        MCP --> STATE["Stateful<br/>sessions"]:::bad
        STATE --> STICKY["Sticky routing<br/>no scale-out"]:::bad
        MCP --> LESS["Stateless<br/>sessions"]:::good
        LESS --> SCALE["Scales behind<br/>any gateway"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "MCP standardizes tools: consume remote servers, expose your own @McpTool"
    - "Spring AI 2.0 made the tool-calling loop composable — observe and guard steps"
    - "Stateful MCP sessions force sticky routing — design for stateless scale-out"
alt_text: "Diagram showing a Spring AI agent calling MCP tools, contrasting stateful sticky sessions against stateless sessions that scale behind a gateway"
status: ready
---
Tool calling is 50 lines now. Scaling it isn't.

Spring AI made agents almost trivial: annotate a method with @McpTool and the model can call it. Through the Model Context Protocol, your service both consumes remote tools and exposes its own — no language lock-in.

Picture the same agent under load: one pins session state to a server and forces sticky routing; the other runs stateless sessions and scales behind any gateway.

What separates a demo from production:

1. Treat tools as a security boundary. An agent that calls tools turns prompt injection into real actions — validate inputs and scope permissions per tool.
2. Use Spring AI 2.0's composable tool loop to observe and guard each step, not fire and hope.
3. Plan for scale-out: stateful MCP sessions force sticky routing. Externalize session state so restarts and autoscaling stay transparent.
4. Test tools like endpoints — contract tests on the MCP schema, not just the happy path.

The bigger lesson: the model isn't your hard part anymore. Security boundaries and horizontal scaling are — the same problems microservices always had, now wearing an AI hat.

What would you let an AI agent actually execute in your system? 👇

📚 Part 3 of 3 — Spring AI for Microservices.

#SpringAI #Microservices
