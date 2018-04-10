"""
Unit and functional tests for the bkt objective unwind service.
"""

import json
from service import bkt_outcome_unwind
from webtest import TestApp as TApp  # Change alias so that pytest does not attempt to load this as a test case class
from werkzeug.debug import DebuggedApplication

app = DebuggedApplication(bkt_outcome_unwind.bkt_app)
app.catchall = False  # Now most exceptions are re-raised within bottle.
test_app = TApp(app)


def test_service_initiated():
    """
    Assert root url returns a message showing the service is ready.
    """
    assert "ready" in bkt_outcome_unwind.index()


def test_no_data():
    """
    Assert correct error message is returned when no data is supplied to the unwind url.
    """
    response = test_app.post("/bkt_service/unwind", expect_errors=True)
    assert response.status == '400 Bad Request'
    assert "No data" in response.text


def test_valid_data():
    """
    Assert calculation returns valid results with valid input data.
    """
    response = test_app.post("/bkt_service/unwind", params='''[{
       "event": {
            "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
            "@type": "http://purl.imsglobal.org/caliper/v1/OutcomeEvent",
            "actor": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "student-1462300421838-1",
              "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
              "roles": [
                "urn:lti:instrole:ims/lis/Learner"
              ]
            },
            "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#Graded",
            "object": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "attempt-1462300421838-4",
              "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
              "extensions": {
                "assessmentType": "Diagnostic Assessment",
                "assessmentId": "assessment-1462300421838-4"
              },
              "count": 1,
              "startedAtTime": "2016-05-03T21:33:41.844Z",
              "endedAtTime": "2016-05-03T22:03:41.844Z"
            },
            "generated": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "result-1462300421838-4",
              "@type": "http://purl.imsglobal.org/caliper/v1/Result",
              "assignableId": "assessment-1462300421838-4",
              "normalScore": 80,
              "totalScore": 100,
              "itemResults": [
                {
                  "@id": "item-result-1462300421838-4-1",
                  "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                  "question_type": "mcq",
                  "automarkable": 1,
                  "score": 7,
                  "max_score": 10,
                  "question_reference": "c0a3f0c8-eac7-4795-8c7a-adf98e336a7b",
                  "item_reference": "Adaptive_Item2_extract_USMOs",
                  "sequenceNumber": 1
                }
              ]
            },
            "group": {
                "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                "@id": "class-01",
                "@type": "http://purl.imsglobal.org/caliper/v1/lis/CourseOffering",
                "name": null,
                "description": null,
                "extensions": {
                  "pageNumber": null,
                  "courseCode": "course-01",
                  "calmsCourseId": "calms-course-01",
                  "lessonId": "lesson-01",
                  "platform": "D2L",
                  "classroomTypeId": "3500.0",
                  "activityId": "10",
                  "gradeLevel": "8",
                  "CourseOfferingId": "1200.0",
                  "adaptivewrapperId": "",
                  "schoolYear": "2015-20116",
                  "unitId": "3201.0",
                  "moduleId": "1110.0",
                  "courseId": "2550.0",
                  "assessmentId": "4520.0",
                  "originSystemId": "sams",
                  "businessLineId": "1300.0",
                  "contextId": "587279312bf9a9afd947ddab"
                },
                "dateCreated": null,
                "dateModified": null,
                "courseNumber": null,
                "academicSession": null,
                "subOrganizationOf": {
                  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                  "@id": "1001.0",
                  "@type": "http://purl.imsglobal.org/caliper/v1/w3c/Organization",
                  "name": null,
                  "description": null,
                  "extensions": {},
                  "dateCreated": null,
                  "dateModified": null,
                  "subOrganizationOf": null
                }
            },
            "eventTime": "2017-01-09T14:21:00Z"
        }
      }
    ]''')
    assert response.status == '200 OK'
    assert len(response.json) == 1
    assert response.json[0]["error"]["code"] == 0


