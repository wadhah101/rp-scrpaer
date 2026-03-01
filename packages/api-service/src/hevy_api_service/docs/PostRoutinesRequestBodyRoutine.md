# PostRoutinesRequestBodyRoutine


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The title of the routine. | [optional] 
**folder_id** | **float** | The folder id the routine should be added to. Pass null to insert the routine into default \&quot;My Routines\&quot; folder | [optional] 
**notes** | **str** | Additional notes for the routine. | [optional] 
**exercises** | [**List[PostRoutinesRequestExercise]**](PostRoutinesRequestExercise.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_routines_request_body_routine import PostRoutinesRequestBodyRoutine

# TODO update the JSON string below
json = "{}"
# create an instance of PostRoutinesRequestBodyRoutine from a JSON string
post_routines_request_body_routine_instance = PostRoutinesRequestBodyRoutine.from_json(json)
# print the JSON string representation of the object
print(PostRoutinesRequestBodyRoutine.to_json())

# convert the object into a dict
post_routines_request_body_routine_dict = post_routines_request_body_routine_instance.to_dict()
# create an instance of PostRoutinesRequestBodyRoutine from a dict
post_routines_request_body_routine_from_dict = PostRoutinesRequestBodyRoutine.from_dict(post_routines_request_body_routine_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


