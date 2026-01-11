---
name: epass-devops
user-invocable: false
description: "E-Pass CI/CD and DevOps knowledge base. Use for deploy, pipeline, GitLab, runner, docker, ssh, staging, production questions. Triggers on deploy, CI/CD, pipeline, GitLab, docker, ssh."
---

# E-Pass DevOps - CI/CD Knowledge Base

**IMPORTANT: Communicate with the user in Ukrainian.**

## Overview

This skill contains comprehensive knowledge about CI/CD infrastructure for the Transport project (E-Pass and related services) at EasyPay.

---

## Environment Architecture

### Servers

| Environment | Purpose | Host | SSH Port | User |
|-------------|---------|------|----------|------|
| **dev** | Development, GitLab Runner | epass-deploy (this host) | local | - |
| **staging** | Testing, QA | 10.21.16.20 | 22 | epass |
| **production** | Live system | 77.222.150.186 | 12223 | - |

### GitLab Runner

- **Location**: epass-deploy host (dev environment)
- **Executor**: shell
- **Registered runners**:
  - `epass-deploy` (id: 6) - for transport/epass project
  - `ai-agent-deploy` - for transport/ai-agent project
- **Config**: `/etc/gitlab-runner/config.toml`

### Database

| Environment | Host | Port | Database | User |
|-------------|------|------|----------|------|
| staging | 10.21.16.22 | 5432 | epass | epass_app |
| production | espostgresql.es.baza.ua | 5432 | epass | epass_app |

---

## GitLab Projects

### transport/epass

Main E-Pass application.

**CI/CD Pipeline Stages:**
1. `test` - MR validation (flake8, pytest, coverage)
2. `deploy` - Manual deployment to staging/production

**Key Jobs:**
- `mr_test_and_validation` - Runs on MR to main
- `merged_notification` - Sends Telegram when merged
- `deploy` - Manual deploy with ENVIRONMENT variable

### transport/ai-agent

AI Agent for monitoring and automation.

**CI/CD Pipeline:**
- Single `deploy` stage with manual trigger
- Builds Docker image locally
- Transfers to target server via SCP
- Uses same SSH credentials as epass

---

## Deployment Process

### Deploy Script Flow (deploy.sh)

1. **create_env.sh** - Generate .env from CI/CD variables
2. **send_notification.sh** - Telegram: "Deploy started"
3. **docker compose build** - Build containers
4. **docker save** - Save images to .tar files
5. **SCP upload** - Transfer to target server
6. **docker load** - Load images on target
7. **docker compose down** - Stop old containers
8. **docker compose up -d** - Start new containers
9. **Telegram notification** - Success/failure

### Required CI/CD Variables

**Global (scope: *):**
- `TELEGRAM_TOKEN` - Bot token for notifications
- `TELEGRAM_CHAT_ID` - Chat for deploy notifications
- `SECRET_KEY` - Django secret
- `POSTGRES_DB` - Database name (epass)

**Per Environment (scope: staging/production):**
- `SSH_HOST` - Target server IP
- `SSH_PORT` - SSH port
- `SSH_USER` - SSH username
- `SSH_PRIVATE_KEY` - SSH key for authentication
- `REMOTE_PASSWORD` - Password for sshpass (if needed)
- `POSTGRES_HOST` - Database host
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `EXTERNAL_HOST` - Public hostname

**Agent-specific:**
- `AGENT_TELEGRAM_TOKEN` - Agent bot token
- `AGENT_TELEGRAM_CHAT` - Agent chat ID
- `GITLAB_TOKEN` - For GitLab API access
- `OPENAI_API_KEY` - For AI features
- `EPASS_REPO_URL` - Repository URL
- `AGENT_ERROR_SECRET` - Error webhook secret

---

## Telegram Notifications

### Bot Tokens

| Bot | Token | Purpose |
|-----|-------|---------|
| epass server | 6675477703:AAHw-... | Deploy notifications |
| dev agentbot | 8401567752:AAHRq... | Agent operations |

### Chat IDs

| Chat | ID | Purpose |
|------|-----|---------|
| epass server | -4034521193 | Main server notifications |
| EPass звітність | -4790416095 | Reports |
| epass dev agentbot | -4836553775 | Agent dev/test |
| RuslanFaion | 5088870093 | Private |

