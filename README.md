# gantryctl

Crane gantry scheduling and load-envelope checks for container terminals.

```
gantryctl fleet
gantryctl check --gantry postpanamax --outreach 44 --load 50
```

Exit codes: `0` lift is safe, `1` lift exceeds the envelope, `2` invalid input.
