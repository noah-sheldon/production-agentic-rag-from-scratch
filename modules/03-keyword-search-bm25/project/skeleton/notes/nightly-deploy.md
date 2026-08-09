# nightly deploy notes
The nightly deploy runs at 3am and builds the image with the latest tag.

# python environment
Use uv for python environments. Pin versions, never rely on the system python.

# agent loop notes
An agent loop calls tools, checks results, and repeats until done.

# database backups
The database backup job runs at midnight and stores to the backups bucket.
