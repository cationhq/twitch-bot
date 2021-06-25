set -e
set -x

poetry run coverage run -m ward
poetry run coverage report
poetry run coverage xml
