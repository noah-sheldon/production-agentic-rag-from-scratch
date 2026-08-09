# Nightly Deploy

The nightly deploy runs at 3am. It builds the image, runs migrations, then restarts the server.

Deploy failures usually come from missing environment variables.
