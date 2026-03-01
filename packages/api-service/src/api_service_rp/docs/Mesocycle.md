# Mesocycle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** |  | [optional] 
**user_id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**days** | **int** |  | [optional] 
**unit** | **str** |  | [optional] 
**week_count** | **int** | Number of weeks in the mesocycle | [optional] 
**source_template_id** | **int** |  | [optional] 
**source_meso_id** | **int** |  | [optional] 
**micro_rirs** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**first_set_completed_at** | **datetime** |  | [optional] 
**last_workout_finished_at** | **datetime** |  | [optional] 
**priorities** | [**Dict[str, MuscleGroupPriority]**](MuscleGroupPriority.md) |  | [optional] 
**notes** | **List[object]** |  | [optional] 
**status** | **str** |  | [optional] 
**generated_from** | **str** |  | [optional] 
**weeks** | [**List[Week]**](Week.md) |  | [optional] 

## Example

```python
from api_service_rp.models.mesocycle import Mesocycle

# TODO update the JSON string below
json = "{}"
# create an instance of Mesocycle from a JSON string
mesocycle_instance = Mesocycle.from_json(json)
# print the JSON string representation of the object
print(Mesocycle.to_json())

# convert the object into a dict
mesocycle_dict = mesocycle_instance.to_dict()
# create an instance of Mesocycle from a dict
mesocycle_from_dict = Mesocycle.from_dict(mesocycle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