def test_teacher_role():
    """
    Assert calculation returns valid results with valid input data.
    """
    response = test_app.post("/bkt_service/unwind", params='''[{
       "event": {
            "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
            "@type": "http://purl.imsglobal.org/caliper/v1/OutcomeEvent",
            "actor": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "student-1462300421838-1",
              "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
              "roles": [
                "urn:lti:instrole:ims/lis/Teacher"
              ]
            },
            "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#Graded",
            "object": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "attempt-1462300421838-4",
              "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
              "extensions": {
                "assessmentType": "Diagnostic Assessment",
                "assessmentId": "assessment-1462300421838-4"
              },
              "count": 1,
              "startedAtTime": "2016-05-03T21:33:41.844Z",
              "endedAtTime": "2016-05-03T22:03:41.844Z"
            },
            "generated": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "result-1462300421838-4",
              "@type": "http://purl.imsglobal.org/caliper/v1/Result",
              "assignableId": "assessment-1462300421838-4",
              "normalScore": 80,
              "totalScore": 100,
              "itemResults": [
                {
                  "@id": "item-result-1462300421838-4-1",
                  "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                  "question_type": "mcq",
                  "automarkable": 1,
                  "score": 7,
                  "max_score": 10,
                  "question_reference": "c0a3f0c8-eac7-4795-8c7a-adf98e336a7b",
                  "item_reference": "Adaptive_Item2_extract_USMOs",
                  "sequenceNumber": 1
                }
              ]
            },
            "group": {
                "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                "@id": "class-01",
                "@type": "http://purl.imsglobal.org/caliper/v1/lis/CourseOffering",
                "name": null,
                "description": null,
                "extensions": {
                  "pageNumber": null,
                  "courseCode": "course-01",
                  "calmsCourseId": "calms-course-01",
                  "lessonId": "lesson-01",
                  "platform": "D2L",
                  "classroomTypeId": "3500.0",
                  "activityId": "10",
                  "gradeLevel": "8",
                  "CourseOfferingId": "1200.0",
                  "adaptivewrapperId": "",
                  "schoolYear": "2015-20116",
                  "unitId": "3201.0",
                  "moduleId": "1110.0",
                  "courseId": "2550.0",
                  "assessmentId": "4520.0",
                  "originSystemId": "sams",
                  "businessLineId": "1300.0",
                  "contextId": "587279312bf9a9afd947ddab"
                },
                "dateCreated": null,
                "dateModified": null,
                "courseNumber": null,
                "academicSession": null,
                "subOrganizationOf": {
                  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                  "@id": "1001.0",
                  "@type": "http://purl.imsglobal.org/caliper/v1/w3c/Organization",
                  "name": null,
                  "description": null,
                  "extensions": {},
                  "dateCreated": null,
                  "dateModified": null,
                  "subOrganizationOf": null
                }
            },
            "eventTime": "2017-01-09T14:21:00Z"
        }
      }
    ]''')
    assert response.status == '200 OK'
    assert len(response.json) == 1
    #assert response.json[0]["error"]["code"] == 21
    #assert "role" in response.json[0]["error"]["message"]


