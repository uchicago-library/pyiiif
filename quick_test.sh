#!/bin/sh
echo "==> Running Tests <=="
coverage run -m py.test \
    && echo "==> Coverage <==" && \
    coverage report
echo "==> Flake8 <=="
flake8
echo "==> Done <=="
