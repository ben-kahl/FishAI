from pvrecorder import PvRecorder


def list_devices():
    devices = PvRecorder.get_available_devices()
    for index, device in enumerate(devices):
        print(f"Index: {index}, Device: {device}")


if __name__ == "__main__":
    list_devices()
