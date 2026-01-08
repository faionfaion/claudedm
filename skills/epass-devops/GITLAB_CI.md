# GitLab CI/CD Reference

## Pipeline Structure

```yaml
stages:
  - test      # Validation, linting, tests
  - deploy    # Deployment to environments
```

## Key Concepts

### Variables

**Global variables** (apply to all jobs):
```yaml
variables:
  DOCKER_DRIVER: "overlay2"
  DOCKER_BUILDKIT: "1"
```

**Environment-scoped variables** (set in GitLab UI):
- Navigate: Settings → CI/CD → Variables
- Use scope: `staging`, `production`, or `*` (all)

**User-input variables** (manual jobs):
```yaml
variables:
  ENVIRONMENT:
    value: "staging"
    description: "Environment name (staging/production)"
```

### Rules

**Run on merge requests to main:**
```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "main"'
```

**Manual deployment on main branch:**
```yaml
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
    when: manual
    allow_failure: false
```

**Run on push after merge:**
```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "main" && $CI_COMMIT_MESSAGE =~ /Merge branch/'
```

### Job Templates

**Test job with Docker-in-Docker:**
```yaml
test_job:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker compose -f compose-test.yml build
    - docker compose -f compose-test.yml run --rm app pytest
  after_script:
    - docker compose -f compose-test.yml down -v
```

**Deploy job with manual trigger:**
```yaml
deploy:
  stage: deploy
  environment:
    name: "$ENVIRONMENT"
  before_script:
    - chmod +x ./deploy-scripts/*.sh
  script:
    - ./deploy-scripts/deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
```

### Artifacts and Cache

**Cache pip packages:**
```yaml
cache:
  paths:
    - .cache/pip/
    - app/.pytest_cache/

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
```

**Save test logs:**
```yaml
artifacts:
  when: always
  expire_in: 1 week
  paths:
    - test_logs.txt
```

## Built-in Variables

| Variable | Description |
|----------|-------------|
| `$CI_COMMIT_BRANCH` | Branch being built |
| `$CI_COMMIT_SHA` | Full commit hash |
| `$CI_PIPELINE_URL` | URL to pipeline in UI |
| `$CI_PROJECT_NAME` | Project name |
| `$CI_PIPELINE_SOURCE` | What triggered: push, merge_request_event, web |
| `$CI_MERGE_REQUEST_TARGET_BRANCH_NAME` | Target branch for MR |
| `$CI_JOB_STATUS` | In after_script: success/failed |
| `$GITLAB_USER_NAME` | User who triggered pipeline |

## glab CLI Commands

### Pipeline Management

```bash
# Check pipeline status
glab ci status

# Run pipeline manually
glab ci run -b main --variables "ENVIRONMENT:staging"

# View pipeline logs
glab ci view

# Trace running job
glab ci trace

# List recent pipelines
glab ci list

# Retry failed pipeline
glab ci retry
```

### Variables Management

```bash
# List all variables
glab variable list

# Set global variable
glab variable set KEY "value"

# Set environment-scoped variable
glab variable set KEY "value" --scope staging

# Delete variable
glab variable delete KEY
```

### Using GitLab API

```bash
# Get project variables with scopes
glab api projects/transport%2Fepass/variables

# Trigger manual job
JOB_ID=$(glab api projects/transport%2Fepass/pipelines/$PIPELINE_ID/jobs | jq -r '.[] | select(.name=="deploy") | .id')
glab api -X POST projects/transport%2Fepass/jobs/$JOB_ID/play

# Set variable with specific scope (API)
glab api -X POST "projects/transport%2Fepass/variables" \
  -f key=SSH_HOST \
  -f value="10.21.16.20" \
  -f environment_scope=staging
```

## Common Patterns

### Logging with tee

```yaml
script:
  - |
    DEPLOY_LOG="deploy-$(date +%Y%m%d_%H%M%S).log"
    if ./deploy.sh 2>&1 | tee "$DEPLOY_LOG"; then
      rm -f "$DEPLOY_LOG"
    else
      ./notify.sh "Failed" "$DEPLOY_LOG"
      exit 1
    fi
```

### Multi-stage Docker testing

```yaml
script:
  - docker compose -f compose-test.yml build app-ci
  - docker compose -f compose-test.yml up -d postgres-ci
  - docker compose -f compose-test.yml run --rm app-ci python manage.py migrate
  - docker compose -f compose-test.yml run --rm app-ci pytest
  - docker compose -f compose-test.yml down -v
```

## Troubleshooting

### Pipeline stuck on "Pending"

**Cause:** No runner available with matching tags or `run_untagged: false`

**Solution:**
1. Register project-specific runner
2. Or add tags to job matching shared runner

### Job fails silently

**Check:**
1. `allow_failure: false` is set
2. Script uses `set -e` or checks exit codes
3. after_script runs regardless of job status

### Variables not available

**Check:**
1. Variable scope matches environment
2. Variable is not masked for use in scripts
3. Protected variables only on protected branches