### Notification Scripts

- `send_notification.sh` - Basic message/file send
- `mr_notification.sh` - MR pipeline status (start/success/failure)
- `merged_notification.sh` - Celebratory merge notification

---

## Docker Infrastructure

### E-Pass Containers

| Container | Purpose |
|-----------|---------|
| app | Django application |
| nginx | Web server, SSL |
| rabbitmq | Message queue |
| celery | Task worker |
| celery-beat | Scheduled tasks |
| agent | AI Agent |
| postgres | Database (external or container) |

### Networks

- `epass_default` - Main network for all containers

### Volumes

- `media` - Uploaded files
- `static_files` - Static assets
- `ssl_certs` - SSL certificates
- `rabbitmq_data` - Queue data
- `agent_data` - Agent persistent data
- `agent_claude` - Claude configuration

---

## CLI Commands

### GitLab CLI (glab)

```bash
# List CI/CD variables
glab variable list --repo transport/epass

# Set variable
glab variable set KEY "value" --repo transport/epass --scope staging

# Run pipeline
glab ci run --repo transport/epass -b main --variables "ENVIRONMENT:staging"

# Check pipeline status
glab ci status --repo transport/epass

# Trigger manual job
JOB_ID=$(glab api projects/transport%2Fepass/pipelines/PIPELINE_ID/jobs | jq -r '.[] | select(.name=="deploy") | .id')
glab api -X POST projects/transport%2Fepass/jobs/$JOB_ID/play
```

### GitLab Runner

```bash
# List runners
sudo gitlab-runner list

# Register new runner
sudo gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.easypay.ua/" \
  --registration-token "TOKEN" \
  --executor "shell" \
  --description "runner-name" \
  --run-untagged="true" \
  --locked="true"

# Restart runner
sudo systemctl restart gitlab-runner
```

### Docker Operations

```bash
# Check container status
docker ps --filter "name=ai-agent"

# View logs
docker logs ai-agent --tail 50

# Network inspection
docker network inspect epass_default

# Manual image build/load
docker build -t ai-agent:latest .
docker save -o image.tar ai-agent:latest
docker load -i image.tar
```

---

## Troubleshooting

### Pipeline Stuck on "Pending"

**Cause:** Shared runners have `run_untagged: false`

**Solution:**
1. Register project-specific runner
2. Or add tags matching shared runner tags

### SSH Connection Failed

**Cause:** Missing or incorrect SSH credentials

**Check:**
```bash
# Verify variables
glab api projects/transport%2Fepass/variables | jq '.[] | select(.key | test("SSH"))'

# Test connection manually
ssh -i key -p PORT USER@HOST
```

### Docker Build Fails

**Cause:** Usually missing dependencies or wrong context

**Solution:**
1. Check Dockerfile syntax
2. Verify build context path
3. Check for missing files in .dockerignore

### Telegram Notifications Not Sending

**Check:**
1. TELEGRAM_TOKEN and TELEGRAM_CHAT_ID set
2. SILENT_DEPLOY != "True"
3. Bot has access to chat

---

## Creating New Project CI/CD

### Step 1: Register Runner

```bash
# Get registration token
TOKEN=$(glab api projects/GROUP%2FPROJECT | jq -r '.runners_token')

# Register
sudo gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.easypay.ua/" \
  --registration-token "$TOKEN" \
  --executor "shell" \
  --description "project-deploy" \
  --run-untagged="true" \
  --locked="true"

sudo systemctl restart gitlab-runner
```

### Step 2: Create CI/CD Variables

Copy from epass and adjust:
- SSH_HOST, SSH_PORT, SSH_USER (per environment)
- POSTGRES_* (per environment)
- TELEGRAM_* (global)
- Project-specific variables

### Step 3: Create .gitlab-ci.yml

Use epass pattern:
- stages: test, deploy
- deploy with manual trigger
- Use deploy-scripts/

### Step 4: Create Deploy Scripts

- `deploy.sh` - Main deployment logic
- `send_notification.sh` - Telegram notifications
- `create_env.sh` - Environment file generation (if needed)

---

## Security Notes

- SSH keys stored as CI/CD variables (masked)
- Passwords stored masked
- Never commit secrets to repository
- Use `.secrets/` directory locally (gitignored)
- GitLab token in `.secrets/gitlab_access_token`
