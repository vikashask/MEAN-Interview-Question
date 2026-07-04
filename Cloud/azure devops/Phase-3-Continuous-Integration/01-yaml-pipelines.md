# Azure Pipelines - YAML From the Ground Up

> **Expert framing:** Basic knowledge gets you a pipeline that builds and deploys. Expert knowledge gets you a pipeline that's **fast** (parallelism, caching), **safe** (conditions that actually match intent, not just "it happened to work"), and **maintainable** (templates instead of copy-pasted YAML across 10 repos). Interviewers probe the difference between `variables` (compile-time-ish, always a string) and `parameters` (true compile-time, typed) constantly — know it cold.

## YAML Pipeline Anatomy

Every Azure Pipeline is defined in a `azure-pipelines.yml` file at the root of your repository.

```yaml
# ================================================================
# ANATOMY OF A YAML PIPELINE
# ================================================================

# Trigger: When does this pipeline run?
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - '**/*.md'    # Don't trigger on docs-only changes

# Pull Request trigger
pr:
  branches:
    include:
      - main

# Which agent pool to use
pool:
  vmImage: 'ubuntu-latest'  # Microsoft-hosted agent
  # name: 'My-Self-Hosted-Pool'  # For self-hosted

# Pipeline-level variables
variables:
  buildConfiguration: 'Release'
  nodeVersion: '20.x'
  MY_SECRET: $(SECRET_FROM_LIBRARY)  # From variable group

stages:
  - stage: Build
    displayName: '🏗️ Build & Test'
    jobs:
      - job: BuildJob
        displayName: 'Build the Application'
        steps:
          - task: NodeTool@0
            displayName: 'Install Node.js'
            inputs:
              versionSpec: $(nodeVersion)

          - script: |
              npm ci
              npm run build
              npm test
            displayName: 'Install, Build & Test'
            workingDirectory: '$(System.DefaultWorkingDirectory)'

          - task: PublishTestResults@2
            displayName: 'Publish Test Results'
            condition: succeededOrFailed()  # Run even if tests fail
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: '**/test-results.xml'

          - task: PublishPipelineArtifact@1
            displayName: 'Upload Build Artifact'
            inputs:
              targetPath: '$(System.DefaultWorkingDirectory)/dist'
              artifact: 'webapp-build'
              publishLocation: 'pipeline'

  - stage: Deploy_Dev
    displayName: '🚀 Deploy to Dev'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployDev
        displayName: 'Deploy to Dev App Service'
        environment: 'Development'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: DownloadPipelineArtifact@2
                  inputs:
                    artifact: 'webapp-build'
                    path: '$(Pipeline.Workspace)/webapp-build'

                - task: AzureWebApp@1
                  displayName: 'Deploy to Azure App Service'
                  inputs:
                    azureSubscription: 'My-Azure-Service-Connection'
                    appName: 'app-mywebapp-dev'
                    package: '$(Pipeline.Workspace)/webapp-build'
```

---

## Important Pipeline Variables

```yaml
# Predefined pipeline variables (always available):
variables:
  BUILD_ID: $(Build.BuildId)                        # e.g. 42
  BUILD_NUMBER: $(Build.BuildNumber)                # e.g. 20240224.3
  BRANCH: $(Build.SourceBranch)                     # refs/heads/main
  BRANCH_NAME: $(Build.SourceBranchName)            # main
  REASON: $(Build.Reason)                           # IndividualCI, PullRequest, Manual
  REPO: $(Build.Repository.Name)
  WORKSPACE: $(System.DefaultWorkingDirectory)
  ARTIFACT_DIR: $(Build.ArtifactStagingDirectory)
```

---

## Runtime Parameters (vs Variables)

```yaml
parameters:
  - name: environment
    displayName: 'Target Environment'
    type: string
    default: dev
    values:
      - dev
      - staging
      - prod

  - name: runTests
    displayName: 'Run tests?'
    type: boolean
    default: true

jobs:
  - job: BuildJob
    steps:
      - script: echo "Deploying to ${{ parameters.environment }}"
      
      - script: npm test
        displayName: 'Run Tests'
        condition: ${{ parameters.runTests }}
```

**Expert insight — variables vs parameters, the distinction that trips people up:**
- **Parameters** (`${{ parameters.x }}`) are resolved at **template/YAML compile time**, before the pipeline even starts running. They're typed (string, boolean, number, object, list), can restrict allowed `values`, and can even control which *stages/jobs exist at all* (structural decisions) — but they can't be changed by a running step.
- **Variables** (`$(x)`) are resolved at **runtime**, are always strings under the hood, and can be set/overridden by a step (`##vso[task.setvariable]`), making them the right tool for values computed *during* the run (like a version number read from `package.json`).
- Rule of thumb: use **parameters** for anything that changes pipeline *structure* (which stages run, which template to include); use **variables** for anything that's just a runtime value passed into steps.

