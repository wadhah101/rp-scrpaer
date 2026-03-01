# UserAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**birthdate** | **str** |  | [optional] 
**sex** | **str** |  | [optional] 
**training_years** | **str** |  | [optional] 
**training_preference_exercise_types** | **str** | JSON-encoded string | [optional] 
**attribution_survey** | **str** |  | [optional] 
**created_on_platform** | **str** |  | [optional] 
**training_feature_auto_apply_weights** | **bool** |  | [optional] 
**training_apply_exercise_types** | **bool** |  | [optional] 

## Example

```python
from api_service_rp.models.user_attributes import UserAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of UserAttributes from a JSON string
user_attributes_instance = UserAttributes.from_json(json)
# print the JSON string representation of the object
print(UserAttributes.to_json())

# convert the object into a dict
user_attributes_dict = user_attributes_instance.to_dict()
# create an instance of UserAttributes from a dict
user_attributes_from_dict = UserAttributes.from_dict(user_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


