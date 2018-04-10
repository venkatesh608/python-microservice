#!/usr/bin/env python
import json
import logging
import functools
from bottle import app, route, run, request, response, abort
from functools import reduce

logging.basicConfig(filename='bkt_outcome_unwind.log',
                    format='%(levelname)s:%(asctime)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


bkt_app = app()

@route('/')
def index():
    return '<pre>%s</pre>' % 'BKT Outcome Unwind - ready to go!!!'

#####################################################################
#
# Pipeline Operation API Implementation
#
#####################################################################


@route('/bkt_service/unwind', method='POST')
def processPipelineOperation():

    result = []

    # Read JSON from previous pipeline operation
    data = request.body.read().decode("utf-8")

    if not data:
        abort(400, 'No data received')

    jsonData = json.loads(data)

    # Loop through each JSON record and apply the Unwrapping Function to it
    for record in jsonData:
        for item in applyModel(record):
            result.append(item)

    # return data
    response.content_type = 'application/json'
    return json.dumps(result)

#####################################################################
#
# Unwrapping Function
#
#####################################################################


def scorelessthanone (score):
    if score is None or score <= 0:
        score = 0
    else:
        score = score

    return score


def applyModel(record):
    # Check incoming outcome event is a student event
    if not reduce(lambda m, n: m or n, ["learner" in _.lower() for _ in record["event"]["actor"]["roles"]]):
        raise InternalAssertionError("Event lacks Learner role", 21)

    result = []
    for question in record["event"]["generated"]["itemResults"]:
       result.append(
            {
                "question": {
                    "studentId": record["event"]["actor"]["@id"],
                    "questionId": question["question_reference"],
                    "sequenceNumber": question["sequenceNumber"],
                    "score": scorelessthanone(question["score"]),
                    "maxScore": question["max_score"] if question["max_score"] is not None and question["max_score"] > 0 else 0,
                    "classroomId": record["event"]["group"]["@id"],
                    "assessmentId": record["event"]["object"]["extensions"]["assessmentId"],
                    "assessmentType": record["event"]["object"]["extensions"]["assessmentType"]
                },
                    "learnositySessionId": record["event"]["object"]["@id"],
                    "learnosityUserId": record["event"]["group"]["extensions"]["contextId"],
                    "assessmentAttempt":record["event"]["object"]["count"] if "count" in record["event"]["object"] else 0,
                    "courseOfferingId":record["event"]["group"]["extensions"]["CourseOfferingId"],
                    "eventSubmitTime":record["event"]["eventTime"] if "eventTime" in record["event"] else None,
                    "assessmentStartTime": record["event"]["object"]["startedAtTime"] if "startedAtTime" in record["event"]["object"] else None,
                    "assessmentEndTime":record["event"]["object"]["endedAtTime"] if "endedAtTime" in record["event"]["object"] else None,
                    "questionType":question["question_type"],
                    "itemReference":question["item_reference"]
            }
        )

    return result

# Start our bottle web server
if __name__ == "__main__":
    # Start our bottle web server
    run(host='0.0.0.0', port=9998)