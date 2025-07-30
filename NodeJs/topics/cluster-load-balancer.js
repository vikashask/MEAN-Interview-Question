/*
In Node.js, the cluster module provides a way to create child processes (called "workers") 
that all share the same server port. This allows your application to take advantage of 
multi-core systems, something a single Node.js process cannot do on its own.

1.Single-Thread Limitation: By default, a single Node.js process runs on a single thread and can only use 
one CPU core, even if the machine has 8, 16, or more cores. This means most of the server's processing 
power goes unused.

2.Creating a Cluster: The cluster module solves this by allowing a master process to fork multiple worker
 processes. Your script correctly identifies the number of available CPU cores (os.cpus().length) and forks a worker for each core.

3.Distributing Traffic (Load Balancing):
The master process listens for incoming requests and distributes them among the worker processes.

4.Increasing Performance and Resilience:
Each worker can handle requests independently, which increases the overall throughput of your application.
If a worker crashes, the master can fork a new one to replace it, ensuring that your application remains available.

*/

const cluster = require("cluster");
const os = require("os");
const express = require("express");

const numCPUs = os.cpus().length;
const PORT = 3000;

if (cluster.isMaster) {
  console.log(`Master process ${process.pid} is running`);
  console.log(`Forking for ${numCPUs} CPUs`);

  // Fork worker processes.
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Listen for dying workers
  cluster.on("exit", (worker, code, signal) => {
    console.log(
      `Worker ${worker.process.pid} died with code: ${code}, and signal: ${signal}. Forking a new one...`
    );
    cluster.fork();
  });
} else {
  // Worker processes have an Express server.
  const app = express();

  app.get("/", (req, res) => {
    const message = `Hello from worker ${process.pid}`;
    console.log(`Request handled by worker ${process.pid}`);
    res.send(message);
  });

  app.listen(PORT, () => {
    console.log(`Worker ${process.pid} started and listening on port ${PORT}`);
  });
}

/*
To run this:
1. Make sure you have express installed:
   npm install express

2. Run the server:
   node 3.cluster-load-balancer.js

3. Open your browser or use a tool like `curl` to access http://localhost:3000.
   Make multiple requests to see the process ID change.

You will see in the console that requests are being handled by different worker processes,
confirming that the load is being distributed.

Example output from curl:
$ curl http://localhost:3000
Hello from worker 23456
$ curl http://localhost:3000
Hello from worker 23457
*/
