from ariadne import QueryType,MutationType,load_schema_from_path, make_executable_schema, ObjectType
from apps.accounts import resolvers as acc_res
#Test Query Field
def resolve_test(_, info, name=None):
    return "Hello I am working!" if name==None else f"Hello {name}, I am working!"

#Base Query Object
query = QueryType() #ObjectType("Query")
query.set_field("test", resolve_test )
query.set_field("patient", acc_res.resolve_patient)
#Base Mutation Object
mutation = MutationType() #ObjectType("Mutation")
mutation.set_field("login", acc_res.resolve_login)

# Type Defs from Schems.graphql Files
type_defs = load_schema_from_path('apps/api/schema.graphql')
accounts_def = load_schema_from_path('apps/accounts/schema.graphql')

#Schema Object
schema = make_executable_schema([type_defs, accounts_def],[query, mutation, acc_res.patient, acc_res.patient_data, acc_res.address])
