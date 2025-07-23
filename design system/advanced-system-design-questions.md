# Advanced System Design Interview Questions (10+ Years Experience)

With 10 years of experience, you can expect more open-ended, large-scale system design questions that test your architectural and leadership skills. The focus will be less on simple definitions and more on trade-offs, scalability, reliability, and cost.

### Large-Scale Application Design

1.  **Design a service like Netflix or YouTube.**
    *   *Follow-ups:* How would you handle video transcoding and delivery (CDN)? How would you design the recommendation engine? How would you manage user data and watch history? How would you handle the massive storage requirements?
2.  **Design a service like Twitter or Facebook's News Feed.**
    *   *Follow-ups:* How do you generate the feed for a user? What is the "fan-out" problem? How would you handle the "celebrity" problem (a user with millions of followers)? How would you design the system to be real-time?
3.  **Design a service like Uber or Lyft.**
    *   *Follow-ups:* How do you match riders with drivers in real-time? How do you handle location updates from millions of drivers? How would you design the pricing system (surge pricing)? How would you ensure the reliability of the service?
4.  **Design a service like Google Docs or Dropbox.**
    *   *Follow-ups:* How would you handle real-time collaborative editing? How would you manage file synchronization across multiple devices? How would you design the system to handle large files and version history?
5.  **Design a distributed web crawler.**
    *   *Follow-ups:* How do you avoid crawling the same page multiple times? How do you handle politeness (not overwhelming a server)? How do you parse and store the crawled data? How would you scale the system to crawl billions of pages?

### Foundational and Architectural Concepts

6.  **How would you design a highly available and scalable key-value store (like Redis or DynamoDB)?**
    *   *Follow-ups:* Discuss data partitioning (sharding), replication, and consistency models (strong vs. eventual). How would you handle leader election and failure detection?
7.  **Design a distributed message queue (like Kafka or RabbitMQ).**
    *   *Follow-ups:* How do you ensure "at-least-once" or "exactly-once" delivery? How would you design for high throughput and low latency? How would you handle consumer groups and topic partitioning?
8.  **Design a URL shortening service (like TinyURL or bit.ly).**
    *   *Follow-ups:* How do you generate unique short URLs? How do you handle the mapping from short to long URLs at scale? How would you handle custom URLs and analytics?
9.  **Design a rate limiter for an API.**
    *   *Follow-ups:* Discuss different algorithms (e.g., token bucket, leaky bucket). How would you implement this in a distributed environment? Where would you store the rate-limiting data?
10. **You are tasked with reducing the infrastructure cost of a large, existing system by 30%. What is your process?**
    *   *Follow-ups:* This tests your practical experience. Discuss your approach to profiling, identifying bottlenecks, using reserved instances, leveraging serverless architectures, optimizing database usage, and implementing auto-scaling.
