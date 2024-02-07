#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses

from enum import Enum


class CustomCodeBase(Enum):
    """Custom status code base class"""

    @property
    def code(self):
        """
        Get status code
        """
        return self.value[0]

    @property
    def msg(self):
        """
        Get status codeInformation
        """
        return self.value[1]


class CustomResponseCode(CustomCodeBase):
    """Custom response status code"""

    HTTP_200 = (200, 'Request succeeded')
    HTTP_201 = (201, 'newRequest succeeded')
    HTTP_202 = (202, 'Request Accepted,But the processing is not yet complete.')
    HTTP_204 = (204, 'Request succeeded,No content returned.')
    HTTP_400 = (400, 'Request error')
    HTTP_401 = (401, 'unauthorized')
    HTTP_403 = (403, 'Prohibited access')
    HTTP_404 = (404, 'The requested resource does not exist.')
    HTTP_410 = (410, 'The requested resource has been permanently deleted.')
    HTTP_422 = (422, 'Illegal request parameters')
    HTTP_425 = (425, 'Unable to execute request.,because')
    HTTP_429 = (429, 'Too many requests,Server restrictions')
    HTTP_500 = (500, 'Internal server error')
    HTTP_502 = (502, 'Gateway error')
    HTTP_503 = (503, 'Server temporarily unable to process request')
    HTTP_504 = (504, 'Gateway timeout')


class CustomErrorCode(CustomCodeBase):
    """Custom error status code"""

    CAPTCHA_ERROR = (40001, 'Verification code error.')


@dataclasses.dataclass
class CustomResponse:
    """
    provide,rather than enumeration,If you want to customize response information,This could be very useful.
    """

    code: int
    msg: str


