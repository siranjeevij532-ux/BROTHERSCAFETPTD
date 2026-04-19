#!/bin/bash
echo "Applying migrations with fake-initial (safe for existing databases)..."
python manage.py migrate --fake-initial
echo "Done!"
