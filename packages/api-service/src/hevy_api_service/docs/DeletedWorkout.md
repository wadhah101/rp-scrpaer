# DeletedWorkout


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Indicates the type of the event (deleted) | 
**id** | **str** | The unique identifier of the deleted workout | 
**deleted_at** | **str** | A date string indicating when the workout was deleted | [optional] 

## Example

```python
from hevy_api_service.models.deleted_workout import DeletedWorkout

# TODO update the JSON string below
json = "{}"
# create an instance of DeletedWorkout from a JSON string
deleted_workout_instance = DeletedWorkout.from_json(json)
# print the JSON string representation of the object
print(DeletedWorkout.to_json())

# convert the object into a dict
deleted_workout_dict = deleted_workout_instance.to_dict()
# create an instance of DeletedWorkout from a dict
deleted_workout_from_dict = DeletedWorkout.from_dict(deleted_workout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


