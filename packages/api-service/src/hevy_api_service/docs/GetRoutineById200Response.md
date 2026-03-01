# GetRoutineById200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**routine** | [**Routine**](Routine.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.get_routine_by_id200_response import GetRoutineById200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetRoutineById200Response from a JSON string
get_routine_by_id200_response_instance = GetRoutineById200Response.from_json(json)
# print the JSON string representation of the object
print(GetRoutineById200Response.to_json())

# convert the object into a dict
get_routine_by_id200_response_dict = get_routine_by_id200_response_instance.to_dict()
# create an instance of GetRoutineById200Response from a dict
get_routine_by_id200_response_from_dict = GetRoutineById200Response.from_dict(get_routine_by_id200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


