# Template


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**emphasis** | **str** |  | [optional] 
**sex** | **str** |  | [optional] 
**frequency** | **int** |  | [optional] 

## Example

```python
from api_service_rp.models.template import Template

# TODO update the JSON string below
json = "{}"
# create an instance of Template from a JSON string
template_instance = Template.from_json(json)
# print the JSON string representation of the object
print(Template.to_json())

# convert the object into a dict
template_dict = template_instance.to_dict()
# create an instance of Template from a dict
template_from_dict = Template.from_dict(template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


