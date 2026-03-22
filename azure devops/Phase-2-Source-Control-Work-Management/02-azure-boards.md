# Azure Boards - Agile Project Management

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

## Practical Exercise ✅
1. Create a new Azure DevOps project using the **Scrum** process.
2. Create an Epic "Build a Login System".
3. Add 2 Features under it and 2 User Stories under each Feature.
4. Set up a Sprint named "Sprint 1" (2 weeks).
5. Assign story points to each User Story and drag them into the sprint.
6. Move one item to "Done" and observe the burndown chart update.
