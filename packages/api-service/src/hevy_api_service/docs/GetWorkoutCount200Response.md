# GetWorkoutCount200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workout_count** | **int** | The total number of workouts | [optional] [default to 42]

## Example

```python
from hevy_api_service.models.get_workout_count200_response import GetWorkoutCount200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkoutCount200Response from a JSON string
get_workout_count200_response_instance = GetWorkoutCount200Response.from_json(json)
# print the JSON string representation of the object
print(GetWorkoutCount200Response.to_json())

# convert the object into a dict
get_workout_count200_response_dict = get_workout_count200_response_instance.to_dict()
# create an instance of GetWorkoutCount200Response from a dict
get_workout_count200_response_from_dict = GetWorkoutCount200Response.from_dict(get_workout_count200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


