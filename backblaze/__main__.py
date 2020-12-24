from b2sdk.v1 import InMemoryAccountInfo, B2Api
from b2sdk.exception import (DuplicateBucketName)

import requests
from sys import getsizeof
import json

from config import config

import timeit, time
from datetime import datetime
from uuid import uuid4

def main():

    # Load Data
    d = Data()
    person = d.get_person()

    # Prep test objects
    b2 = B2()
    tw = Timer()

    # # StartTest # #

    # Create Test Bucket
    test_bucket = "fray-test-bucket"
    create_bucket = wrapper(b2.create_bucket, test_bucket, "allPrivate", get_on_collision=True)
    tw.timeit("Create Bucket", create_bucket)

    # # # Upload small data
    for i in range(1000):
        person = json.dumps(d.get_person().json()).encode()
        person_size = getsizeof(person)
        upload = wrapper(b2.upload_bytes, person, "People/" + str(uuid4()) + ".json")
        tw.timeit("Persist Object", upload, note_name="object size", note_value=str(person_size))

    # Delete test bucket
    b2.delete_bucket(b2.bucket)

    # # End Test # #

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

class Timer:

    def __init__(self):
        self.report = datetime.now().isoformat() + ".csv"

    def timeit(self, test_name, function, **kwargs):
        t = timeit.timeit(function, number=1)
        self.record(test_name, t, **kwargs)

    def record(self, test_name, t, note_name=None, note_value=None):
        t = str(t)
        note_name = str(note_name)
        note_value = str(note_value)
        with open(self.report, "a") as f:
            f.write(",".join([datetime.now().isoformat(), test_name, t, note_name, note_value, '\n']))


class B2:

    def __init__(self):
        self.api = self.auth_init_b2()
        self.bucket = None

    def create_bucket(self, bucket_name, bucket_type, get_on_collision=False, **kwargs):
        try:
            response = self.api.create_bucket(bucket_name, bucket_type, **kwargs)
        except DuplicateBucketName as err:
            if not get_on_collision:
                raise err
            response = self.get_bucket(bucket_name)
        self.bucket = response
        return response

    def delete_bucket(self, bucket):
        return self.api.delete_bucket(bucket)

    def get_bucket(self, name_or_id, by="name"):
        if by.lower() == "name":
            return self.api.get_bucket_by_name(name_or_id)
        elif by.lower() == "id":
            return self.api.get_bucket_by_id(name_or_id)
        else:
            raise KeyError(f"Unrecognized 'by' -> {by}. Expected 'name' or 'id'")

    def upload_bytes(self, obj, file_name):
        return self.bucket.upload_bytes(obj, file_name)

    def auth_init_b2(self):
        """Init b2 api and attach auth"""

        b2_info = InMemoryAccountInfo()
        b2_api = B2Api(b2_info)
        b2_api.authorize_account("production", config.APP_KEY_ID, config.APP_KEY)

        return b2_api


class Data:

    def get_person(self):
        people_endpoint = "https://pipl.ir/v1/getPerson"
        return requests.get(people_endpoint)


if __name__ == "__main__":
    main()