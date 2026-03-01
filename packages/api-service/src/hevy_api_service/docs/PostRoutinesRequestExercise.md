# PostRoutinesRequestExercise


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exercise_template_id** | **str** | The ID of the exercise template. | [optional] 
**superset_id** | **int** | The ID of the superset. | [optional] 
**rest_seconds** | **int** | The rest time in seconds. | [optional] 
**notes** | **str** | Additional notes for the exercise. | [optional] 
**sets** | [**List[PostRoutinesRequestSet]**](PostRoutinesRequestSet.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_routines_request_exercise import PostRoutinesRequestExercise

# TODO update the JSON string below
json = "{}"
# create an instance of PostRoutinesRequestExercise from a JSON string
post_routines_request_exercise_instance = PostRoutinesRequestExercise.from_json(json)
# print the JSON string representation of the object
print(PostRoutinesRequestExercise.to_json())

# convert the object into a dict
post_routines_request_exercise_dict = post_routines_request_exercise_instance.to_dict()
# create an instance of PostRoutinesRequestExercise from a dict
post_routines_request_exercise_from_dict = PostRoutinesRequestExercise.from_dict(post_routines_request_exercise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


