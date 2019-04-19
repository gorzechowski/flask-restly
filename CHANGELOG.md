# Changelog

## 1.0.1 (19.04.2019)
* Fix: protobuf's map causes error, #16

## 1.0.0 (12.04.2019)
* Rating limit decorators

## 0.7.1 (22.02.2019)
* Fix: Return BadRequest when request body not provided but required

## 0.7.0 (03.01.2019)
* Limitation of max nested resources removed
* Better url rule names used in `flask.request.url_rule.endpoint`
* Fix: proper handle of dict returned from `put` method

## 0.6.0 (10.12.2018)
* Identity support (authentication)
* Added few missing exceptions: NotAcceptable, NotImplemented, TooManyRequests, Unauthorized, UnprocessableEntity
* Fix: Inject body keyword argument to view function only if declared and available in request

## 0.5.1 (08.11.2018)
* Fix: removed limitation regarding same method names between resources

## 0.5.0 (30.10.2018)
* `@queued` decorator added
* BREAK: removed `queued` flag in `@delete` decorator, `@queued` should be used instead 

## 0.4.0 (26.10.2018)
* Authorization decorators

## 0.3.1 (25.10.2018)
* Fixed routing

## 0.3.0 (25.10.2018)
* Protobuf support
* Request body JSON and Protobuf deserialization
* Customizable api prefix

## 0.2.0 (16.10.2018)
* Ability to skip `flask-restly`'s serialization when `Response` object is used
* Custom serializer support

## 0.1.1 (12.10.2018)
* Fixed PyPi markdown README view

## 0.1.0 (11.10.2018)
* Initial release
