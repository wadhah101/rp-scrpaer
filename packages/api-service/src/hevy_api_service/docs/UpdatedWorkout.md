# UpdatedWorkout


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Indicates the type of the event (updated) | 
**workout** | [**Workout**](Workout.md) |  | 

## Example

```python
from hevy_api_service.models.updated_workout import UpdatedWorkout

# TODO update the JSON string below
json = "{}"
# create an instance of UpdatedWorkout from a JSON string
updated_workout_instance = UpdatedWorkout.from_json(json)
# print the JSON string representation of the object
print(UpdatedWorkout.to_json())

# convert the object into a dict
updated_workout_dict = updated_workout_instance.to_dict()
# create an instance of UpdatedWorkout from a dict
updated_workout_from_dict = UpdatedWorkout.from_dict(updated_workout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


