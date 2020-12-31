## modules in this package

<!--
@startuml domain-lib
skinparam {
  handwritten true
  monochrome true
  linetype ortho
}
hide <<functions>> circle
hide <<functions>> attributes
hide <<functions>> stereotype

package quiltz.domain {
  package results {
    class Success
    class Failure
  }
  package validator {
    class validatorfunctions <<functions>> {
      validate()
      optionality_of()
      max_length_of()
      is_between()
      conversion_of()
      an_attempt_to()
    }
  }
  package parsers {
    class parserfunctions <<functions>> {
      date_from_iso()
      int_from_string()
    }
  }
  package anonymizer {
    class anonymizerfunctions <<functions>> {
      anonymize()
    }
  }
  package id {
    class ID
    class IDGenerator
    class FixedIDGeneratorGenerating
  }
}
validator .> parsers
validator .> results
parsers ..> results

@enduml

-->
![domain-lib](images/domain-lib.svg)

## id

The `id` module contains a UUID based `ID` concept. It is a small domain class
encapsulating the concept of a unique id. It enables cleaner domain code and
helps to hide UUID specifics.

`IDGenerator` is a small abstraction around generation of IDs. It allows the ID
generation logic to be injected as a dependency. `IDGenerator` generates ID
objects with unique version 4 UUIDs.

```python
from quiltz.domain.id import ID, IDGenerator

id_generator = IDGenerator()
id_generator.generate_id()
# e.g. ID(_uuid=UUID('efdd6bd4-1444-4291-999c-c8e2e43a41c6'))

ID.from_string('efdd6bd4-1444-4291-999c-c8e2e43a41c6')
# ID(_uuid=UUID('efdd6bd4-1444-4291-999c-c8e2e43a41c6'))

id = ID.from_string('efdd6bd4-1444-4291-999c-c8e2e43a41c6')
str(id)
# 'efdd6bd4-1444-4291-999c-c8e2e43a41c6'
```

`ID.from_string` returns a unique null object if the string cannot be parsed as a valid UUID.

```python
ID.from_string('not a valid UUID')
# InvalidID(value='invalid_id_1')
```

