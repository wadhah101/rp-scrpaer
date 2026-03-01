# PaginatedWorkoutEventsEventsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Indicates the type of the event (deleted) | 
**workout** | [**Workout**](Workout.md) |  | 
**id** | **str** | The unique identifier of the deleted workout | 
**deleted_at** | **str** | A date string indicating when the workout was deleted | [optional] 

## Example

```python
from hevy_api_service.models.paginated_workout_events_events_inner import PaginatedWorkoutEventsEventsInner

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedWorkoutEventsEventsInner from a JSON string
paginated_workout_events_events_inner_instance = PaginatedWorkoutEventsEventsInner.from_json(json)
# print the JSON string representation of the object
print(PaginatedWorkoutEventsEventsInner.to_json())

# convert the object into a dict
paginated_workout_events_events_inner_dict = paginated_workout_events_events_inner_instance.to_dict()
# create an instance of PaginatedWorkoutEventsEventsInner from a dict
paginated_workout_events_events_inner_from_dict = PaginatedWorkoutEventsEventsInner.from_dict(paginated_workout_events_events_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


