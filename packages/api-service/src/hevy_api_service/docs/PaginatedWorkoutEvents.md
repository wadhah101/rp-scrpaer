# PaginatedWorkoutEvents


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** | The current page number | 
**page_count** | **int** | The total number of pages available | 
**events** | [**List[PaginatedWorkoutEventsEventsInner]**](PaginatedWorkoutEventsEventsInner.md) | An array of workout events (either updated or deleted) | 

## Example

```python
from hevy_api_service.models.paginated_workout_events import PaginatedWorkoutEvents

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedWorkoutEvents from a JSON string
paginated_workout_events_instance = PaginatedWorkoutEvents.from_json(json)
# print the JSON string representation of the object
print(PaginatedWorkoutEvents.to_json())

# convert the object into a dict
paginated_workout_events_dict = paginated_workout_events_instance.to_dict()
# create an instance of PaginatedWorkoutEvents from a dict
paginated_workout_events_from_dict = PaginatedWorkoutEvents.from_dict(paginated_workout_events_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


