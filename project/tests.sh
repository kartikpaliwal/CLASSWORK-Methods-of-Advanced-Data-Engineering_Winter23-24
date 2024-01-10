
python project_test.py

# Checking if the test run was successful or not.
if [ $? -eq 0 ]; then
    echo "All tests passed successfully."
else
    echo "Tests failed."
    exit 1
fi
