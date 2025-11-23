#!/bin/bash

echo "========================================="
echo "SMOKE TESTS - Infrastructure as Code"
echo "========================================="
echo ""

START_TIME=$(date +%s)
MODULES=("network" "compute" "storage" "firewall" "dns")
FAILED=0
PASSED=0

for module in "${MODULES[@]}"; do
    echo "Testing module: $module"
    echo "-----------------------------------------"
    
    cd "modules/$module" || exit
    
    # Test 1: Format check
    echo "  [1/4] Checking format..."
    if terraform fmt -check > /dev/null 2>&1; then
        echo "    ✓ Format OK"
        ((PASSED++))
    else
        echo "    ✗ Format FAILED"
        ((FAILED++))
    fi
    
    # Test 2: Validation
    echo "  [2/4] Validating syntax..."
    terraform init -backend=false > /dev/null 2>&1
    if terraform validate > /dev/null 2>&1; then
        echo "    ✓ Validation OK"
        ((PASSED++))
    else
        echo "    ✗ Validation FAILED"
        ((FAILED++))
    fi
    
    # Test 3: Plan (dry-run)
    echo "  [3/4] Running plan..."
    if timeout 10s terraform plan -refresh=false -out=smoke.tfplan > /dev/null 2>&1; then
        echo "    ✓ Plan OK"
        ((PASSED++))
    else
        echo "    ✗ Plan FAILED or TIMEOUT"
        ((FAILED++))
    fi
    
    # Test 4: Contract check (outputs exist)
    echo "  [4/4] Checking contract..."
    OUTPUT_COUNT=$(grep -c "^output" outputs.tf 2>/dev/null || echo "0")
    if [ "$OUTPUT_COUNT" -gt 0 ]; then
        echo "    ✓ Contract OK ($OUTPUT_COUNT outputs defined)"
        ((PASSED++))
    else
        echo "    ✗ Contract FAILED (no outputs)"
        ((FAILED++))
    fi
    
    # Cleanup
    rm -f smoke.tfplan .terraform.lock.hcl
    rm -rf .terraform
    
    cd ../.. || exit
    echo ""
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "========================================="
echo "SMOKE TEST SUMMARY"
echo "========================================="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Duration: ${DURATION}s"
echo ""

if [ $FAILED -gt 0 ]; then
    exit 1
fi