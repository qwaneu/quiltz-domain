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

## validations

## parsers

## results

## anonymizer