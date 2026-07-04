# Common Azure Pipelines Tasks — Copy Files & Publish Artifacts

> **Expert framing:** These two tasks look trivial but are the most common source of "the pipeline succeeded but the artifact is empty/wrong" bugs. Knowing exactly what each does — and the order they must run in — separates people who've actually debugged a broken release from people who copy-pasted a working YAML once.

## The Pattern: Copy Files → Publish Build Artifacts

Almost every CI pipeline that produces a deployable output follows this two-step pattern at the end of the Build stage:

1. **Copy Files** — gather exactly the files you want to ship (compiled output, config templates, scripts) from wherever they landed during the build, into one staging folder.
2. **Publish Build Artifacts** (or the newer `PublishPipelineArtifact@1`) — take that staging folder and upload it as a named artifact attached to this pipeline run, so later stages (or a human) can download it.

### Copy Files Task

```yaml
- task: CopyFiles@2
  displayName: 'Copy Files to Artifact Staging Directory'
  inputs:
    SourceFolder: '$(System.DefaultWorkingDirectory)/dist'   # Where to copy FROM
    Contents: '**'                                            # Which files (glob pattern)
    TargetFolder: '$(Build.ArtifactStagingDirectory)'         # Where to copy TO
    CleanTargetFolder: true                                   # Wipe target first (avoid stale files)
```

**Expert insight:** `$(Build.ArtifactStagingDirectory)` is a predefined, temporary variable pointing at a clean folder created fresh for each pipeline run specifically for staging what will be published — using it (rather than an arbitrary folder) is the convention every Microsoft-provided task and template expects. `CleanTargetFolder: true` matters more than it looks: without it, files from a previous local run (on a self-hosted agent) or a previous copy step earlier in the same pipeline can silently linger and get published alongside your intended files.

### Publish Build Artifacts Task

```yaml
- task: PublishBuildArtifacts@1
  displayName: 'Publish Artifact'
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'                # Name consumers will reference to download this
    publishLocation: 'Container'        # Container = Azure Pipelines storage (most common)
```

```yaml
# Modern equivalent — faster, recommended for new pipelines
- task: PublishPipelineArtifact@1
  displayName: 'Publish Pipeline Artifact'
  inputs:
    targetPath: '$(Build.ArtifactStagingDirectory)'
    artifact: 'drop'
    publishLocation: 'pipeline'
```

**Expert insight — `PublishBuildArtifacts@1` vs `PublishPipelineArtifact@1`:** the newer `PublishPipelineArtifact@1` task is built on the Pipeline Artifacts backend (faster upload/download, better performance at scale) and is Microsoft's current recommendation for new pipelines. `PublishBuildArtifacts@1` still works and is common in older/Classic pipelines but is effectively legacy. If you're writing a new YAML pipeline today, default to `PublishPipelineArtifact@1` unless you have a specific reason (like Release-pipeline/Classic compatibility) to use the older task.

### Consuming the Artifact in a Later Stage

```yaml
- task: DownloadPipelineArtifact@2
  displayName: 'Download Artifact'
  inputs:
    artifact: 'drop'
    path: '$(Pipeline.Workspace)/drop'
```

## Common Pitfalls & Expert Tips

- **Copying from the wrong source folder.** A build tool might output to `dist/`, `build/`, `bin/Release/`, or `out/` depending on the stack — verify the actual output path rather than assuming; this is the #1 cause of "Publish Artifact succeeded but the artifact is empty."
- **Forgetting `CleanTargetFolder: true`** on self-hosted agents, where workspace state can persist between runs — leads to publishing stale or duplicate files.
- **Publishing the entire repository instead of just build output** (`Contents: '**'` from the repo root instead of the build output folder) — bloats artifact size and can accidentally leak source code, `.git` internals, or `.env` files into a deployable artifact.
- **Mismatched artifact names between the publish step and the download step.** `ArtifactName`/`artifact` in the publish task must exactly match what the consuming `Download...` task requests — a typo here fails silently with "artifact not found" rather than a helpful compile-time error.
- **Not distinguishing `Container` vs `FilePath` publish location.** `Container` uploads into Azure Pipelines' own storage (the common, portable choice). `FilePath` copies to a UNC path instead — only useful if you specifically need artifacts on a particular shared file server, and it ties the pipeline to that network location's availability.

## Expert Interview Q&A

**Q: Why does a pipeline sometimes report success even though the published artifact is missing expected files?**
`CopyFiles`/`Publish` tasks don't fail just because zero files matched a glob pattern in some configurations — if the `Contents` pattern or `SourceFolder` path is wrong, the step can complete "successfully" having copied nothing. Always verify by checking the actual artifact contents (via the Pipeline run's Artifacts tab) rather than trusting a green checkmark alone, especially after changing build tool output paths.

**Q: What's the difference between `PublishBuildArtifacts@1` and `PublishPipelineArtifact@1`, and which should a new pipeline use?**
Both publish an artifact for later stages/downloads, but `PublishPipelineArtifact@1` uses the newer, faster Pipeline Artifacts storage backend and is Microsoft's current recommendation. `PublishBuildArtifacts@1` is the older task, still functional and common in legacy/Classic pipelines, but offers no advantage for new YAML pipelines — default to the newer task unless compatibility with older tooling requires otherwise.

**Q: Why stage files into `$(Build.ArtifactStagingDirectory)` instead of publishing directly from the build output folder?**
Staging lets you assemble exactly the right set of files — combining compiled output with additional files (README, config templates, deployment scripts) that don't live in the same folder the build tool wrote to — into one clean location before publishing. It also gives you a single, predictable, pipeline-managed location to clean and control, rather than publishing an arbitrary folder that might contain build tool cache files or other unwanted artifacts.
