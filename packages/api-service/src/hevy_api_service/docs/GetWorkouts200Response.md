# GetWorkouts200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** | Current page number | [optional] 
**page_count** | **int** | Total number of pages | [optional] 
**workouts** | [**List[Workout]**](Workout.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.get_workouts200_response import GetWorkouts200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkouts200Response from a JSON string
get_workouts200_response_instance = GetWorkouts200Response.from_json(json)
# print the JSON string representation of the object
print(GetWorkouts200Response.to_json())

# convert the object into a dict
get_workouts200_response_dict = get_workouts200_response_instance.to_dict()
# create an instance of GetWorkouts200Response from a dict
get_workouts200_response_from_dict = GetWorkouts200Response.from_dict(get_workouts200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


