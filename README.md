# bkt-service #

This is the microservice that calculates the updated bkt values for student objective pairs for the proficiency stream.

## Requirements ##

Only bottle.py and its dependencies are required for running the service itself, but everything in the requirements file
is required for running the unit and functional tests bundled in the test package. They are designed for the pytest
suite.

## Running ##

Simply running the bkt_service script once dependencies are installed is enough to get the service to run locally on
port 9991 (bottle's default).

```
$ python bkt_service.py
```

Executing the following command in the root directory runs the bundled tests.

```
$ py.test
```