def test_valid_data_null_scores():
    """
    Assert calculation returns valid results with valid input data.
    """
    response = test_app.post("/bkt_service/unwind", params='''[{
       "event": {
            "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
            "@type": "http://purl.imsglobal.org/caliper/v1/OutcomeEvent",
            "actor": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "student-1462300421838-1",
              "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
              "roles": [
                "urn:lti:instrole:ims/lis/Learner"
              ]
            },
            "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#Graded",
            "object": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "attempt-1462300421838-4",
              "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
              "extensions": {
                "assessmentType": "Diagnostic Assessment",
                "assessmentId": "assessment-1462300421838-4"
              },
              "count": 1,
              "startedAtTime": "2016-05-03T21:33:41.844Z",
              "endedAtTime": "2016-05-03T22:03:41.844Z"
            },
            "generated": {
              "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
              "@id": "result-1462300421838-4",
              "@type": "http://purl.imsglobal.org/caliper/v1/Result",
              "assignableId": "assessment-1462300421838-4",
              "normalScore": 80,
              "totalScore": 100,
              "itemResults": [
                {
                  "@id": "item-result-1462300421838-4-1",
                  "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                  "question_type": "mcq",
                  "automarkable": 1,
                  "score": null,
                  "max_score": 10,
                  "question_reference": "c0a3f0c8-eac7-4795-8c7a-adf98e336a7b",
                  "item_reference": "Adaptive_Item2_extract_USMOs",
                  "sequenceNumber": 1
                }
              ]
            },
            "group": {
                "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                "@id": "class-01",
                "@type": "http://purl.imsglobal.org/caliper/v1/lis/CourseOffering",
                "name": null,
                "description": null,
                "extensions": {
                  "pageNumber": null,
                  "courseCode": "course-01",
                  "calmsCourseId": "calms-course-01",
                  "lessonId": "lesson-01",
                  "platform": "D2L",
                  "classroomTypeId": "3500.0",
                  "activityId": "10",
                  "gradeLevel": "8",
                  "CourseOfferingId": "1200.0",
                  "adaptivewrapperId": "",
                  "schoolYear": "2015-20116",
                  "unitId": "3201.0",
                  "moduleId": "1110.0",
                  "courseId": "2550.0",
                  "assessmentId": "4520.0",
                  "originSystemId": "sams",
                  "businessLineId": "1300.0",
                  "contextId": "587279312bf9a9afd947ddab"
                },
                "dateCreated": null,
                "dateModified": null,
                "courseNumber": null,
                "academicSession": null,
                "subOrganizationOf": {
                  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                  "@id": "1001.0",
                  "@type": "http://purl.imsglobal.org/caliper/v1/w3c/Organization",
                  "name": null,
                  "description": null,
                  "extensions": {},
                  "dateCreated": null,
                  "dateModified": null,
                  "subOrganizationOf": null
                }
            },
            "eventTime": "2017-01-09T14:21:00Z"
        }
      }
    ]''')
    assert response.status == '200 OK'
    assert len(response.json) == 1
    assert (response.json[0]["question"]["score"] == 0)

def test_multiple_data():
    """
    Assert calculation returns valid results with valid input data.
    """
    response = test_app.post("/bkt_service/unwind", params='''[{
        "event": {
             "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
             "@type": "http://purl.imsglobal.org/caliper/v1/OutcomeEvent",
             "actor": {
               "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
               "@id": "student-1462300421838-1",
               "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
               "roles": [
                 "urn:lti:instrole:ims/lis/Learner"
                 ]
             },
             "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#Graded",
             "object": {
               "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
               "@id": "attempt-1462300421838-4",
               "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
               "extensions": {
                 "assessmentType": "Diagnostic Assessment",
                 "assessmentId": "assessment-1462300421838-4"
               },
               "count": 1,
               "startedAtTime": "2016-05-03T21:33:41.844Z",
               "endedAtTime": "2016-05-03T22:03:41.844Z"
             },
             "generated": {
               "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
               "@id": "result-1462300421838-4",
               "@type": "http://purl.imsglobal.org/caliper/v1/Result",
               "assignableId": "assessment-1462300421838-4",
               "normalScore": 80,
               "totalScore": 100,
               "itemResults": [
                 {
                   "@id": "item-result-1462300421838-4-1",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 1,
                   "score": 7,
                   "max_score": 10,
                   "question_reference": "c0a3f0c8-eac7-4795-8c7a-adf98e336a7b",
                   "item_reference": "Adaptive_Item2_extract_USMOs",
                   "sequenceNumber": 1
                 },
                 {
                   "@id": "item-result-1462300421838-4-2",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 0,
                   "score": 8,
                   "max_score": 10,
                   "question_reference": "5ee295ad-5e8b-413f-9fe6-87038e8e6e42",
                   "item_reference": "Adaptive_Item4_extract_USMOs",
                   "sequenceNumber": 2
                 },
                 {
                   "@id": "item-result-1462300421838-4-3",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 1,
                   "score": 7,
                   "max_score": 10,
                   "question_reference": "047c4139-a64b-4596-8169-7a294d0c69d7",
                   "item_reference": "Adaptive_Item3_extract_USMOs",
                   "sequenceNumber": 3
                 },
                 {
                   "@id": "item-result-1462300421838-4-4",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 0,
                   "score": 10,
                   "max_score": 10,
                   "question_reference": "b7cc7839-63d4-4e12-93ce-f25fad380aaa",
                   "item_reference": "Adaptive_Item1_extract_USMOs",
                   "sequenceNumber": 4
                 }
               ]
             },
             "group": {
                "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                "@id": "class-01",
                "@type": "http://purl.imsglobal.org/caliper/v1/lis/CourseOffering",
                "name": null,
                "description": null,
                "extensions": {
                  "pageNumber": null,
                  "courseCode": "course-01",
                  "calmsCourseId": "calms-course-01",
                  "lessonId": "lesson-01",
                  "platform": "D2L",
                  "classroomTypeId": "3500.0",
                  "activityId": "10",
                  "gradeLevel": "8",
                  "CourseOfferingId": "1200.0",
                  "adaptivewrapperId": "",
                  "schoolYear": "2015-20116",
                  "unitId": "3201.0",
                  "moduleId": "1110.0",
                  "courseId": "2550.0",
                  "assessmentId": "4520.0",
                  "originSystemId": "sams",
                  "businessLineId": "1300.0",
                  "contextId": "587279312bf9a9afd947ddab"
                },
                "dateCreated": null,
                "dateModified": null,
                "courseNumber": null,
                "academicSession": null,
                "subOrganizationOf": {
                  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                  "@id": "1001.0",
                  "@type": "http://purl.imsglobal.org/caliper/v1/w3c/Organization",
                  "name": null,
                  "description": null,
                  "extensions": {},
                  "dateCreated": null,
                  "dateModified": null,
                  "subOrganizationOf": null
                }
              },
              "eventTime": "2017-01-09T14:21:00Z"
         }
       }
     ]''')
    assert response.status == '200 OK'
    assert len(response.json) == 4

