# PutRoutinesRequestBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**routine** | [**PutRoutinesRequestBodyRoutine**](PutRoutinesRequestBodyRoutine.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.put_routines_request_body import PutRoutinesRequestBody

# TODO update the JSON string below
json = "{}"
# create an instance of PutRoutinesRequestBody from a JSON string
put_routines_request_body_instance = PutRoutinesRequestBody.from_json(json)
# print the JSON string representation of the object
print(PutRoutinesRequestBody.to_json())

# convert the object into a dict
put_routines_request_body_dict = put_routines_request_body_instance.to_dict()
# create an instance of PutRoutinesRequestBody from a dict
put_routines_request_body_from_dict = PutRoutinesRequestBody.from_dict(put_routines_request_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


