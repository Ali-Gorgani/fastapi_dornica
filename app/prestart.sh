#!/bin/bash

echo "Running Alembic upgrade"
alembic upgrade head

echo "Seeding database with fake users"
# Use the Python command to execute the seed_users_with_hashed_passwords function
python -c 'from app.fake_users import seed_users_with_hashed_passwords; seed_users_with_hashed_passwords()'
