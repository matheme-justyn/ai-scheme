.PHONY: help build run test test-coverage lint clean

# Variables
APP_NAME=app
BUILD_DIR=bin
MAIN_PATH=./cmd/app

# Colors for output
CYAN=\033[0;36m
NC=\033[0m # No Color

help: ## Show this help message
	@echo '${CYAN}Usage:${NC}'
	@echo '  make ${CYAN}<target>${NC}'
	@echo ''
	@echo '${CYAN}Targets:${NC}'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${CYAN}%-15s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the application
	@echo "${CYAN}Building...${NC}"
	@mkdir -p ${BUILD_DIR}
	@go build -o ${BUILD_DIR}/${APP_NAME} ${MAIN_PATH}
	@echo "${CYAN}Build complete: ${BUILD_DIR}/${APP_NAME}${NC}"

run: ## Run the application
	@echo "${CYAN}Running...${NC}"
	@go run ${MAIN_PATH}

test: ## Run tests
	@echo "${CYAN}Running tests...${NC}"
	@go test -v ./...

test-coverage: ## Run tests with coverage
	@echo "${CYAN}Running tests with coverage...${NC}"
	@go test -v -race -coverprofile=coverage.txt -covermode=atomic ./...
	@go tool cover -html=coverage.txt -o coverage.html
	@echo "${CYAN}Coverage report generated: coverage.html${NC}"

lint: ## Run linters
	@echo "${CYAN}Running linters...${NC}"
	@golangci-lint run ./...

fmt: ## Format code
	@echo "${CYAN}Formatting code...${NC}"
	@go fmt ./...
	@goimports -w .

clean: ## Clean build artifacts
	@echo "${CYAN}Cleaning...${NC}"
	@rm -rf ${BUILD_DIR}
	@rm -f coverage.txt coverage.html
	@echo "${CYAN}Clean complete${NC}"

deps: ## Download dependencies
	@echo "${CYAN}Downloading dependencies...${NC}"
	@go mod download
	@go mod tidy

.DEFAULT_GOAL := help
