# MuscleGroupPriority


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**muscle_group_id** | **int** |  | [optional] 
**mg_priority_type** | **str** |  | [optional] 

## Example

```python
from api_service_rp.models.muscle_group_priority import MuscleGroupPriority

# TODO update the JSON string below
json = "{}"
# create an instance of MuscleGroupPriority from a JSON string
muscle_group_priority_instance = MuscleGroupPriority.from_json(json)
# print the JSON string representation of the object
print(MuscleGroupPriority.to_json())

# convert the object into a dict
muscle_group_priority_dict = muscle_group_priority_instance.to_dict()
# create an instance of MuscleGroupPriority from a dict
muscle_group_priority_from_dict = MuscleGroupPriority.from_dict(muscle_group_priority_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


