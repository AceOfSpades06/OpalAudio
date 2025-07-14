import os
import wave
import grpc
from audio import OpusCoder
import comms_pb2
import comms_pb2_grpc
import queue
from concurrent import futures
import threading

class DeviceServiceServicer(comms_pb2_grpc.DeviceServiceServicer):
    SET = 0xFFFFFFFF
    UNSET = 0x00000000
    SAMPLE_RATE = 48000
    CHANNELS = 1
    FRAME_SIZE = 960
    NUM_MODES = 4
    def __init__(self):
        self.devices = {}
        self.stop_audio_event = {}

    # The server send DeviceStatusRequests and expects responses in
    # DeviceStatusResponse
    def StatusStream(self, request_iterator, context):
        # fix the status stream to ask for get before update
        print("StatusStream-----> server")
        device_id = self._get_device_id(context)
        if device_id not in self.devices:
            self.setup_device(device_id)
        while context.is_active():
            status = self.devices[device_id]["state_q"].get()
            # print("mode queue received: " + str(status))
            yield comms_pb2.DeviceStatusRequest(
                set=comms_pb2.DeviceStatusSet(
                    led_0=status.led_0, 
                    led_1=status.led_1, 
                    led_2=status.led_2, 
                    led_3=status.led_3, 
                    led_4=status.led_4, 
                    led_5=status.led_5))
        # for request in request_iterator:
        #     print(f"StatusStream received: {request}")
        #     if request.status == "SUCCESS":
        #         yield comms_pb2.DeviceStatusRequest(get=True)
        #     else:
        #         self.status.led_1 = request.status.led_1
        #         self.status.led_2 = request.status.led_2
        #         self.status.led_3 = request.status.led_3
        #         self.status.led_4 = request.status.led_4
        #         self.status.led_5 = request.status.led_5
        #         yield comms_pb2.DeviceStatusRequest(set=self.status)

    # The device streams DeviceEvents(s) and expects a DeviceEventResponse to ACK
    def EventStream(self, request_iterator, context):
        print("EventStream-----> server")
        device_id = self._get_device_id(context)
        for request in request_iterator:
            if device_id not in self.devices:
                self.setup_device(device_id)
            if request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_1:
                print("POWER button pressed")
                self.devices[device_id]["status"].button_1 = request.button_event.event
                yield comms_pb2.DeviceEventResponse(ack=True)
            elif request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_2:
                print("MODE button pressed")
                self.devices[device_id]["status"].button_2 = request.button_event.event
                self.change_mode(device_id)
                yield comms_pb2.DeviceEventResponse(ack=True)
            elif request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_3:
                print("STOP button pressed")
                self.devices[device_id]["status"].button_3 = request.button_event.event
                self.devices[device_id]["status"].led_1.rgba = self.UNSET
                self.devices[device_id]["state_q"].put(self.devices[device_id]["status"])
                self.stop_audio_event[device_id].set()
                yield comms_pb2.DeviceEventResponse(ack=True)
            elif request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_4:
                print("PLAY button pressed")
                self.devices[device_id]["status"].button_4 = request.button_event.event
                self.devices[device_id]["status"].led_1.rgba = self.SET
                self.devices[device_id]["state_q"].put(self.devices[device_id]["status"])
                self.devices[device_id]["audio_q"].put(comms_pb2.AudioPacket(is_start=True))
                yield comms_pb2.DeviceEventResponse(ack=True)
            else:
                print("Unknown button pressed")
                yield comms_pb2.DeviceEventResponse(ack=False)

    # The device opens a stream from the server with an AudioStreamRequest and server 
    # streams Opus-encoded audio packets
    def ServerAudioStream(self, request, context):
        print("ServerAudioStream-----> server")
        device_id = self._get_device_id(context)
        if device_id not in self.devices:
            self.setup_device(device_id)
        while True:
            audio_request = self.devices[device_id]["audio_q"].get()
            if self.devices[device_id]["mode"] == 0:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/a.wav", "rb"), device_id):
                    yield audio_packet
            elif self.devices[device_id]["mode"] == 1:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/b.wav", "rb"), device_id):
                    yield audio_packet
            elif self.devices[device_id]["mode"] == 2:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/c.wav", "rb"), device_id):
                    yield audio_packet
            elif self.devices[device_id]["mode"] == 3:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/d.wav", "rb"), device_id):
                    yield audio_packet

    def change_mode(self, device_id):
        print("=== CHANGING MODE ===")
        self.devices[device_id]["mode"] = (self.devices[device_id]["mode"] + 1) % self.NUM_MODES
        self.unset_all_leds(device_id)
        if self.devices[device_id]["mode"] == 0:
            self.devices[device_id]["status"].led_2.rgba = self.SET
            print("Mode 1: LED 2 ON")
        elif self.devices[device_id]["mode"] == 1:
            self.devices[device_id]["status"].led_3.rgba = self.SET
            print("Mode 2: LED 3 ON")
        elif self.devices[device_id]["mode"] == 2:
            self.devices[device_id]["status"].led_4.rgba = self.SET
            print("Mode 3: LED 4 ON")
        elif self.devices[device_id]["mode"] == 3:
            self.devices[device_id]["status"].led_5.rgba = self.SET
            print("Mode 4: LED 5 ON")
        self.devices[device_id]["state_q"].put(self.devices[device_id]["status"])

    def unset_all_leds(self, device_id):
        self.devices[device_id]["status"].led_0.rgba = self.UNSET
        self.devices[device_id]["status"].led_1.rgba = self.UNSET
        self.devices[device_id]["status"].led_2.rgba = self.UNSET
        self.devices[device_id]["status"].led_3.rgba = self.UNSET
        self.devices[device_id]["status"].led_4.rgba = self.UNSET
        self.devices[device_id]["status"].led_5.rgba = self.UNSET

    def _get_device_id(self, context) -> str:
        return dict(context.invocation_metadata()).get("device_id", "unknown")

    def setup_device(self, device_id):
        # lock the dic so that only one thread can access it
        self.devices[device_id] = {
            "status": comms_pb2.DeviceStatus(),
            "state_q": queue.Queue(),
            "audio_q": queue.Queue(),
            "mode": -1,
        }
        # per-device stop flag
        self.stop_audio_event[device_id] = threading.Event()
        self.devices[device_id]["status"].led_0.rgba = self.UNSET
        self.devices[device_id]["status"].led_1.rgba = self.UNSET
        self.devices[device_id]["status"].led_2.rgba = self.UNSET
        self.devices[device_id]["status"].led_3.rgba = self.UNSET
        self.devices[device_id]["status"].led_4.rgba = self.UNSET
        self.devices[device_id]["status"].led_5.rgba = self.UNSET
        self.devices[device_id]["status"].button_1 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.devices[device_id]["status"].button_2 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.devices[device_id]["status"].button_3 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.devices[device_id]["status"].button_4 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.devices[device_id]["status"].battery_level = 100.0

    def stream_audio(self, wave_file, device_id):
        opus_coder = OpusCoder(sample_rate=self.SAMPLE_RATE, channels=self.CHANNELS)
        frame_size = self.FRAME_SIZE
        first_packet = True
        bytes_per_frame = frame_size * wave_file.getsampwidth() * wave_file.getnchannels()
        while True:
            # Check for stop event before processing each frame
            if self.stop_audio_event[device_id].is_set():
                self.stop_audio_event[device_id].clear()
                print("Stream audio interrupted by stop event")
                return
                
            pcm_data = wave_file.readframes(frame_size)
            if len(pcm_data) == 0:
                break
            if len(pcm_data) < bytes_per_frame:
                pcm_data += b"\x00" * (bytes_per_frame - len(pcm_data))
            opus_data = opus_coder.encode(pcm_data)
            yield comms_pb2.AudioPacket(is_start=first_packet, 
                                        is_end=False,
                                        data=bytes(opus_data))
            first_packet = False
        yield comms_pb2.AudioPacket(is_start=False, is_end=True)


def serve():
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comms_pb2_grpc.add_DeviceServiceServicer_to_server(DeviceServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, stopping server")
        server.stop(0)
        os._exit(0)



if __name__ == "__main__":
    serve()
