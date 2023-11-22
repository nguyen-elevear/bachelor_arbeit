from pydub import AudioSegment

def crop_audio(input_file, output_file, start_time, duration):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)

    # Crop the audio
    cropped_audio = audio[start_time:start_time+duration]

    # Export the cropped audio
    cropped_audio.export(output_file, format="wav")

# Usage
input_file = "tonal_wind.wav"
output_file = "wind_tonal.wav"
start_time = 0 * 1000  # start at the beginning (in milliseconds)
duration = 30 * 1000  # 30 seconds (in milliseconds)

crop_audio(input_file, output_file, start_time, duration)