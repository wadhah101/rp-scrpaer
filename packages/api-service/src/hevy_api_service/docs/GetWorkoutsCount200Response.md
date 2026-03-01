# GetWorkoutsCount200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workout_count** | **int** | The total number of workouts | [optional] [default to 42]

## Example

```python
from hevy_api_service.models.get_workouts_count200_response import GetWorkoutsCount200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkoutsCount200Response from a JSON string
get_workouts_count200_response_instance = GetWorkoutsCount200Response.from_json(json)
# print the JSON string representation of the object
print(GetWorkoutsCount200Response.to_json())

# convert the object into a dict
get_workouts_count200_response_dict = get_workouts_count200_response_instance.to_dict()
# create an instance of GetWorkoutsCount200Response from a dict
get_workouts_count200_response_from_dict = GetWorkoutsCount200Response.from_dict(get_workouts_count200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


