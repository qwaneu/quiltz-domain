# quiltz-domain

python domain concepts for quiltz

## Purpose

At QWAN we're building some applications in python. We collect usefull stuff in
quiltz packages:

* **quiltz-domain** (this module) contains domain level modules like, entity
  id's, results, an email anonymizer, validators and parsers
* **quiltz-testsupport** contains test support modules, that supports mainly non
  unit tests, like integrating with smtp, probing asynchronous results and
  asserting log statements
* **quiltz-messaging** contains a messaging domain concept and an engine(s) to
  send the messages. Currently only smtp sending is supported.

## installing 

```bash
pip install quitlz-domain
```

See [documentation](doc/index.md)
