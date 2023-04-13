.PHONY: help install run install-and-run

install:  ## Install or Update package
	chmod +x install.sh && ./install.sh

run:  ## Run pre-commit
	git add .; pre-commit run -c pre-commit.yaml

install-and-run:  ## Install package and Run pre-commit
	make install && make run

help: ## Display this help message
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help
