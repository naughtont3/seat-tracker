#!/bin/bash
# Quick test script for the work location tracker

# Avoid using any existing envvar set data dirs
unset SEAT_TRACKER_DATA_DIR

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Change to the parent directory (project root)
cd "$SCRIPT_DIR/.."

# Create temporary test data directory
TEST_DATA_DIR="$(mktemp -d)"
trap "rm -rf '$TEST_DATA_DIR'" EXIT

echo "=== Work Location Tracker Test ==="
echo "Using temporary data directory: $TEST_DATA_DIR"
echo ""

echo "1. Setting some test data..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --force --home 2025-10-14
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --force --lab 2025-10-15
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --force --travel 2025-10-17
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --force --vacation 2025-10-18
echo ""

echo "2. Getting designation for specific dates..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --get 2025-10-14
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --get 2025-10-15
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --get 2025-10-17
echo ""

echo "3. Displaying calendar..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --calendar
echo ""

echo "4. Testing delete functionality..."
echo "4a. Attempting to delete non-existent date (should fail)..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --force --delete 2025-10-20
echo ""
echo "4b. Deleting existing entry for 2025-10-17..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --force --delete 2025-10-17
echo ""
echo "4c. Verifying deletion (should show no entry)..."
cat "$TEST_DATA_DIR/2025.log" | grep "2025-10-17" || echo "✓ Entry successfully deleted"
echo ""

echo "5. Validating data..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --validate
echo ""

echo "6. Viewing stats..."
python3 seat-tracker.py --data-dir "$TEST_DATA_DIR" --stats 30
echo ""

echo "=== Test Complete ==="
echo "Temporary data directory will be cleaned up automatically"
