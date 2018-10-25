from flask_restly.serializer import _dict_to_protobuf, _protobuf_to_dict
from tests.fixtures.company_pb2 import Company, Employee
import pytest


def company_with_no_employees():
    return {
        'id': 1,
    }


def company_with_employees():
    return {
        'id': 2,
        'employees': [
            {
                'id': 1,
                'name': 'some name',
                'position': Employee.CTO,
            },
            {
                'id': 2,
                'name': 'some other name',
                'position': Employee.CEO,
                'isActive': True,
            },
        ]
    }


@pytest.mark.parametrize("data,expected_data", [
    (company_with_no_employees(), bytes('\x08\x01', 'utf8')),
    (company_with_employees(), bytes(
        '\x08\x02\x12\x0f\x08\x01\x12\tsome name\x18\x01\x12\x17\x08\x02\x12\x0fsome other name\x18\x02 \x01', 'utf8'
    )),
])
def test_should_serialize_given_response_to_json(data, expected_data):
    company = _dict_to_protobuf(data, Company)

    assert company.SerializeToString() == expected_data


@pytest.mark.parametrize("data,expected_data", [
    (_dict_to_protobuf(company_with_no_employees(), Company), company_with_no_employees()),
    (_dict_to_protobuf(company_with_employees(), Company), company_with_employees()),
])
def test_should_serialize_given_response_to_json(data, expected_data):
    company = _protobuf_to_dict(data)

    assert company == expected_data
