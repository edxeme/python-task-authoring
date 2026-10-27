EXAMPLES := $(sort $(dir $(wildcard examples/*/)))
IMAGE_PREFIX := pta

.PHONY: test test-strict solve revert

# Run every example's verification suite in its own Docker container.
# In task state, 02-bugfix and 03-feature are expected to be RED —
# the failing suite is the task's starting signal.
test:
	@for d in $(EXAMPLES); do \
		name=$$(basename $$d); \
		echo "===== $$name ====="; \
		docker build -q -t $(IMAGE_PREFIX):$$name $$d >/dev/null && \
		docker run --rm $(IMAGE_PREFIX):$$name || \
		echo "RED — suite failed for $$name (expected in task state for 02/03)"; \
	done

# Strict variant: stops at the first failing suite. Used by `solve`.
test-strict:
	@set -e; for d in $(EXAMPLES); do \
		name=$$(basename $$d); \
		echo "===== $$name ====="; \
		docker build -q -t $(IMAGE_PREFIX):$$name $$d >/dev/null; \
		docker run --rm $(IMAGE_PREFIX):$$name; \
	done

# Apply every golden patch, then prove the full matrix is green.
solve:
	git apply examples/*/solution/solution.patch
	$(MAKE) test-strict

# Return the working tree to the pristine task state.
revert:
	git apply -R examples/*/solution/solution.patch
