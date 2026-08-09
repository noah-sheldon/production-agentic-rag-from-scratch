# The 3am Deploy

## What happened

A scheduled job pushed a release at 3am and the site went down. The deploy
log showed a bad configuration value that the tests had never covered.

## The fix

Rolled back in five minutes, then added a check that validates the
configuration before the deploy starts. The job now refuses to push when the
config file is wrong, and the failure is loud instead of silent.

## Lesson

Automation at 3am needs the same care as automation at 3pm: guard rails
before the action, and a rollback that is one command, not a procedure.
