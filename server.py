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
        self.mode = -1
        self.status = comms_pb2.DeviceStatus()
        self.status.led_0.rgba = self.UNSET
        self.status.led_1.rgba = self.UNSET
        self.status.led_2.rgba = self.UNSET
        self.status.led_3.rgba = self.UNSET
        self.status.led_4.rgba = self.UNSET
        self.status.led_5.rgba = self.UNSET
        self.status.button_1 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.status.button_2 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.status.button_3 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.status.button_4 = comms_pb2.DeviceStatus.ButtonStatus.RELEASED
        self.status.battery_level = 100.0
        self.state_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.stop_audio_event = threading.Event()

    # The server send DeviceStatusRequests and expects responses in
    # DeviceStatusResponse
    def StatusStream(self, request_iterator, context):
        # fix the status stream to ask for get before update
        print("StatusStream-----> server")
        while True:
            status = self.state_queue.get()
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
        for request in request_iterator:
            if request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_1:
                print("POWER button pressed")
                self.status.button_1 = request.button_event.event
                yield comms_pb2.DeviceEventResponse(ack=True)
            elif request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_2:
                print("MODE button pressed")
                self.status.button_2 = request.button_event.event
                self.change_mode()
                yield comms_pb2.DeviceEventResponse(ack=True)
            elif request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_3:
                print("STOP button pressed")
                self.status.button_3 = request.button_event.event
                self.status.led_1.rgba = self.UNSET
                self.state_queue.put(self.status)
                self.stop_audio_event.set()
                yield comms_pb2.DeviceEventResponse(ack=True)
            elif request.button_event.button_id == comms_pb2.ButtonEvent.ButtonId.BUTTON_4:
                print("PLAY button pressed")
                self.status.button_4 = request.button_event.event
                self.status.led_1.rgba = self.SET
                self.state_queue.put(self.status)
                self.audio_queue.put(comms_pb2.AudioPacket(is_start=True))
                yield comms_pb2.DeviceEventResponse(ack=True)
            else:
                print("Unknown button pressed")
                yield comms_pb2.DeviceEventResponse(ack=False)

    # The device opens a stream from the server with an AudioStreamRequest and server 
    # streams Opus-encoded audio packets
    def ServerAudioStream(self, request, context):
        print("ServerAudioStream-----> server")
        while True:
            audio_request = self.audio_queue.get()
            if self.mode == 0:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/a.wav", "rb")):
                    yield audio_packet
            elif self.mode == 1:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/b.wav", "rb")):
                    yield audio_packet
            elif self.mode == 2:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/c.wav", "rb")):
                    yield audio_packet
            elif self.mode == 3:
                for audio_packet in self.stream_audio(wave.open("audio_recordings/server/d.wav", "rb")):
                    yield audio_packet

    def change_mode(self):
        print("=== CHANGING MODE ===")
        # print(f"Current LED states: led_2={hex(self.status.led_2.rgba)}, led_3={hex(self.status.led_3.rgba)}, led_4={hex(self.status.led_4.rgba)}, led_5={hex(self.status.led_5.rgba)}")
        self.mode = (self.mode + 1) % self.NUM_MODES
        self.unset_all_leds()
        if self.mode == 0:
            self.status.led_2.rgba = self.SET
            print("Mode 1: LED 2 ON")
        elif self.mode == 1:
            self.status.led_3.rgba = self.SET
            print("Mode 2: LED 3 ON")
        elif self.mode == 2:
            self.status.led_4.rgba = self.SET
            print("Mode 3: LED 4 ON")
        elif self.mode == 3:
            self.status.led_5.rgba = self.SET
            print("Mode 4: LED 5 ON")
        elif self.mode == 4:
            self.status.led_2.rgba = self.SET
            print("Mode 5: Back to LED 2 ON")
        self.state_queue.put(self.status)

    def unset_all_leds(self):
        self.status.led_0.rgba = self.UNSET
        self.status.led_1.rgba = self.UNSET
        self.status.led_2.rgba = self.UNSET
        self.status.led_3.rgba = self.UNSET
        self.status.led_4.rgba = self.UNSET
        self.status.led_5.rgba = self.UNSET

    def stream_audio(self, wave_file):
        opus_coder = OpusCoder(sample_rate=self.SAMPLE_RATE, channels=self.CHANNELS)
        frame_size = self.FRAME_SIZE
        first_packet = True
        bytes_per_frame = frame_size * wave_file.getsampwidth() * wave_file.getnchannels()
        while True:
            # Check for stop event before processing each frame
            if self.stop_audio_event.is_set():
                self.stop_audio_event.clear()
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
