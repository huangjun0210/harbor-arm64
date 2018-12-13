# -*- coding: utf-8 -*-

import time
import re
import base
import swagger_client
from swagger_client.rest import ApiException

class System(base.Base):
    def get_gc_history(self, expect_status_code = 200, expect_response_body = None, **kwargs):
        client = self._get_client(**kwargs)

        try:
            data, status_code, _ = client.system_gc_get_with_http_info()
        except ApiException as e:
            if e.status == expect_status_code:
                if expect_response_body is not None and e.body.strip() != expect_response_body.strip():
                    raise Exception(r"Get configuration response body is not as expected {} actual status is {}.".format(expect_response_body.strip(), e.body.strip()))
                else:
                    return e.reason, e.body
            else:
                raise Exception(r"Get configuration result is not as expected {} actual status is {}.".format(expect_status_code, e.status))
        base._assert_status_code(expect_status_code, status_code)
        return data

    def get_gc_status_by_id(self, job_id, expect_status_code = 200, expect_response_body = None, **kwargs):
        client = self._get_client(**kwargs)

        try:
            data, status_code, _ = client.system_gc_id_get_with_http_info(job_id)
        except ApiException as e:
            if e.status == expect_status_code:
                if expect_response_body is not None and e.body.strip() != expect_response_body.strip():
                    raise Exception(r"Get configuration response body is not as expected {} actual status is {}.".format(expect_response_body.strip(), e.body.strip()))
                else:
                    return e.reason, e.body
            else:
                raise Exception(r"Get configuration result is not as expected {} actual status is {}.".format(expect_status_code, e.status))
        base._assert_status_code(expect_status_code, status_code)
        return data

    def get_gc_log_by_id(self, job_id, expect_status_code = 200, expect_response_body = None, **kwargs):
        client = self._get_client(**kwargs)

        try:
            data, status_code, _ = client.system_gc_id_log_get_with_http_info(job_id)
        except ApiException as e:
            if e.status == expect_status_code:
                if expect_response_body is not None and e.body.strip() != expect_response_body.strip():
                    raise Exception(r"Get configuration response body is not as expected {} actual status is {}.".format(expect_response_body.strip(), e.body.strip()))
                else:
                    return e.reason, e.body
            else:
                raise Exception(r"Get configuration result is not as expected {} actual status is {}.".format(expect_status_code, e.status))
        base._assert_status_code(expect_status_code, status_code)
        return data

    def get_gc_schedule(self, expect_status_code = 200, expect_response_body = None, **kwargs):
        client = self._get_client(**kwargs)

        try:
            data, status_code, _ = client.system_gc_schedule_get_with_http_info()
        except ApiException as e:
            if e.status == expect_status_code:
                if expect_response_body is not None and e.body.strip() != expect_response_body.strip():
                    raise Exception(r"Get configuration response body is not as expected {} actual status is {}.".format(expect_response_body.strip(), e.body.strip()))
                else:
                    return e.reason, e.body
            else:
                raise Exception(r"Get configuration result is not as expected {} actual status is {}.".format(expect_status_code, e.status))
        base._assert_status_code(expect_status_code, status_code)
        return data

    def set_gc_schedule(self, schedule_type = 'None', offtime = None, weekday = None, expect_status_code = 200, expect_response_body = None, **kwargs):
        client = self._get_client(**kwargs)
        gc_schedule = swagger_client.GCSchedule()
        gc_schedule.type = schedule_type
        if offtime is not None:
            gc_schedule.offtime = offtime
        if weekday is not None:
            gc_schedule.weekday = weekday
        try:
            data, status_code, _ = client.system_gc_schedule_put_with_http_info(gc_schedule)
        except ApiException as e:
            if e.status == expect_status_code:
                if expect_response_body is not None and e.body.strip() != expect_response_body.strip():
                    raise Exception(r"Get configuration response body is not as expected {} actual status is {}.".format(expect_response_body.strip(), e.body.strip()))
                else:
                    return e.reason, e.body
            else:
                raise Exception(r"Get configuration result is not as expected {} actual status is {}.".format(expect_status_code, e.status))
        base._assert_status_code(expect_status_code, status_code)
        return data

    def create_gc_schedule(self, schedule_type, offtime = None, weekday = None, expect_status_code = 201, expect_response_body = None, **kwargs):
        client = self._get_client(**kwargs)
        gcscheduleschedule = swagger_client.GCScheduleSchedule()
        gcscheduleschedule.type = schedule_type
        if offtime is not None:
            gcscheduleschedule.offtime = offtime
        if weekday is not None:
            gcscheduleschedule.weekday = weekday

        gc_schedule = swagger_client.GCSchedule(gcscheduleschedule)
        try:
            _, status_code, header = client.system_gc_schedule_post_with_http_info(gc_schedule)
        except ApiException as e:
            if e.status == expect_status_code:
                if expect_response_body is not None and e.body.strip() != expect_response_body.strip():
                    raise Exception(r"Create GC schedule response body is not as expected {} actual status is {}.".format(expect_response_body.strip(), e.body.strip()))
                else:
                    return e.reason, e.body
            else:
                raise Exception(r"Create GC schedule result is not as expected {} actual status is {}.".format(expect_status_code, e.status))
        base._assert_status_code(expect_status_code, status_code)
        return base._get_id_from_header(header)

    def gc_now(self, **kwargs):
        gc_id = self.create_gc_schedule('Manual', **kwargs)
        return gc_id

    def validate_gc_job_status(self, gc_id, expected_gc_status, **kwargs):
        get_gc_status_finish = False
        timeout_count = 20
        while not (get_gc_status_finish):
            time.sleep(5)
            status = self.get_gc_status_by_id(gc_id, **kwargs)
            if len(status) is not 1:
                raise Exception(r"Get GC status count expected 1 actual count is {}.".format(len(status)))
            if status[0].job_status == expected_gc_status:
                get_gc_status_finish = True
            timeout_count = timeout_count - 1

        if not (get_gc_status_finish):
            raise Exception("Scan image result is not as expected {} actual scan status is {}".format(expected_scan_status, actual_scan_status))

    def validate_deletion_success(self, gc_id, **kwargs):
        log_content = self.get_gc_log_by_id(gc_id, **kwargs)
        key_message = "blobs eligible for deletion"
        key_message_pos = log_content.find(key_message)
        full_message = log_content[key_message_pos-30 : key_message_pos + len(key_message)]
        deleted_files_count_list = re.findall(r'\s+(\d+)\s+blobs eligible for deletion', full_message)

        if len(deleted_files_count_list) != 1:
            raise Exception(r"Fail to get blobs eligible for deletion in log file, failure is {}.".format(len(deleted_files_count_list)))
        deleted_files_count = int(deleted_files_count_list[0])
        if deleted_files_count == 0:
            raise Exception(r"Get blobs eligible for deletion count is {}, while we expect more than 1.".format(deleted_files_count))

