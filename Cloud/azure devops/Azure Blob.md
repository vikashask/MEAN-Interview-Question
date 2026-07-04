# Azure Blob Storage

> **Expert framing:** Blob Storage underpins a lot of what you already do in Azure DevOps — Terraform remote state, pipeline artifacts, static website hosting, and backup/DR targets all live here. The exam/interview-relevant depth is the access tier trade-offs, redundancy options, and consistency model — not just "it stores files."

## What It Is

Blob Storage is Azure's object storage service for unstructured data — images, videos, documents, backups, logs, and (relevant to this repo) Terraform state files and pipeline artifacts. "Blob" = Binary Large OBject; think of it as a massively scalable file store accessed over HTTP(S) rather than a traditional file system.

## Key Capabilities

- **Access tiers — Hot, Cool, Archive, and Premium.** These trade storage cost against retrieval cost/latency:
  - **Hot**: highest storage cost, lowest access cost, lowest latency — for data accessed frequently (active application data).
  - **Cool**: lower storage cost, higher access cost — for infrequently accessed data kept for at least 30 days (backups, older logs).
  - **Archive**: lowest storage cost, highest access cost and latency (retrieval can take **hours**, not seconds) — for data rarely accessed and kept for at least 180 days (compliance archives, cold backups).
  - **Premium**: SSD-backed, low-latency, higher cost — for workloads needing consistently fast access to smaller objects (e.g., some IoT/telemetry scenarios).

- **Strong consistency.** When an object is written/changed, every subsequent read sees that change immediately — no "eventual consistency" window where a read might return stale data right after a write. This matters a lot for Terraform remote state: you need the very next `plan`/`apply` to see the latest committed state, not a stale cached copy.

- **Object mutability.** Blobs support in-place edits (for append/block blob operations) rather than requiring a full re-upload for every change — reduces bandwidth and improves performance for workloads that incrementally update files (e.g., append-only logs).

- **Multiple blob types**:
  - **Block blobs** — the default; optimized for uploading/storing discrete files (images, documents, pipeline artifacts, backups).
  - **Append blobs** — optimized for append-only operations, ideal for logging scenarios where you continuously add data to the end of a blob.
  - **Page blobs** — optimized for random read/write access, used as the backing storage for VM disks (VHDs).

- **Geo-redundancy, configured with one setting.** Rather than manually engineering cross-region replication, you pick a redundancy option and Azure handles it:
  - **LRS** (Locally Redundant Storage): 3 copies within one datacenter — cheapest, protects against hardware failure only.
  - **ZRS** (Zone-Redundant Storage): copies across 3 Availability Zones in one region — protects against a datacenter-level failure.
  - **GRS** (Geo-Redundant Storage): LRS in the primary region + async-replicated copy in a secondary region — protects against a full regional outage, but the secondary copy isn't readable unless a failover occurs (or you use RA-GRS, which allows read access to the secondary).
  - **GZRS**: combines ZRS in the primary region with geo-replication to a secondary region — the strongest standard option, combining zone and regional resilience.

- **One infrastructure, worldwide access.** A single storage account is reachable globally over HTTPS, with the option to front it with a CDN (or Azure Front Door) for lower-latency global delivery of frequently accessed content.

- **Exabyte-scale, any data type.** Designed for petabyte/exabyte-scale unstructured data storage — images, video, audio, documents, backups — with the same durability guarantees regardless of volume.

## Where This Shows Up in Azure DevOps Work

- **Terraform remote state** — the `azurerm` backend stores `.tfstate` in a Blob container, relying on strong consistency (so the next `plan` always sees the latest state) and blob leases for locking.
- **Pipeline artifacts** — under the hood, published pipeline artifacts are stored in blob-backed storage.
- **Static website hosting** — Blob Storage can directly serve a static site (HTML/CSS/JS) without a web server, commonly fronted by a CDN.
- **Backup and DR targets** — Cool/Archive tiers are the standard destination for long-term backup retention given their low storage cost.

## Common Pitfalls & Expert Tips

- **Choosing Archive tier for anything that might need occasional quick access.** Archive retrieval isn't instant — it requires an explicit "rehydrate" operation that can take hours. Using Archive for data you might need same-day creates painful, unplanned delays.
- **Assuming LRS is "good enough" for anything production-critical.** LRS only protects against hardware failure within a single datacenter — a datacenter-level event (fire, flood, power loss) can mean data loss. Production workloads needing real resilience should use at minimum ZRS, or GRS/GZRS for regional disaster protection.
- **Confusing GRS with "automatically available in the secondary region."** Standard GRS replicates asynchronously to the secondary region, but you can't *read* from the secondary unless a Microsoft-initiated failover occurs (or you specifically provisioned RA-GRS, which allows read access to the secondary copy directly).
- **Storing Terraform state without understanding it's stored in plaintext, including any sensitive values.** Combine Blob Storage's encryption-at-rest (on by default) with strict RBAC on the storage account/container — don't rely on "it's just a blob container" as sufficient protection for state files with secrets in them.

## Expert Interview Q&A

**Q: Why does strong consistency matter specifically for using Blob Storage as a Terraform state backend?**
Terraform's correctness depends on every `plan`/`apply` reading the true, most recent state — if storage had eventual consistency, a `plan` run immediately after another engineer's `apply` could read a stale version of the state and compute an incorrect (or destructive) plan. Blob Storage's strong consistency guarantees the very next read reflects the most recent write, which is essential for safe concurrent Terraform usage.

**Q: A team wants to reduce storage costs for 2-year-old audit logs. What Blob Storage feature would you recommend, and what's the trade-off?**
Move them to the Archive tier via a lifecycle management policy (auto-transition after a defined age). The trade-off is retrieval time — Archive data isn't instantly accessible; rehydrating a blob back to Hot/Cool tier for reading can take hours, so this is only appropriate for data that's very rarely accessed and where hours-long retrieval latency is acceptable (which audit logs for compliance typically are).

**Q: What's the actual difference between GRS and RA-GRS, and why would that distinction matter during a regional outage?**
GRS replicates data asynchronously to a secondary region, but that secondary copy is only accessible after Microsoft performs (or you initiate, where supported) an account failover — you can't read from it under normal operation. RA-GRS (Read-Access GRS) additionally exposes a read-only endpoint against the secondary region at all times, meaning during a primary-region outage, read operations can continue against the secondary immediately, without waiting for a failover to complete — important for read-heavy availability requirements during an incident.

Links: [Azure Blob Storage quickstart](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal)
