# API client hangs

The api client hangs when the server is slow to answer. Add a timeout to
the client and a deadline to the server so one slow endpoint cannot
freeze the whole app.