---

## Conditions, Expressions & Output Variables

```yaml
steps:
  - script: echo "This runs only on main"
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')

  - script: echo "Runs when previous step fails"
    condition: failed()

  - script: echo "Always runs (even on cancellation)"
    condition: always()
    
  # Set an output variable to use in the next step/job
  - bash: |
      VERSION=$(cat package.json | python3 -c "import sys, json; print(json.load(sys.stdin)['version'])")
      echo "##vso[task.setvariable variable=APP_VERSION;isOutput=true]$VERSION"
    name: SetVersionStep
    displayName: 'Read app version'

  - script: echo "Version is $(SetVersionStep.APP_VERSION)"
```

---

## Common Pitfalls & Expert Tips

- **Confusing `condition: succeeded()` (the implicit default) with actually needed logic.** Every step/job implicitly requires the previous one to succeed unless you override with `condition: always()`, `succeededOrFailed()`, or a custom expression — forgetting this means a "cleanup" step you wanted to always run gets silently skipped after a failure.
- **`trigger` vs `pr` confusion.** `trigger` controls CI runs on pushes to branches; `pr` controls validation runs on pull requests — they're independent. Forgetting to configure `pr` means PRs merge without any pipeline validation at all.
- **Runtime expressions (`$[ ]`) vs compile-time expressions (`${{ }}`) vs macro syntax (`$( )`)** are three different evaluation times in the same YAML file — mixing them up (e.g. expecting `${{ }}` to see a variable set by an earlier *runtime* step) is one of the most common YAML pipeline bugs, because `${{ }}` is already resolved before the pipeline runs, so it can never see a runtime-set variable.
- **Not pinning the agent image version** (`vmImage: 'ubuntu-latest'`) for anything sensitive to toolchain versions — "latest" images get updated by Microsoft periodically and can silently change installed tool versions, breaking a previously-passing pipeline with no code change on your side.
- **Overusing `condition: always()`** on deploy steps — this can cause a deployment step to run even after a build failure, potentially deploying broken/incomplete artifacts.

---

## Practical Exercise ✅
1. Push a simple Node.js or Python app to your Azure Repo.
2. Create an `azure-pipelines.yml` at the root of the repo.
3. Configure it to trigger on `main`.
4. Add steps to: install dependencies, run tests, and publish the artifact.
5. Run the pipeline and verify the artifact is published in the "Artifacts" tab.

---

## Expert Interview Q&A

**Q: `${{ }}` vs `$( )` vs `$[ ]` in Azure Pipelines YAML — what's the actual difference?**
`${{ }}` is a **compile-time (template) expression** — resolved before the pipeline run starts, used for parameters and structural template logic. `$( )` is a **runtime (macro) expression** — resolved at the start of each step, mainly for variables, always substituted as plain text before the step runs. `$[ ]` is a **runtime expression** evaluated just before a task runs, typically used in `condition:` and can reference output variables from earlier steps in the same job/stage. Mixing these up — e.g. trying to reference a runtime-set variable with `${{ }}` — silently fails because that syntax already resolved before the variable existed.

**Q: How would you pass a value computed in one job to another job in a later stage?**
Set it as an output variable in the producing job (`##vso[task.setvariable variable=x;isOutput=true]` with a named step), then reference it in the consuming job/stage via `dependencies` (cross-stage) or `stageDependencies`, e.g. `$[ stageDependencies.Build.BuildJob.outputs['SetVersionStep.APP_VERSION'] ]` — this is a very common real-world need (e.g., passing a computed version number from Build to Deploy).

**Q: Why might a pipeline that was passing suddenly start failing with no code changes?**
Common culprits: a Microsoft-hosted agent image update (`ubuntu-latest` silently changed a tool version), an expired/rotated service connection or secret, a dependency (npm/NuGet package) publishing a breaking change picked up by an unpinned version range, or an external service the pipeline depends on being down/changed. Pinning agent images and dependency versions reduces this class of "mystery failure."

**Q: What's the danger of setting `condition: always()` broadly across a pipeline?**
It causes a step/job to run even after upstream failures — appropriate for cleanup/notification steps, but dangerous on deployment steps, where it could deploy a partially-built or broken artifact after a failed build stage. Conditions should be deliberately chosen per step based on what's actually safe to run in a failure state.
