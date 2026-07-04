# Azure Boards - Agile Project Management

> **Expert framing:** Anyone can drag a card across a Kanban board. The expert-level skill is using Boards data (velocity, cumulative flow, cycle time) to actually diagnose process problems — and knowing WIQL well enough to build custom queries/dashboards instead of manually hunting through backlogs. This is also the layer that gives CI/CD **traceability** — an expert makes sure every PR and build links back to a work item, since that link is what auditors and incident post-mortems rely on.

## Process Templates Overview
When creating an Azure DevOps project, you choose a **process template**:

| Template | Best For | Work Item Types |
|----------|----------|-----------------|
| **Agile** | Flexible projects | Epic, Feature, User Story, Task, Bug, Issue |
| **Scrum** | Sprint-based delivery | Epic, Feature, Product Backlog Item (PBI), Task, Bug |
| **Basic** | Simple tracking | Epic, Issue, Task |
| **CMMI** | Formal governance | Epic, Feature, Requirement, Task, Bug, Change Request |

> **Recommendation**: Use **Scrum** for most DevOps teams. It maps directly to how Azure Pipelines and sprints work together.

---

## Work Item Hierarchy

```
Epic (months of work - e.g., "Redesign Authentication System")
  └── Feature (weeks of work - e.g., "Implement OAuth 2.0 Login")
       └── User Story / PBI (days of work - e.g., "As a user, I can log in with Google")
            ├── Task (hours of work - e.g., "Implement Google OAuth callback endpoint")
            └── Bug (a defect found in testing)
```

---

## Sprint Planning on Azure Boards

### Setting Up a Sprint
1. Go to **Boards > Sprints > New Sprint**
2. Set start and end dates.
3. Drag items from the **Backlog** into the Sprint.
4. Set **Capacity** per team member (e.g., 6 hours/day).

### Kanban Board Columns (Typical Flow)
```
New  -->  Active  -->  In Review  -->  Done
```
You can customize columns in **Board Settings** to match your workflow (e.g., add a "In Testing" column).

---

## Work Item Best Practices

### Writing a Good User Story
```
Title: Login with Google Account

As a [registered user],
I want to [log in using my Google account],
So that [I don't have to remember a separate password].

Acceptance Criteria:
- [ ] "Login with Google" button appears on the login page.
- [ ] Clicking it redirects to Google OAuth consent screen.
- [ ] After consent, user is redirected back and logged into the app.
- [ ] User account is created automatically if first time.

Story Points: 5
```

---

## WIQL (Work Item Query Language)

WIQL is a SQL-like language for querying Azure Boards work items. You can access it under **Boards > Queries > New Query > Edit WIQL**.

### Example Queries

```sql
-- All active bugs assigned to me
SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.State] = 'Active'
  AND [System.AssignedTo] = @Me
ORDER BY [System.CreatedDate] DESC

-- All User Stories in the current sprint
SELECT [System.Id], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.StoryPoints]
FROM WorkItems
WHERE [System.WorkItemType] = 'User Story'
  AND [System.IterationPath] = @CurrentIteration('[Your Project]\[Your Team]')

-- Flat list of all items changed in the last 7 days
SELECT [System.Id], [System.Title], [System.ChangedDate]
FROM WorkItems
WHERE [System.ChangedDate] >= @Today - 7
ORDER BY [System.ChangedDate] DESC

-- Bug count by state
SELECT [System.State], COUNT([System.Id])
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
GROUP BY [System.State]
```

---

## Dashboards & Reporting
Navigate to **Overview > Dashboards > Add Widget**. Useful widgets:
- **Sprint Burndown**: Shows remaining work (story points) vs time.
- **Velocity**: Story points completed per sprint over time.
- **Cumulative Flow Diagram**: Visualizes WIP and bottlenecks.
- **Build History**: Shows CI pipeline pass/fail rate.

**Expert insight — reading these charts, not just displaying them:**
- A Burndown chart that's flat for days then drops suddenly usually means work isn't being broken into small enough tasks (batch-completing instead of incremental progress) — a process smell, not just a chart shape.
- A Cumulative Flow Diagram with a widening "In Progress" band (versus "Done") over time signals WIP is growing faster than the team can close it — the fix is usually a WIP limit on the board, not "work harder."
- Velocity should be used for *forecasting*, never as a performance metric for individuals — teams that get graded on velocity start inflating story point estimates, which destroys the metric's usefulness (Goodhart's Law in action, a classic anti-pattern interviewers like to probe).

---

## Azure Boards REST API
Automate work item creation from your scripts or pipelines:

```bash
# Create a work item via REST API (requires a Personal Access Token - PAT)
curl -X POST "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/\$Task?api-version=7.1" \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: Basic $(echo -n ':YOUR_PAT' | base64)" \
  -d '[
    { "op": "add", "path": "/fields/System.Title", "value": "Automated Task from Pipeline" },
    { "op": "add", "path": "/fields/System.AssignedTo", "value": "user@company.com" },
    { "op": "add", "path": "/fields/System.State", "value": "Active" }
  ]'
```

---

## Common Pitfalls & Expert Tips

- **No linked work item on commits/PRs.** This breaks end-to-end traceability (a core AZ-400 exam theme) — you lose the ability to answer "which work item caused this production deploy" during an incident review. Enforce it via a branch policy ("Check for linked work items: Required").
- **Treating story points as time estimates.** Points measure relative *complexity/effort*, not hours — teams that convert points to hours 1:1 end up fighting the estimation process instead of using it.
- **Over-customizing the process template early.** Heavy workflow customization (custom states, custom fields) before the team has stabilized its actual process creates rigid tooling that fights how the team really works. Start with a stock template, customize only after real pain points emerge.
- **WIQL queries scoped too broadly** (`SELECT * FROM WorkItems` with no filters) are slow and return noise — always scope by `IterationPath`, `AreaPath`, `WorkItemType`, or date range.

---

## Practical Exercise ✅
1. Create a new Azure DevOps project using the **Scrum** process.
2. Create an Epic "Build a Login System".
3. Add 2 Features under it and 2 User Stories under each Feature.
4. Set up a Sprint named "Sprint 1" (2 weeks).
5. Assign story points to each User Story and drag them into the sprint.
6. Move one item to "Done" and observe the burndown chart update.

---

## Expert Interview Q&A

**Q: Why does "traceability" matter in a regulated or enterprise DevOps setup, and how does Azure Boards provide it?**
Traceability means you can trace a line from a business requirement (Epic/Feature) → a specific User Story → the commit(s)/PR that implemented it → the build/release that shipped it. This matters for audits (proving controlled, reviewed change) and incident response (finding exactly what shipped and why). Azure Boards provides it via work item linking — branch policies requiring linked work items, and PR descriptions referencing `AB#<id>` automatically link the PR, commit, and eventual build to that work item.

**Q: Your team's velocity chart is flat/declining even though people say they're busy. What would you investigate?**
Whether story points are being estimated consistently (definition-of-done drift), whether work is being started but not finished (check the Cumulative Flow Diagram for a growing "In Progress" band — a WIP problem, not a speed problem), and whether unplanned/interrupt work (production incidents, ad-hoc requests) is consuming capacity without being tracked on the board at all.

**Q: What's the risk of using story points as an individual performance metric?**
It creates an incentive to inflate estimates (easier to "hit" a bigger number) or avoid picking up hard/ambiguous work, which corrupts the very data you rely on for sprint forecasting — a textbook Goodhart's Law problem ("when a measure becomes a target, it ceases to be a good measure"). Points should stay a team-level planning/forecasting tool, never an individual scorecard.