#Evaluate when score is less than zero, put score in zero
def test_score_less_than_one():
    """
    Assert calculation returns valid results with valid input data.
    """
    response = test_app.post("/bkt_service/unwind", params='''[{
        "event": {
             "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
             "@type": "http://purl.imsglobal.org/caliper/v1/OutcomeEvent",
             "actor": {
               "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
               "@id": "student-1462300421838-1",
               "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
               "roles": [
                 "urn:lti:instrole:ims/lis/Learner"
                 ]
             },
             "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#Graded",
             "object": {
               "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
               "@id": "attempt-1462300421838-4",
               "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
               "extensions": {
                 "assessmentType": "Diagnostic Assessment",
                 "assessmentId": "assessment-1462300421838-4"
               },
               "count": 1,
               "startedAtTime": "2016-05-03T21:33:41.844Z",
               "endedAtTime": "2016-05-03T22:03:41.844Z"
             },
             "generated": {
               "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
               "@id": "result-1462300421838-4",
               "@type": "http://purl.imsglobal.org/caliper/v1/Result",
               "assignableId": "assessment-1462300421838-4",
               "normalScore": 80,
               "totalScore": 100,
               "itemResults": [
                 {
                   "@id": "item-result-1462300421838-4-1",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 1,
                   "score": 0,
                   "max_score": 10,
                   "question_reference": "c0a3f0c8-eac7-4795-8c7a-adf98e336a7b",
                   "item_reference": "Adaptive_Item2_extract_USMOs",
                   "sequenceNumber": 1
                 },
                 {
                   "@id": "item-result-1462300421838-4-2",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 0,
                   "score": -1,
                   "max_score": 10,
                   "question_reference": "5ee295ad-5e8b-413f-9fe6-87038e8e6e42",
                   "item_reference": "Adaptive_Item4_extract_USMOs",
                   "sequenceNumber": 2
                 },
                 {
                   "@id": "item-result-1462300421838-4-3",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 1,
                   "score": 1,
                   "max_score": 10,
                   "question_reference": "047c4139-a64b-4596-8169-7a294d0c69d7",
                   "item_reference": "Adaptive_Item3_extract_USMOs",
                   "sequenceNumber": 3
                 },
                 {
                   "@id": "item-result-1462300421838-4-4",
                   "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                   "question_type": "mcq",
                   "automarkable": 0,
                   "score": -1,
                   "max_score": 10,
                   "question_reference": "b7cc7839-63d4-4e12-93ce-f25fad380aaa",
                   "item_reference": "Adaptive_Item1_extract_USMOs",
                   "sequenceNumber": 4
                 }
               ]
             },
             "group": {
                "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                "@id": "class-01",
                "@type": "http://purl.imsglobal.org/caliper/v1/lis/CourseOffering",
                "name": null,
                "description": null,
                "extensions": {
                  "pageNumber": null,
                  "courseCode": "course-01",
                  "calmsCourseId": "calms-course-01",
                  "lessonId": "lesson-01",
                  "platform": "D2L",
                  "classroomTypeId": "3500.0",
                  "activityId": "10",
                  "gradeLevel": "8",
                  "CourseOfferingId": "1200.0",
                  "adaptivewrapperId": "",
                  "schoolYear": "2015-20116",
                  "unitId": "3201.0",
                  "moduleId": "1110.0",
                  "courseId": "2550.0",
                  "assessmentId": "4520.0",
                  "originSystemId": "sams",
                  "businessLineId": "1300.0",
                  "contextId": "587279312bf9a9afd947ddab"
                },
                "dateCreated": null,
                "dateModified": null,
                "courseNumber": null,
                "academicSession": null,
                "subOrganizationOf": {
                  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
                  "@id": "1001.0",
                  "@type": "http://purl.imsglobal.org/caliper/v1/w3c/Organization",
                  "name": null,
                  "description": null,
                  "extensions": {},
                  "dateCreated": null,
                  "dateModified": null,
                  "subOrganizationOf": null
                }
              },
              "eventTime": "2017-01-09T14:21:00Z"
         }
       }
     ]''')
    assert response.status == '200 OK'
    data = response.json
    score = data[0]["question"]["score"]
    score1 = data[1]["question"]["score"]
    score2 = data[2]["question"]["score"]
    score3 = data[3]["question"]["score"]
    assert score == 0
    assert score1 == 0
    assert score2 == 1
    assert score3 == 0


