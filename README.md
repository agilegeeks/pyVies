# A wrapper API of VIES VAT web service

## Compatibility
Requires Python 2.7 or greater.
Has been tested on 2.7, 3.4 and 3.6

## Installation

    $ pip install pyvieser

## Usage

##### Python API:

```python
from pyVies import api

try:
    vies = api.Vies()
    result = vies.request('2785503', 'RO')

    # works as well
    # result = vies.request('RO2785503')
    # result = vies.request('RO2785503', 'RO')

except api.ViesValidationError as e:
    print (e)
except api.ViesHTTPError as e:
    print (e)
except api.ViesError as e:
    print (e)
else:
    print (result)


# You may also use "clean" to extract vat number and country code
# The line bellow would print ('2785503', 'RO')

print (vies.clean('RO2785503'))

```

##### From console:

	$ pyvies <vat_number>

The number should start with the country code.
For python3 you might have to set python encoding for your environment (e.g. export PYTHONIOENCODING=utf-8).
