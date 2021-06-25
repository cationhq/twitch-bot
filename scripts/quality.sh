set -e
set -x

APP_PATH=app
UNIT_TEST_PATH=tests/unit

# Remove unsed variables and imports.
poetry run autoflake \
  --remove-all-unused-imports \
  --recursive \
  --remove-unused-variables \
  --in-place $APP_PATH $UNIT_TEST_PATH

# Sort imports from app and unit tests.
poetry run isort $APP_PATH $UNIT_TEST_PATH

# Pydocstyle:
#   - D101: Missing docstring in public class.
#   - D102: Missing docstring in public method.
#   - D103: Missing docstring in public function.
poetry run pydocstyle \
  --select=D101,D102,D103 \
  $APP_PATH -v

# Cyclomatic Complexity
poetry run radon cc \
  $APP_PATH \
  --show-complexity \
  --total-average

# Maintainability Index
poetry run radon mi \
  $APP_PATH

# Lint
poetry run black --check $APP_PATH $UNIT_TEST_PATH -v
