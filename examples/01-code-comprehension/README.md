# 01 · Code comprehension — retry-with-backoff decorator

Read `src/retry.py` (the kind of utility found inside HTTP clients and job
runners) and answer the questions below. The suite in `tests/` encodes the
verified answers — use it to check your reasoning against the reference.

## Questions

1. Why doesn't Ctrl-C (`KeyboardInterrupt`) break out of the retry loop?
2. With `max_attempts=3`, what is the maximum number of calls made to the
   wrapped function?
3. Why does the decorator need `functools.wraps`? What breaks without it?
4. When every attempt fails, what exactly does the caller receive — and how
   is the original exception preserved?

## Run

```sh
docker build -t pta-01 . && docker run --rm pta-01
# or locally: python -m pytest tests/ -v
```

## Solution

`solution/ANSWER.md` — each answer with its reasoning and the test that
verifies the claim.
