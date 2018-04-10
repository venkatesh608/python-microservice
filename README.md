# bkt-service #

This is the microservice that calculates the updated bkt values for student objective pairs for the proficiency stream.

## Requirements ##

Only bottle.py and its dependencies are required for running the service itself, but everything in the requirements file
is required for running the unit and functional tests bundled in the test package. They are designed for the pytest
suite.

## Running ##


```
$ pip install -r requirements.txt
$ python service/unwind_array.py
```