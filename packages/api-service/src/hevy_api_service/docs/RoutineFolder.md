# RoutineFolder


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **float** | The routine folder ID. | [optional] 
**index** | **float** | The routine folder index. Describes the order of the folder in the list. | [optional] 
**title** | **str** | The routine folder title. | [optional] 
**updated_at** | **str** | ISO 8601 timestamp of when the folder was last updated. | [optional] 
**created_at** | **str** | ISO 8601 timestamp of when the folder was created. | [optional] 

## Example

```python
from hevy_api_service.models.routine_folder import RoutineFolder

# TODO update the JSON string below
json = "{}"
# create an instance of RoutineFolder from a JSON string
routine_folder_instance = RoutineFolder.from_json(json)
# print the JSON string representation of the object
print(RoutineFolder.to_json())

# convert the object into a dict
routine_folder_dict = routine_folder_instance.to_dict()
# create an instance of RoutineFolder from a dict
routine_folder_from_dict = RoutineFolder.from_dict(routine_folder_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


