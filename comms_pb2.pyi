from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RGBAColor(_message.Message):
    __slots__ = ("rgba",)
    RGBA_FIELD_NUMBER: _ClassVar[int]
    rgba: int
    def __init__(self, rgba: _Optional[int] = ...) -> None: ...

class DeviceStatus(_message.Message):
    __slots__ = ("led_0", "led_1", "led_2", "led_3", "led_4", "led_5", "button_1", "button_2", "button_3", "button_4", "battery_level")
    class ButtonStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESSED: _ClassVar[DeviceStatus.ButtonStatus]
        RELEASED: _ClassVar[DeviceStatus.ButtonStatus]
    PRESSED: DeviceStatus.ButtonStatus
    RELEASED: DeviceStatus.ButtonStatus
    LED_0_FIELD_NUMBER: _ClassVar[int]
    LED_1_FIELD_NUMBER: _ClassVar[int]
    LED_2_FIELD_NUMBER: _ClassVar[int]
    LED_3_FIELD_NUMBER: _ClassVar[int]
    LED_4_FIELD_NUMBER: _ClassVar[int]
    LED_5_FIELD_NUMBER: _ClassVar[int]
    BUTTON_1_FIELD_NUMBER: _ClassVar[int]
    BUTTON_2_FIELD_NUMBER: _ClassVar[int]
    BUTTON_3_FIELD_NUMBER: _ClassVar[int]
    BUTTON_4_FIELD_NUMBER: _ClassVar[int]
    BATTERY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    led_0: RGBAColor
    led_1: RGBAColor
    led_2: RGBAColor
    led_3: RGBAColor
    led_4: RGBAColor
    led_5: RGBAColor
    button_1: DeviceStatus.ButtonStatus
    button_2: DeviceStatus.ButtonStatus
    button_3: DeviceStatus.ButtonStatus
    button_4: DeviceStatus.ButtonStatus
    battery_level: float
    def __init__(self, led_0: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_1: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_2: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_3: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_4: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_5: _Optional[_Union[RGBAColor, _Mapping]] = ..., button_1: _Optional[_Union[DeviceStatus.ButtonStatus, str]] = ..., button_2: _Optional[_Union[DeviceStatus.ButtonStatus, str]] = ..., button_3: _Optional[_Union[DeviceStatus.ButtonStatus, str]] = ..., button_4: _Optional[_Union[DeviceStatus.ButtonStatus, str]] = ..., battery_level: _Optional[float] = ...) -> None: ...

class DeviceStatusSet(_message.Message):
    __slots__ = ("led_0", "led_1", "led_2", "led_3", "led_4", "led_5")
    LED_0_FIELD_NUMBER: _ClassVar[int]
    LED_1_FIELD_NUMBER: _ClassVar[int]
    LED_2_FIELD_NUMBER: _ClassVar[int]
    LED_3_FIELD_NUMBER: _ClassVar[int]
    LED_4_FIELD_NUMBER: _ClassVar[int]
    LED_5_FIELD_NUMBER: _ClassVar[int]
    led_0: RGBAColor
    led_1: RGBAColor
    led_2: RGBAColor
    led_3: RGBAColor
    led_4: RGBAColor
    led_5: RGBAColor
    def __init__(self, led_0: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_1: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_2: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_3: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_4: _Optional[_Union[RGBAColor, _Mapping]] = ..., led_5: _Optional[_Union[RGBAColor, _Mapping]] = ...) -> None: ...

class DeviceStatusRequest(_message.Message):
    __slots__ = ("get", "set")
    GET_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    get: bool
    set: DeviceStatusSet
    def __init__(self, get: bool = ..., set: _Optional[_Union[DeviceStatusSet, _Mapping]] = ...) -> None: ...

class DeviceStatusResponse(_message.Message):
    __slots__ = ("state", "status")
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    state: DeviceStatus
    status: str
    def __init__(self, state: _Optional[_Union[DeviceStatus, _Mapping]] = ..., status: _Optional[str] = ...) -> None: ...

class ButtonEvent(_message.Message):
    __slots__ = ("button_id", "event")
    class ButtonId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BUTTON_1: _ClassVar[ButtonEvent.ButtonId]
        BUTTON_2: _ClassVar[ButtonEvent.ButtonId]
        BUTTON_3: _ClassVar[ButtonEvent.ButtonId]
        BUTTON_4: _ClassVar[ButtonEvent.ButtonId]
    BUTTON_1: ButtonEvent.ButtonId
    BUTTON_2: ButtonEvent.ButtonId
    BUTTON_3: ButtonEvent.ButtonId
    BUTTON_4: ButtonEvent.ButtonId
    class ButtonEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESS: _ClassVar[ButtonEvent.ButtonEventType]
        HOLD: _ClassVar[ButtonEvent.ButtonEventType]
        RELEASE: _ClassVar[ButtonEvent.ButtonEventType]
    PRESS: ButtonEvent.ButtonEventType
    HOLD: ButtonEvent.ButtonEventType
    RELEASE: ButtonEvent.ButtonEventType
    BUTTON_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    button_id: ButtonEvent.ButtonId
    event: ButtonEvent.ButtonEventType
    def __init__(self, button_id: _Optional[_Union[ButtonEvent.ButtonId, str]] = ..., event: _Optional[_Union[ButtonEvent.ButtonEventType, str]] = ...) -> None: ...

class DeviceEvent(_message.Message):
    __slots__ = ("button_event",)
    BUTTON_EVENT_FIELD_NUMBER: _ClassVar[int]
    button_event: ButtonEvent
    def __init__(self, button_event: _Optional[_Union[ButtonEvent, _Mapping]] = ...) -> None: ...

class DeviceEventResponse(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: bool
    def __init__(self, ack: bool = ...) -> None: ...

class AudioStreamRequest(_message.Message):
    __slots__ = ("start",)
    START_FIELD_NUMBER: _ClassVar[int]
    start: bool
    def __init__(self, start: bool = ...) -> None: ...

class AudioPacket(_message.Message):
    __slots__ = ("is_start", "is_end", "data")
    IS_START_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    is_start: bool
    is_end: bool
    data: bytes
    def __init__(self, is_start: bool = ..., is_end: bool = ..., data: _Optional[bytes] = ...) -> None: ...
