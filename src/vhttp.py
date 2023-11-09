import asyncio
import dataclasses
import enum
import utils


@utils.reversible_str_enum
class HttpVersion(enum.StrEnum):
    HTTP_1_0 = "HTTP/1.0"
    HTTP_1_1 = "HTTP/1.1"
    HTTP_2 = "HTTP/2"
    HTTP_3 = "HTTP/3"


@utils.reversible_str_enum
class HttpMethod(enum.StrEnum):
    OPTIONS = "OPTIONS"
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    TRACE = "TRACE"
    CONNECT = "CONNECT"


@utils.reversible_int_enum
class HttpStatusCode(enum.IntEnum):
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102
    EARLY_HINTS = 103
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_CONTENT = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


HTTP_STATUS_CODE_MESSAGES = {
    HttpStatusCode.CONTINUE: "Continue",
    HttpStatusCode.SWITCHING_PROTOCOLS: "Switching Protocols",
    HttpStatusCode.PROCESSING: "Processing",
    HttpStatusCode.EARLY_HINTS: "Early Hints",
    HttpStatusCode.OK: "OK",
    HttpStatusCode.CREATED: "Created",
    HttpStatusCode.ACCEPTED: "Accepted",
    HttpStatusCode.NON_AUTHORITATIVE_INFORMATION: "Non-Authoritative Information",
    HttpStatusCode.NO_CONTENT: "No Content",
    HttpStatusCode.RESET_CONTENT: "Reset Content",
    HttpStatusCode.PARTIAL_CONTENT: "Partial Content",
    HttpStatusCode.MULTI_STATUS: "Multi-Status",
    HttpStatusCode.ALREADY_REPORTED: "Already Reported",
    HttpStatusCode.IM_USED: "IM Used",
    HttpStatusCode.MULTIPLE_CHOICES: "Multiple Choices",
    HttpStatusCode.MOVED_PERMANENTLY: "Moved Permanently",
    HttpStatusCode.FOUND: "Found",
    HttpStatusCode.SEE_OTHER: "See Other",
    HttpStatusCode.NOT_MODIFIED: "Not Modified",
    HttpStatusCode.TEMPORARY_REDIRECT: "Temporary Redirect",
    HttpStatusCode.PERMANENT_REDIRECT: "Permanent Redirect",
    HttpStatusCode.BAD_REQUEST: "Bad Request",
    HttpStatusCode.UNAUTHORIZED: "Unauthorized",
    HttpStatusCode.PAYMENT_REQUIRED: "Payment Required",
    HttpStatusCode.FORBIDDEN: "Forbidden",
    HttpStatusCode.NOT_FOUND: "Not Found",
    HttpStatusCode.METHOD_NOT_ALLOWED: "Method Not Allowed",
    HttpStatusCode.NOT_ACCEPTABLE: "Not Acceptable",
    HttpStatusCode.PROXY_AUTHENTICATION_REQUIRED: "Proxy Authentication Required",
    HttpStatusCode.REQUEST_TIMEOUT: "Request Timeout",
    HttpStatusCode.CONFLICT: "Conflict",
    HttpStatusCode.GONE: "Gone",
    HttpStatusCode.LENGTH_REQUIRED: "Length Required",
    HttpStatusCode.PRECONDITION_FAILED: "Precondition Failed",
    HttpStatusCode.PAYLOAD_TOO_LARGE: "Payload Too Large",
    HttpStatusCode.URI_TOO_LONG: "URI Too Long",
    HttpStatusCode.UNSUPPORTED_MEDIA_TYPE: "Unsupported Media Type",
    HttpStatusCode.RANGE_NOT_SATISFIABLE: "Range Not Satisfiable",
    HttpStatusCode.EXPECTATION_FAILED: "Expectation Failed",
    HttpStatusCode.IM_A_TEAPOT: "I'm a teapot",
    HttpStatusCode.MISDIRECTED_REQUEST: "Misdirected Request",
    HttpStatusCode.UNPROCESSABLE_CONTENT: "Unprocessable Content",
    HttpStatusCode.LOCKED: "Locked",
    HttpStatusCode.FAILED_DEPENDENCY: "Failed Dependency",
    HttpStatusCode.TOO_EARLY: "Too Early",
    HttpStatusCode.UPGRADE_REQUIRED: "Upgrade Required",
    HttpStatusCode.PRECONDITION_REQUIRED: "Precondition Failed",
    HttpStatusCode.TOO_MANY_REQUESTS: "Too Many Requests",
    HttpStatusCode.REQUEST_HEADER_FIELDS_TOO_LARGE: "Request Header Fields Too Large",
    HttpStatusCode.UNAVAILABLE_FOR_LEGAL_REASONS: "Unavailable For Legal Reasons",
    HttpStatusCode.INTERNAL_SERVER_ERROR: "Internal Server Error",
    HttpStatusCode.NOT_IMPLEMENTED: "Not Implemented",
    HttpStatusCode.BAD_GATEWAY: "Bad Gateway",
    HttpStatusCode.SERVICE_UNAVAILABLE: "Service Unavailable",
    HttpStatusCode.GATEWAY_TIMEOUT: "Gateway Timeout",
    HttpStatusCode.HTTP_VERSION_NOT_SUPPORTED: "HTTP Version Not Supported",
    HttpStatusCode.VARIANT_ALSO_NEGOTIATES: "Variant Also Negotiates",
    HttpStatusCode.INSUFFICIENT_STORAGE: "Insufficient Storage",
    HttpStatusCode.LOOP_DETECTED: "Loop Detected",
    HttpStatusCode.NOT_EXTENDED: "Not Extended",
    HttpStatusCode.NETWORK_AUTHENTICATION_REQUIRED: "Network Authentication Required",
}


@dataclasses.dataclass
class HttpRequestLine:
    method: HttpMethod
    uri: str
    version: HttpVersion

    @classmethod
    def parse(cls, line: bytes) -> 'HttpRequestLine':
        method_s, uri, version_s = line.decode('utf-8').strip().split(' ', 2)
        return cls(HttpMethod.inverse(method_s), uri, HttpVersion.inverse(version_s))


class HttpError(Exception):
    def __init__(self, status_code: HttpStatusCode):
        self.status_code = status_code


class HttpRequest:
    def __init__(self, request_line: HttpRequestLine, headers: dict[str, str | list[str]], body: bytes):
        self.request_line = request_line
        self.headers = headers
        self.body = body

    @classmethod
    async def read(cls, reader: asyncio.StreamReader) -> 'HttpRequest':
        request_line_s: bytes = await reader.readline()
        request_line = HttpRequestLine.parse(request_line_s)
        headers: dict[str, str | list[str]] = {}
        line = (await reader.readline()).strip()
        while line:
            print(line)
            header_key, header_value = line.split(b":", 1)
            header_key = header_key.strip()
            header_value = header_value.strip()
            if header_key in headers:
                if isinstance(headers[header_key], list):
                    headers[header_key].append(header_value)
                else:
                    headers[header_key] = [headers[header_key], header_value]
            else:
                headers[header_key] = header_value

            line = (await reader.readline()).strip()

        # TODO: read body



        return cls(request_line, headers, b"")