def test_bkt_service_guid_propagation():

    message = ''' [
      {
        "sensorId": "com.k12.learnx.events.outcome",
        "apiKey": "WC95MDmCRnWaYdUz8UJP1w",
        "event": {
          "eventTime": "2016-11-11T20:07:06Z",
          "endedAtTime": 0,
          "iType": "OutcomeEvent",
          "target": null,
          "object": {
            "count": 2,
            "dateToStartOn": 0,
            "dateToShow": 0,
            "assessmentDuration": 2,
            "maxScore": 0,
            "maxSubmits": 0,
            "endedAtTime": "2016-11-11T20:06:51Z",
            "startedAtTime": "2016-11-11T20:05:00Z",
            "datePublished": 0,
            "maxAttempts": 3,
            "dateToSubmit": 0,
            "extensions": {
              "assessmentType": "Concept Quiz",
              "assessmentId": "NG_IMA_H_01_U05_Quiz"
            },
            "assessmentItems": [],
            "dateToActivate": 0,
            "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
            "dateCreated": 0,
            "@id": "e145cb39-01a4-4935-a0e7-4b709845f825",
            "dateModified": 0
          },
          "actor": {
            "properties": null,
            "iType": "Person",
            "name": null,
            "firstName": null,
            "lastName": null,
            "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
            "email": null,
            "extensions": {
              "impersonatingUserRoles": null,
              "impersonatingUserIdentityId": null
            },
            "roles": [
              "urn:lti:instrole:ims/lis/Learner,Learner"
            ],
            "dateCreated": 0,
            "@id": "4284034",
            "dateModified": 0,
            "description": null
          },
          "group": {
            "properties": null,
            "iType": "Organization",
            "name": null,
            "dateCreated": 0,
            "parentOrg": null,
            "extensions": {
              "lti_context_label": "COF_ID6218",
              "contextId": "580e2c452d31db3dd2ef2586",
              "lti_context_id": "157988",
              "assessmentId": "134020",
              "calmsCourseId": "2907",
              "platform": "Desire2Learn",
              "unitId": "154622",
              "CourseOfferingId": "157988",
              "lessonId": "154627",
              "moduleId": "170183"
            },
            "dateModified": 0,
            "@id": "549455",
            "@type": "http://purl.imsglobal.org/caliper/v1/lis/Organization",
            "description": null
          },
          "duration": null,
          "generated": {
            "comment": null,
            "scoredBy": null,
            "properties": null,
            "iType": "AssessmentResult",
            "name": null,
            "lexileMeasure": 0,
            "curvedTotalScore": 0,
            "penaltyScore": 0,
            "assignableId": "134020",
            "extraCreditScore": 0,
            "dateCreated": 0,
            "curveFactor": 0,
            "extensions": null,
            "itemResults": [
              {
                "question_reference": "3c8f3691-aec0-494a-b0bd-4de11a3c09a7",
                "item_reference": "NP157_57",
                "properties": null,
                "iType": "AssessmentItemResult",
                "name": null,
                "sequenceNumber": 0,
                "max_score": 1,
                "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                "score": 1,
                "extensions": null,
                "question_type": "classification",
                "dateCreated": 0,
                "@id": "e145cb39-01a4-4935-a0e7-4b709845f825_d212892b86301d189ceb4f89b73c9e07",
                "dateModified": 0,
                "automarkable": 1,
                "description": null
              },
              {
                "question_reference": "e9ce48ca-7af3-4932-8de8-ec297512f9b6",
                "item_reference": "NP018_99",
                "properties": null,
                "iType": "AssessmentItemResult",
                "name": null,
                "sequenceNumber": 1,
                "max_score": 1,
                "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                "score": 1,
                "extensions": null,
                "question_type": "mcq",
                "dateCreated": 0,
                "@id": "e145cb39-01a4-4935-a0e7-4b709845f825_7540aa1474ca690f02b15d48cf2e294b",
                "dateModified": 0,
                "automarkable": 1,
                "description": null
              },
              {
                "question_reference": "261964c4-c1d6-4993-871c-e7efe860f82b",
                "item_reference": "NP018_104",
                "properties": null,
                "iType": "AssessmentItemResult",
                "name": null,
                "sequenceNumber": 2,
                "max_score": 1,
                "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                "score": 0,
                "extensions": null,
                "question_type": "mcq",
                "dateCreated": 0,
                "@id": "e145cb39-01a4-4935-a0e7-4b709845f825_34d1092c40220ff2be27309ec2485933",
                "dateModified": 0,
                "automarkable": 1,
                "description": null
              },
              {
                "question_reference": "56d4d4e8-3889-4b7a-bf34-a57c28c7d0d6",
                "item_reference": "NP157_58",
                "properties": null,
                "iType": "AssessmentItemResult",
                "name": null,
                "sequenceNumber": 3,
                "max_score": 1,
                "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                "score": 1,
                "extensions": null,
                "question_type": "classification",
                "dateCreated": 0,
                "@id": "e145cb39-01a4-4935-a0e7-4b709845f825_9ca3cc74396600afc344c4d273e5f69c",
                "dateModified": 0,
                "automarkable": 1,
                "description": null
              },
              {
                "question_reference": "1bc382bd-bb90-4c06-8daa-69bbbee0f54e",
                "item_reference": "NP157_59",
                "properties": null,
                "iType": "AssessmentItemResult",
                "name": null,
                "sequenceNumber": 4,
                "max_score": 1,
                "@type": "http://purl.imsglobal.org/caliper/v1/Result",
                "score": 1,
                "extensions": null,
                "question_type": "classification",
                "dateCreated": 0,
                "@id": "e145cb39-01a4-4935-a0e7-4b709845f825_e54b322f8bf66fe2b29413b111e973a1",
                "dateModified": 0,
                "automarkable": 1,
                "description": null
              }
            ],
            "@type": "http://purl.imsglobal.org/caliper/v1/Result",
            "totalScore": 5,
            "actorId": "4284034",
            "@id": "e145cb39-01a4-4935-a0e7-4b709845f825",
            "dateModified": 0,
            "normalScore": 4,
            "description": null
          },
          "startedAtTime": 0,
          "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#Graded",
          "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
          "@type": "http://purl.imsglobal.org/caliper/v1/OutcomeEvent",
          "edApp": {
            "properties": null,
            "iType": "SoftwareApplication",
            "description": null,
            "@type": null,
            "extensions": null,
            "dateCreated": 0,
            "@id": null,
            "dateModified": 0,
            "name": "K12 LearnX"
          }
        },
        "system": {
          "@id": [
            "db5a874b-ed84-4cbd-87e0-a4241659b36d"
          ]
        }
      }
    ]
    '''

    response = test_app.post("/bkt_service/unwind", params=message)

    assert response.status == '200 OK'

    result = response.json
    input = json.loads(message)[0]

    for e in result:
        assert e["system"]["@id"] == input["system"]["@id"]