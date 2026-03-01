# Exercise


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**muscle_group_id** | **int** |  | [optional] 
**mg_sub_type** | **str** | e.g. \&quot;vertical\&quot; | [optional] 
**exercise_type** | **str** |  | [optional] 
**youtube_id** | **str** |  | [optional] 
**user_id** | **int** | null for built-in, user ID for custom | [optional] 
**notes** | **List[object]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 

## Example

```python
from api_service_rp.models.exercise import Exercise

# TODO update the JSON string below
json = "{}"
# create an instance of Exercise from a JSON string
exercise_instance = Exercise.from_json(json)
# print the JSON string representation of the object
print(Exercise.to_json())

# convert the object into a dict
exercise_dict = exercise_instance.to_dict()
# create an instance of Exercise from a dict
exercise_from_dict = Exercise.from_dict(exercise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


