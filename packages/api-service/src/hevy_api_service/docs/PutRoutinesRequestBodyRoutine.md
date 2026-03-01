# PutRoutinesRequestBodyRoutine


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The title of the routine. | [optional] 
**notes** | **str** | Additional notes for the routine. | [optional] 
**exercises** | [**List[PutRoutinesRequestExercise]**](PutRoutinesRequestExercise.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.put_routines_request_body_routine import PutRoutinesRequestBodyRoutine

# TODO update the JSON string below
json = "{}"
# create an instance of PutRoutinesRequestBodyRoutine from a JSON string
put_routines_request_body_routine_instance = PutRoutinesRequestBodyRoutine.from_json(json)
# print the JSON string representation of the object
print(PutRoutinesRequestBodyRoutine.to_json())

# convert the object into a dict
put_routines_request_body_routine_dict = put_routines_request_body_routine_instance.to_dict()
# create an instance of PutRoutinesRequestBodyRoutine from a dict
put_routines_request_body_routine_from_dict = PutRoutinesRequestBodyRoutine.from_dict(put_routines_request_body_routine_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


