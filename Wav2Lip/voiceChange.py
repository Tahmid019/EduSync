from pydub import AudioSegment
import os

def convert_female_to_male(audio_file, pitch_shift=-7, bass_boost_db=8, speedup_factor=1.4):
    # Loading the audio file
    audio = AudioSegment.from_file(audio_file)

    # Adjusting pitch (down by 5 semitones)
    pitch_shifted = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * (2 ** (pitch_shift / 12)))
    }).set_frame_rate(audio.frame_rate)

    # Equalization - Boosting low frequencies and cutting high frequencies
    eq_adjusted = pitch_shifted.low_pass_filter(600).high_pass_filter(20)
    eq_adjusted = eq_adjusted.high_pass_filter(3000).apply_gain(6)

    # Adjusting bass
    bass_adjusted = eq_adjusted.apply_gain(bass_boost_db)

    # Compression to make the voice more consistent
    compressed = bass_adjusted.compress_dynamic_range()

    # Adding slight reverb for presence (simulated with echo)
    reverb_adjusted = compressed + compressed.reverse().fade_in(50).fade_out(50).reverse()

    # Speed adjustment
    sped_up = compressed.speedup(playback_speed=speedup_factor)

     # Normalization
    normalized = sped_up.normalize()

    return normalized

def save_audio(audio, output_file):
    audio.export(output_file, format="wav")
    print(f"Converted audio saved to {output_file}")

def main():
    # Input audio file
    input_file = "/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/HINDI_PALL_23S.wav"

    # Output audio file
    output_file = "male_voice.wav"

    # Converting female voice to male
    converted_audio = convert_female_to_male(input_file)

    # Saving converted audio
    save_audio(converted_audio, output_file)

    # Play converted audio (Windows)
    os.system(f"start {output_file}")
    print(">>>complete<<<<")
    
main()