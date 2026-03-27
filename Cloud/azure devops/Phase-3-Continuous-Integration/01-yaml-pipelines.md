# Azure Pipelines - YAML From the Ground Up

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

## Practical Exercise ✅
1. Push a simple Node.js or Python app to your Azure Repo.
2. Create an `azure-pipelines.yml` at the root of the repo.
3. Configure it to trigger on `main`.
4. Add steps to: install dependencies, run tests, and publish the artifact.
5. Run the pipeline and verify the artifact is published in the "Artifacts" tab.