The `id` module provides unit testing support that allows you to be in full
control of generating IDs. `aValidID` is a [test data builder](https://www.qwan.eu/2020/10/09/test-data-builders.html) function that generates
a valid, constant UUID ending with a specified string:

```python
from quiltz.domain.id.testbuilders import aValidID

aValidID('20')
# ID(_uuid=UUID('11111111-1111-1111-1111-111111111120'))
aValidID('55')
# ID(_uuid=UUID('11111111-1111-1111-1111-111111111155'))
```

Having ID generation injectable as a dependency enables the use of test doubles
in your unit test. The `id` module provides a stubbed ID generator
`FixedIDGeneratorGenerating`. This stubbed ID generator always returns a
specific ID value.

```python
from quiltz.domain.id import FixedIDGeneratorGenerating
from quiltz.domain.id.testbuilders import aValidID

def test_some_product_factory_generates_id():
  fixed_id_generator = FixedIDGeneratorGenerating(aValidID(20))
  factory = SomeProductFactory(id_generator=fixed_id_generator)
  assert factory.create().id == aValidID(20)
```

## results

The `results` module provides an abstraction around successful and failed
results, as a cleaner, more expressive alternative to exception handling and
passing around error codes.

The basic idea is to wrap the result of a function that can fail, in a `Result`
object, either a `Success` or a `Failure`. Both `Success` and `Failure` objects
have a `body` dictionary attribute which can contain any attribute you put in
it. They allow to directly access your attributes on the object.

```python
from quiltz.domain.results import Success, Failure

result = Success(team='Team A')     # Success(body={'team': 'Team A'})
result.team           # 'Team A'
result.is_success()   # True
result.is_failure()   # False

result = Failure(message='Failed')  # Failure(body={'message': 'Failed'})
result.message        # 'Failed'
result.is_success()   # False
result.is_failure()   # True
```

Results can be chained through `map`, which works on success values and
does nothing for failure values. 

```python
result = (Success(value=10)
  .map(lambda res: Success(new_value=res.value + 5)))
result.new_value    # 15

result = (Success(value=10)
  .map(lambda res: Failure(message='Failed'))
  .map(lambda res: Success(new_value=res.value + 5)))
result.message      # 'Failed'
result.new_value    # None
```

You can also map the failure part with `or_fail_with`, which replaces the
failure attributes and stores the original failure in the `reason` attribute.
The `or_fail_with` function does nothing on success values.

```python
result = (Failure(message='Failed')
  .or_fail_with(error_code=97))
result.error_code   # 97
result.message      # None

result = (Success(value=10)
  .or_fail_with(message='Failed'))
result.value        # 10
result.reason       # Failure(body={'message': 'Failed'})
result.message      # None
```

Results also provide a `do` function that allows to chain side effects to successful results.

```python
result = (Success(value=10)
  .do(lambda res: perform_side_effect()))
result.value    # 10
```

**Notes:** 
- The function passed to `map`/`do` receives the whole `Success` object as an argument.
- The arguments of `or_fail_with` should be the attributes of the new `Failure`.
- Both `map` and `or_fail_with` should return a new `Result` object.

To prefix an existing failure message, use the `prefix_error` function, which does nothing on success objects.

```python
result = (Failure(message='failure')
  .prefix_error('big '))
result.message    # 'big failure'
```

The `prefix_error` function follows our convention to use the `message` attribute for failure messages.

## validations

The `validations` module provides a small DSL (domain specific language) for building data validation logic.

If successful, the `validate` function returns a `ValidationResults` object
having all validated and optionally converted parameters. If not successful, it
returns a `Failure` object containing a message attribute with the validation
error.

The successful result from `validate` can be mapped to whatever you'd like to do with the valid parameters.

```python
from quiltz.domain.results import Success
from quiltz.domain.validator import validate, presence_of, max_length_of, is_between

def create(team=None, participant_count=0):
    return validate(
        presence_of('team', team),
        max_length_of('team', team, 140),
        is_between('participant_count', participant_count, 1, 30),
    ).map(lambda valid_parameters:
        Success(product=MyProduct(
                          team = valid_parameters.team,
                          participants=valid_parameters.participant_count))
    )

create(team='Team A', participant_count=2, language='en')
# Success(body={'product': <__main__.Product object at 0x7f8548df8310>})

create(team=None, participant_count=2, language='en')
# Failure(body={'message': 'team is missing'})

create(team='Team A', participant_count=100, language='en')
# Failure(body={'message': 'participant_count should be between 1 and 30'})

create(team='Team A', participant_count=100, language='xx')
# Failure(body={'message': "language 'x' is not a valid language"})
```

The `conversion_of` function takes a parameter name, an input value and a class to which the value should be converted. This class should have a static `parse_from` function, which should return a `Result` object

```python
from enum import Enum
from quiltz.domain.results import Success, Failure
from quiltz.domain.validator import validate, conversion_of

class Language(Enum):
    en = 'en'
    de = 'de'

    @staticmethod
    def parse_from(text):
        try:
            return Success(language=Language(text.lower()))
        except AttributeError:
            return Failure(message="language '{}' is not a valid language".format(text))
        except ValueError:
            return Failure(message="language '{}' is not a valid language".format(text))

def create_language(language="en"):
        return validate(
            conversion_of('language', language, Language)
        ).map(lambda valid_parameters:
            Success(language=valid_parameters.language)
        )

create_language('en')
# Success(body={'language': <Language.en: 'en'>})

create_language('xx')
# Failure(body={'message': "language 'xx' is not a valid language"})
```

## parsers

The `parsers` module offers two parsers for string to object conversion:
`StringToIntParser` and `StringToDateParser`. For convenience, it provides
conversion functions `date_from_iso` and `int_from_string`, which can be used
with the `conversion_of` validator.

```python 
from quiltz.domain.results import Success
from quiltz.domain.validator import conversion_of, validate
from quiltz.domain.parsers import date_from_iso

def create(expiry_date=None):
  validate(
    conversion_of('expiry_date', expiry_date, date_from_iso)
  ).map(lambda valid_parameters:
    Success(user=User(expiry_date=valid_parameters.expiry_date))
  )
```

## anonymizer

The `anynomizer` module contains an email anonymizing function `anonymize` which
replaces most of the local part of the address by '***'. It only works on email
addresses, other strings are left unchanged.

```python
from quiltz.domain.anonymizer import anonymize

anonymize('invoices@qwan.eu')
# 'i***@qwan.eu'

anonymize('me@qwan.eu')
# 'm***@qwan.eu'

anonymize('not an email address')
# 'not an email address'
```
