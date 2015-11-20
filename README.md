[![Build Status](https://travis-ci.org/darthghandi/jsoncompare.svg?branch=master)](https://travis-ci.org/darthghandi/jsoncompare)

##Install
```bash
pip install json_compare
```

##Explanation
*  Being able to tell whether or not an arbitrarily nested json blob is the same as another blob can hurt your eyes.
*  Additional complexity comes in when your json array's order doesn't matter.
*  For example, you might have a set in Java that you are going to send over the wire as json. It may be represented as a json array but in actuality, you don't care about the order.

##Disclaimer
This project takes the original jsoncompare and adds a few things. First, I wanted to use this with python 3. I also needed flexibility with integers.
If an integer is say 10 off, then it's still close enough for me. I also used rapidjson instead of the builtin json module since it can offer a lot of speed.

## Recent Changes
    Version    Comments
    0.1.1      Orginal Version
    0.1.2      Adds support for "contains"
    0.1.3      Adds support for Python 3, range for int values, ujson instead of builtin json(for speed)
    0.2.0      Adds rapidjson instead of ujson, fixes a comparison issue, all unit tests pass

##Examples
```python
from json_compare import json_compare

# Compare respecting each array's order
json_compare.are_same(a, b)

# Compare ignoring each array's order
json_compare.are_same(a, b, True)

# Compare ignoring the value of certain keys
json_compare.are_same(a, b, False, ["datetime", "snacktime"])

# Compare ignoring each array's order and giving int values a 30% leeway
json_compare.are_same(a, b, True, times_higher=1.3, times_lower=.7)

# Contains at least
json_compare.contains(a, b)

```

```python
# Getting difference traces
from json_compare import json_compare

a = {
    "failureReason" : "Invalid request entity",
    "fieldValidationErrors" : [
        {
            "field" : "normal value 1",
            "reason" : "may not be smelly"
        },
        {
            "field" : "Catalog.name",
            "reason" : "may not be null"
        }
    ]
}
b = {
    "failureReason" : "Invalid request entity",
    "fieldValidationErrors" : [
        {
            "field" : "crazy value 2",
            "reason" : "may not be null"
        },
        {
            "field" : "Catalog.catalogOwner",
            "reason" : "may not be null"
        }
    ]
}
print json_compare.are_same(a, b)[1]
```
results in:

```python
Reason: Different values
Expected:
  "normal value 1"
Actual:
  "crazy value 2"

Reason: Different values (Check order)
Expected:
  {
      "field": "normal value 1", 
      "reason": "may not be smelly"
  }
Actual:
  {
      "field": "crazy value 2", 
      "reason": "may not be null"
  }

Reason: Different values
Expected:
  [
      {
          "field": "normal value 1", 
          "reason": "may not be smelly"
      }, 
      {
          "field": "Catalog.name", 
          "reason": "may not be null"
      }
  ]
Actual:
  [
      {
          "field": "crazy value 2", 
          "reason": "may not be null"
      }, 
      {
          "field": "Catalog.catalogOwner", 
          "reason": "may not be null"
      }
  ]
```