class StandardResponseCode:
    """Standard response status code"""

    """
    HTTP codes
    See HTTP Status Code Registry:
    https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

    And RFC 2324 - https://tools.ietf.org/html/rfc2324
    """
    HTTP_100 = 100  # CONTINUE: Continue.
    HTTP_101 = 101  # SWITCHING_PROTOCOLS: Agreement Switching
    HTTP_102 = 102  # PROCESSING: processing
    HTTP_103 = 103  # EARLY_HINTS: Prompt information
    HTTP_200 = 200  # OK: Request succeeded
    HTTP_201 = 201  # CREATED: Created
    HTTP_202 = 202  # ACCEPTED: Accepted
    HTTP_203 = 203  # NON_AUTHORITATIVE_INFORMATION: Non-authoritative information
    HTTP_204 = 204  # NO_CONTENT: no content
    HTTP_205 = 205  # RESET_CONTENT: reset
    HTTP_206 = 206  # PARTIAL_CONTENT: Some content
    HTTP_207 = 207  # MULTI_STATUS: Multiple statuses
    HTTP_208 = 208  # ALREADY_REPORTED: reported
    HTTP_226 = 226  # IM_USED: used
    HTTP_300 = 300  # MULTIPLE_CHOICES: Multiple choices
    HTTP_301 = 301  # MOVED_PERMANENTLY: permanent move
    HTTP_302 = 302  # FOUND: temporary move
    HTTP_303 = 303  # SEE_OTHER: View other locations.
    HTTP_304 = 304  # NOT_MODIFIED: Not modified.
    HTTP_305 = 305  # USE_PROXY: use, employ, utilize
    HTTP_307 = 307  # TEMPORARY_REDIRECT: temporary redirection
    HTTP_308 = 308  # PERMANENT_REDIRECT: Permanent redirection
    HTTP_400 = 400  # BAD_REQUEST: Request error
    HTTP_401 = 401  # UNAUTHORIZED: unauthorized
    HTTP_402 = 402  # PAYMENT_REQUIRED: need
    HTTP_403 = 403  # FORBIDDEN: Prohibited access
    HTTP_404 = 404  # NOT_FOUND: not found
    HTTP_405 = 405  # METHOD_NOT_ALLOWED: Method not allowed
    HTTP_406 = 406  # NOT_ACCEPTABLE: unacceptable
    HTTP_407 = 407  # PROXY_AUTHENTICATION_REQUIRED: Proxy authentication is required.
    HTTP_408 = 408  # REQUEST_TIMEOUT: Request timeout
    HTTP_409 = 409  # CONFLICT: Conflict
    HTTP_410 = 410  # GONE: Deleted
    HTTP_411 = 411  # LENGTH_REQUIRED: Content Length
    HTTP_412 = 412  # PRECONDITION_FAILED: Prerequisite failure
    HTTP_413 = 413  # REQUEST_ENTITY_TOO_LARGE: Request entity too large
    HTTP_414 = 414  # REQUEST_URI_TOO_LONG: Request URI Too long
    HTTP_415 = 415  # UNSUPPORTED_MEDIA_TYPE: Unsupported media type
    HTTP_416 = 416  # REQUESTED_RANGE_NOT_SATISFIABLE: RequestRange does not meet requirements
    HTTP_417 = 417  # EXPECTATION_FAILED: Expectation failure
    HTTP_418 = 418  # UNUSED: Idle
    HTTP_421 = 421  # MISDIRECTED_REQUEST: misguidedRequest
    HTTP_422 = 422  # UNPROCESSABLE_CONTENT: Unable to process entity.
    HTTP_423 = 423  # LOCKED: Locked
    HTTP_424 = 424  # FAILED_DEPENDENCY: Dependency failure
    HTTP_425 = 425  # TOO_EARLY: Too early
    HTTP_426 = 426  # UPGRADE_REQUIRED: need
    HTTP_427 = 427  # UNASSIGNED: Unallocated
    HTTP_428 = 428  # PRECONDITION_REQUIRED: precondition
    HTTP_429 = 429  # TOO_MANY_REQUESTS: Too many requests
    HTTP_430 = 430  # Unassigned: Unallocated
    HTTP_431 = 431  # REQUEST_HEADER_FIELDS_TOO_LARGE: Requesthead field too big
    HTTP_451 = 451  # UNAVAILABLE_FOR_LEGAL_REASONS: Unavailable due to legal reasons.
    HTTP_500 = 500  # INTERNAL_SERVER_ERROR: Internal server error
    HTTP_501 = 501  # NOT_IMPLEMENTED: Not achieved
    HTTP_502 = 502  # BAD_GATEWAY: Wrong gateway
    HTTP_503 = 503  # SERVICE_UNAVAILABLE: Service unavailable
    HTTP_504 = 504  # GATEWAY_TIMEOUT: Gateway timeout
    HTTP_505 = 505  # HTTP_VERSION_NOT_SUPPORTED: HTTP Version not supported
    HTTP_506 = 506  # VARIANT_ALSO_NEGOTIATES: variant
    HTTP_507 = 507  # INSUFFICIENT_STORAGE: Insufficient storage space
    HTTP_508 = 508  # LOOP_DETECTED: Detected loop
    HTTP_509 = 509  # UNASSIGNED: Unallocated
    HTTP_510 = 510  # NOT_EXTENDED: Not expanded.
    HTTP_511 = 511  # NETWORK_AUTHENTICATION_REQUIRED: Need network authentication.

    """
    WebSocket codes
    https://www.iana.org/assignments/websocket/websocket.xml#close-code-number
    https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent
    """
    WS_1000 = 1000  # NORMAL_CLOSURE: Normal closure
    WS_1001 = 1001  # GOING_AWAY: Leaving.
    WS_1002 = 1002  # PROTOCOL_ERROR: Agreement error
    WS_1003 = 1003  # UNSUPPORTED_DATA: Unsupported data type
    WS_1005 = 1005  # NO_STATUS_RCVD: Did not receive the status.
    WS_1006 = 1006  # ABNORMAL_CLOSURE: Unexpected Shutdown
    WS_1007 = 1007  # INVALID_FRAME_PAYLOAD_DATA: Invalid frame payload data
    WS_1008 = 1008  # POLICY_VIOLATION: Violation
    WS_1009 = 1009  # MESSAGE_TOO_BIG: The message is too big."
    WS_1010 = 1010  # MANDATORY_EXT: essential expansion
    WS_1011 = 1011  # INTERNAL_ERROR: Internal error
    WS_1012 = 1012  # SERVICE_RESTART: Service restart
    WS_1013 = 1013  # TRY_AGAIN_LATER: Please try again later.
    WS_1014 = 1014  # BAD_GATEWAY: Wrong gateway
    WS_1015 = 1015  # TLS_HANDSHAKE: TLShandshake error
    WS_3000 = 3000  # UNAUTHORIZED: unauthorized
    WS_3003 = 3003  # FORBIDDEN: Prohibited access
