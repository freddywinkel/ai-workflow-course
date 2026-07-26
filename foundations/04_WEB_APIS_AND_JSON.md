# Foundation 4 — The Web, APIs, HTTP, and JSON

## Outcome

You can describe a request and response, read a small JSON payload, and explain
why a status code alone does not prove that the returned data is correct.

## Browser, client, server

A **client** asks for something. A **server** listens for requests and returns
responses. A web browser is one kind of client. n8n and Python can also be
clients.

In later exercises, a development tool may create a small local server.
“Local” or `localhost` means it runs on your computer. Port `8000` identifies
one listening service:

```text
http://localhost:8000/health
```

- `http` is the protocol;
- `localhost` is the host;
- `8000` is the port;
- `/health` is the path.

An **endpoint** is a particular method and path exposed by an API.

## What an API is

An application programming interface (API) is an agreed way for software
components to communicate. It defines:

- what request is allowed;
- which data shape is expected;
- how authentication works;
- what response or error is returned.

It is a contract between programs, not a guarantee that the data is true.

## HTTP request anatomy

A request includes:

- a method;
- a URL;
- optional headers;
- sometimes a body.

Common methods:

- `GET`: read;
- `POST`: submit or create;
- `PUT` / `PATCH`: replace or update;
- `DELETE`: delete.

Treat the method as a clue, not proof of safety. A badly designed `GET` can
still have side effects, and a `POST` may only perform a harmless validation.
Read the API documentation.

Headers carry metadata such as content type, authentication, or a trace ID. The
body carries the main payload.

## Responses and status codes

Common status families:

- `2xx`: the server accepted or completed the request;
- `4xx`: the request, identity, permission, or current state was unacceptable;
- `5xx`: the server failed while handling it.

Examples:

- `200 OK`: successful response;
- `202 Accepted`: accepted for processing, not necessarily finished;
- `400 Bad Request`: invalid request;
- `401 Unauthorized`: authentication missing or invalid;
- `403 Forbidden`: identity known but action not allowed;
- `404 Not Found`: resource not found;
- `409 Conflict`: conflicts with current state;
- `422 Unprocessable Content`: shape understood but validation failed;
- `429 Too Many Requests`: rate limit;
- `500 Internal Server Error`: server-side failure.

A `200` can still contain wrong facts. The response must also pass schema,
semantic, evidence, and business-rule validation.

## JSON

JSON carries structured data:

```json
{
  "request_id": "demo-001",
  "accepted": true,
  "state": "received",
  "reason_code": null,
  "work_items": [
    {"work_item_id": "WI-0001", "status": "open"}
  ]
}
```

An object uses `{}` and contains key/value pairs. An array uses `[]` and
contains a sequence. Strings use double quotes. `true`, `false`, and `null` are
lowercase.

A JSON Schema describes allowed structure and types. It can establish that
`byte_size` is an integer. It cannot establish that the actual uploaded file
has that size or that a quoted price is correct. Those require deterministic
checks and evidence.

## Authentication and authorization

**Authentication** asks “who or what are you?” **Authorization** asks “may this
identity perform this action on this resource?”

An API key is a secret credential. Do not place it:

- in course Markdown;
- in source code;
- in a screenshot;
- in an exported n8n workflow;
- in a Git commit;
- in an AI chat message.

Use the environment or credential store taught in the setup guide.

## Timeouts, retries, and duplicates

A timeout means the client stopped waiting. It does not prove the server did
nothing. Blindly repeating a request can create a duplicate.

An idempotency key lets repeated equivalent attempts refer to one intended
operation. Modules 4 and 6 turn this into executable safety tests.

Retry only declared temporary failures and cap the attempts. Validation or
permission failures normally require correction or review, not repeated calls.
Modules 4–6 turn these principles into workflow controls.

## Practice without an external service

Read this fictional interaction:

```text
POST /v1/work-items/validate
Content-Type: application/json

{"request_id":"demo-001","work_item_id":"WI-0001"}
```

Response:

```text
202 Accepted

{"request_id":"demo-001","state":"received"}
```

Answer:

1. What is the method?
2. What is the endpoint path?
3. What is the body format?
4. Does `202` mean validation finished?
5. What identifier should a retry preserve?

Then edit the JSON by removing one quote or comma and use your editor's JSON
validation. Observe the error and restore it.

## Chapter check

You pass when you can explain:

- client, server, localhost, port, API, endpoint, request, and response;
- the difference between authentication and authorization;
- why status `202` and schema-valid JSON do not prove factual correctness;
- why a timed-out request must not be repeated without duplicate protection.
