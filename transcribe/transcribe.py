import os
import azure.cognitiveservices.speech as speechsdk
import json

from annotate_transcriptions import annotate_stopwords_in_json_dir

def synthesize_with_word_boundaries(text, name):
    """
    Synthesizes speech from plain text, saves audio as MP3 and word boundary timings as JSON.
    Args:
        text (str): The plain text to synthesize.
        name (str): The base name for the output files (no extension).
    Returns:
        Tuple of (audio_path, timing_path)
    """
    # Load Azure keys from .keys file
    with open(os.path.join(os.path.dirname(__file__), ".keys")) as keyfile:
        keys = json.load(keyfile)
        speech_key = keys["speech_key"]
        speech_region = keys["speech_region"]

    audio_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../client/assets/audio")
    )
    timing_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../client/assets/transcripts")
    )
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(timing_folder, exist_ok=True)

    audio_path = os.path.join(audio_folder, f"{name}.mp3")
    timing_path = os.path.join(timing_folder, f"{name}.json")

    # Build SSML from plain text
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
      <voice name="en-US-AvaMultilingualNeural">
        {text}
      </voice>
    </speak>
    """

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.set_property(
        property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestWordBoundary,
        value="true",
    )
    speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    word_boundaries = []

    def word_boundary_event(evt: speechsdk.SpeechSynthesisWordBoundaryEventArgs):
        def to_seconds(val):
            try:
                return val.total_seconds()
            except AttributeError:
                return val / 10000000 if isinstance(val, (int, float)) else float(val)

        info = {
            "text": evt.text,
            "audio_offset": to_seconds(evt.audio_offset),
            "duration": to_seconds(evt.duration),
            "boundary_type": str(evt.boundary_type),
        }
        word_boundaries.append(info)
        print(
            f"WordBoundaryEvent: Text='{evt.text}', AudioOffset={info['audio_offset']:.2f}s, Duration={info['duration']:.2f}s, BoundaryType={info['boundary_type']}"
        )

    speech_synthesizer.synthesis_word_boundary.connect(word_boundary_event)
    result = speech_synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    with open(timing_path, "w") as f:
        json.dump(word_boundaries, f, indent=2)
    print(f"Saved word boundaries to {timing_path}")
    print(f"Saved synthesized audio to {audio_path}")
    return audio_path, timing_path


if __name__ == "__main__":
    sources_dir = os.path.join(os.path.dirname(__file__), "sources")
    for fname in os.listdir(sources_dir):
        if fname.endswith(".txt"):
            name = os.path.splitext(fname)[0]
            print(f"Processing {name}...")
            with open(os.path.join(sources_dir, fname), "r") as f:
                text = f.read()
            audio_folder = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../client/assets/audio")
            )
            timing_folder = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../client/assets/transcripts")
            )
            audio_path = os.path.join(audio_folder, f"{name}.mp3")
            timing_path = os.path.join(timing_folder, f"{name}.json")
            if os.path.exists(audio_path) and os.path.exists(timing_path):
                print(
                    f"Skipping synthesis: {audio_path} and {timing_path} already exist."
                )
            else:
                synthesize_with_word_boundaries(text, name)

    # Annotate stopwords after synthesis
    annotate_stopwords_in_json_dir(timing_folder)
