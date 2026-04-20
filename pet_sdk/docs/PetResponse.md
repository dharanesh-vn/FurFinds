# PetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**type** | **str** |  | 
**adopted** | **bool** |  | 

## Example

```python
from openapi_client.models.pet_response import PetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PetResponse from a JSON string
pet_response_instance = PetResponse.from_json(json)
# print the JSON string representation of the object
print(PetResponse.to_json())

# convert the object into a dict
pet_response_dict = pet_response_instance.to_dict()
# create an instance of PetResponse from a dict
pet_response_from_dict = PetResponse.from_dict(pet_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


