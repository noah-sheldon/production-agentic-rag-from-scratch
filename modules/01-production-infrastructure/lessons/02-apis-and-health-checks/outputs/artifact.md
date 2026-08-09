# Artifact — the health-check probe + why health checks exist

Use this the next time you stand up any service. Two parts: a probe you can
run from your terminal, and the explanation you will need when someone asks
"why do we need health checks?"

## Part 1 — the probe (works against any service)

```bash
# One-shot: is the service ready?
curl -s -o /dev/null -w "%{http_code}\n" localhost:8000/health
# 200 = ready, 503 = degraded, 000 = nothing listening

# Human-readable check
curl -s localhost:8000/health | python3 -m json.tool

# Loop until healthy (what an orchestrator does):
until curl -sf localhost:8000/health >/dev/null; do sleep 1; done
echo "service is ready"
```

Put the same probe inside your compose file as a `healthcheck` and
`docker compose ps` will show `healthy`/`unhealthy` for every service —
one command, whole stack.

## Part 2 — why health checks exist (say this out loud)

1. **Alive is not ready.** A process can run while its database connection is
   dead, its disk is full, or it is stuck in an infinite loop. "Is the process
   running?" answers the wrong question.
2. **Machines need a machine-readable answer.** Load balancers and
   orchestrators route traffic on status codes, not on logs. `200` means
   "send me work", `503` means "stop sending".
3. **Failures should be cheap.** The health check turns a five-minute mystery
   ("why are requests hanging?") into a one-second answer ("service says 503,
   dependency is down").
4. **It is the contract your stack runs on.** Compose, Kubernetes, and every
   monitoring tool in this course will read `/health`. Give it one shape:
   `200` + a JSON body that names the checks it ran.

## The rules of a good /health

- Check real dependencies, not "I am a process and I exist".
- Return `503` fast when degraded — never hang.
- Include the check details in the body (`{"checks": {"db": "up"}}`).
- No secrets, no heavy work — health checks run constantly.
