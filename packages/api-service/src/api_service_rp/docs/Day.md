# Day


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**meso_id** | **int** |  | [optional] 
**week** | **int** |  | [optional] 
**position** | **int** |  | [optional] 
**bodyweight** | **float** |  | [optional] 
**bodyweight_at** | **datetime** |  | [optional] 
**unit** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**status** | **str** |  | [optional] 
**notes** | **List[object]** |  | [optional] 
**muscle_groups** | **List[object]** |  | [optional] 
**exercises** | [**List[DayExercise]**](DayExercise.md) |  | [optional] 

## Example

```python
from api_service_rp.models.day import Day

# TODO update the JSON string below
json = "{}"
# create an instance of Day from a JSON string
day_instance = Day.from_json(json)
# print the JSON string representation of the object
print(Day.to_json())

# convert the object into a dict
day_dict = day_instance.to_dict()
# create an instance of Day from a dict
day_from_dict = Day.from_dict(day_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


