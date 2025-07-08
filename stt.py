import pvleopard

leopard = pvleopard.create(access_key='${ACCESS_KEY}')


def get_audio_data():
    pass


def listen():
    transcript, words = leopard.process(get_audio_data())
    print(transcript)
