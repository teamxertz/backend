from ariadne import ObjectType
from .models import User, Patient, Address, PatientData
from .exceptions import UserNotFoundError


#Address Resolver
address = ObjectType("Address")

def resolve_address(_,info,email):
    user = User.objects.prefetch_related("address").get(email=email)
    if user:
        return user.address
    else:
        raise UserNotFoundError
"""
@address.field("line1")
def resolve_address_line1(obj,*_):
    return obj.line1

@address.field("line2")
def resolve_address_line2(obj,*_):
    return obj.line2

@address.field("city")
def resolve_address_city(obj,*_):
    return obj.city

@address.field("state")
def resolve_address_state(obj,*_):
    return obj.state

@address.field("pincode")
def resolve_address_pincode(obj,*_):
    return obj.pincode
"""

# PatientData Resolvers
patient_data = ObjectType("PatientData")


def resolve_patient_data(_, info,email):
    patient = PatientData.objects.get(user__email=email)
    if patient:
        return patient
    else:
        raise UserNotFoundError
"""
@patient_data.field("name")
def resolve_patient_data_name(obj,*_):
    return obj.name

@patient_data.field("age")
def resolve_patient_data_age(obj,*_):
    return obj.age

@patient_data.field("gender")
def resolve_patient_data_gender(obj,*_):
    return obj.gender

@patient_data.field("phone")
def resolve_patient_data_phone(obj,*_):
    return f'+91 {obj.phone}'
"""
@patient_data.field("address")
def resolve_patient_data_address(obj,*_):
    return obj.user.address


#PAatient Resolvers
patient = ObjectType('Patient')

def resolve_patient(_,info, email):
    patient = Patient.objects.prefetch_related("patientdata").get(email=email)
    if patient:
        return patient
    else:
        raise UserNotFoundError

"""
@patient.field("active")
def resolve_patient_active(obj,*_):
    return obj.active

@patient.field("type")
def resolve_patient_type(obj,*_):
    return obj.type

@patient.field("email")
def resolve_patient_email(obj,*_):
    return obj.email
"""
@patient.field("data")
def resolve_patientdata(obj,*_):
    return obj.patientdata