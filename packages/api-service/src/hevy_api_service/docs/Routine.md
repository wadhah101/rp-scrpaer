# Routine


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The routine ID. | [optional] 
**title** | **str** | The routine title. | [optional] 
**folder_id** | **float** | The routine folder ID. | [optional] 
**updated_at** | **str** | ISO 8601 timestamp of when the routine was last updated. | [optional] 
**created_at** | **str** | ISO 8601 timestamp of when the routine was created. | [optional] 
**exercises** | [**List[RoutineExercisesInner]**](RoutineExercisesInner.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.routine import Routine

# TODO update the JSON string below
json = "{}"
# create an instance of Routine from a JSON string
routine_instance = Routine.from_json(json)
# print the JSON string representation of the object
print(Routine.to_json())

# convert the object into a dict
routine_dict = routine_instance.to_dict()
# create an instance of Routine from a dict
routine_from_dict = Routine.from_dict(routine_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


