## What’s the difference between API Gateway and Load Balancer?

**Load Balancer** and **API Gateway** are both components in a distributed system, but they serve different purposes.

- **Load Balancer:** A load balancer distributes incoming network traffic across multiple servers to ensure no single server is overwhelmed. Its primary goal is to improve availability and reliability. Load balancers operate at Layer 4 (TCP) or Layer 7 (HTTP) of the OSI model.

- **API Gateway:** An API Gateway acts as a single entry point for all clients. It handles tasks like authentication, authorization, rate limiting, and request routing to the appropriate microservices. It's a more application-aware component that sits in front of your APIs.

**In short:** A load balancer distributes traffic, while an API gateway manages, secures, and orchestrates APIs.

---

## What’s the difference between forward proxy and reverse proxy?

- **Forward Proxy:** A forward proxy sits in front of a client (or a group of clients) and forwards their requests to the internet. It can be used for security, filtering, and caching. The server that receives the request sees the IP address of the proxy, not the original client.

- **Reverse Proxy:** A reverse proxy sits in front of a server (or a group of servers) and forwards client requests to those servers. It's used for load balancing, SSL termination, and caching. The client that sends the request doesn't know which server is actually handling it.

---

## What is the difference between horizontal scaling and vertical scaling?

- **Horizontal Scaling (Scaling Out):** This involves adding more machines to your pool of resources. For example, adding more web servers to a cluster. It's generally more flexible and resilient than vertical scaling.

- **Vertical Scaling (Scaling Up):** This involves increasing the resources of a single machine, such as adding more CPU, RAM, or storage. It's often simpler to implement initially but can be more expensive and has physical limits.

---

## Explain microservices vs. monolithic architecture.

- **Monolithic Architecture:** In a monolithic architecture, the entire application is built as a single, unified unit. All the components are tightly coupled and run in the same process. This can be simpler to develop and deploy initially, but it can become difficult to maintain, scale, and update as the application grows.

- **Microservices Architecture:** In a microservices architecture, the application is broken down into a collection of small, independent services. Each service is responsible for a specific business capability and can be developed, deployed, and scaled independently. This provides more flexibility and resilience but also introduces more complexity in terms of deployment and management.

---

## What is CAP theorem?

The CAP theorem (also known as Brewer's theorem) states that it is impossible for a distributed data store to simultaneously provide more than two of the following three guarantees:

- **Consistency:** Every read receives the most recent write or an error.
- **Availability:** Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
- **Partition Tolerance:** The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

In a distributed system, you must choose between consistency and availability when a network partition occurs.

---

## How does a Rate Limiter work?

A rate limiter is a mechanism that controls the rate at which requests are processed. It's used to prevent abuse, ensure fair usage, and protect services from being overwhelmed.

**Common algorithms:**

- **Token Bucket:** A bucket is filled with tokens at a fixed rate. Each request consumes a token. If the bucket is empty, the request is rejected.
- **Leaky Bucket:** Requests are added to a queue (the bucket). They are processed at a fixed rate. If the queue is full, new requests are rejected.
- **Fixed Window Counter:** The number of requests in a fixed time window is tracked. If the count exceeds a threshold, requests are rejected.

---

## How does Single Sign-On (SSO) work?

Single Sign-On (SSO) allows a user to log in once and gain access to multiple applications without having to re-enter their credentials.

**Typical flow:**

1.  The user tries to access an application (the Service Provider or SP).
2.  The SP redirects the user to an Identity Provider (IdP) to authenticate.
3.  The user authenticates with the IdP.
4.  The IdP generates a token (e.g., a SAML assertion or a JWT) and sends it back to the user's browser.
5.  The browser sends the token to the SP.
6.  The SP validates the token and grants the user access.

---

## What is caching, and why is it important?

Caching is the process of storing copies of files or data in a temporary storage location (a cache) so that they can be accessed more quickly. It's important because it can significantly improve the performance and scalability of a system by:

- **Reducing latency:** By serving data from a cache closer to the user, you can reduce the time it takes to retrieve it.
- **Reducing load on backend services:** By serving frequently accessed data from a cache, you can reduce the number of requests that hit your backend servers.

---

## What are the types of load balancers and their use cases?

- **Layer 4 (Transport Layer):** These load balancers operate at the TCP/UDP level. They make routing decisions based on the source and destination IP addresses and ports. They are fast and efficient but don't have any knowledge of the application-level data.
- **Layer 7 (Application Layer):** These load balancers operate at the HTTP level. They can inspect the content of the requests (e.g., headers, URLs, cookies) and make more intelligent routing decisions. They are useful for things like content-based routing and SSL termination.

---

## How does sharding help in database scaling?

Sharding is a database scaling technique that involves breaking up a large database into smaller, more manageable pieces called shards. Each shard is a separate database, and they are distributed across multiple servers.

**Benefits:**

- **Improved Performance:** By distributing the data and the query load across multiple servers, you can improve the performance of your database.
- **Increased Scalability:** You can add more shards as your data grows, allowing you to scale your database horizontally.

---

## Differences between JWT, OAuth, and SAML?

- **JWT (JSON Web Token):** A compact, URL-safe means of representing claims to be transferred between two parties. It's often used for authentication and information exchange.

- **OAuth (Open Authorization):** An authorization framework that allows a third-party application to obtain limited access to a user's account on another service, without giving it the user's password.

- **SAML (Security Assertion Markup Language):** An XML-based standard for exchanging authentication and authorization data between parties, in particular, between an identity provider and a service provider. It's often used for enterprise-level single sign-on (SSO).
