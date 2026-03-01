# UserProfile


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**email** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**photo_url** | **str** |  | [optional] 
**google_id** | **str** |  | [optional] 
**apple_id** | **str** |  | [optional] 
**facebook_id** | **str** |  | [optional] 
**role_id** | **int** |  | [optional] 
**stripe_id** | **str** |  | [optional] 
**klaviyo_id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**first_seen_at** | **datetime** |  | [optional] 
**attributes** | [**UserAttributes**](UserAttributes.md) |  | [optional] 

## Example

```python
from api_service_rp.models.user_profile import UserProfile

# TODO update the JSON string below
json = "{}"
# create an instance of UserProfile from a JSON string
user_profile_instance = UserProfile.from_json(json)
# print the JSON string representation of the object
print(UserProfile.to_json())

# convert the object into a dict
user_profile_dict = user_profile_instance.to_dict()
# create an instance of UserProfile from a dict
user_profile_from_dict = UserProfile.from_dict(user_profile_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


