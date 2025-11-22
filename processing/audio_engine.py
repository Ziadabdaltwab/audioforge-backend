import librosa, soundfile as sf, subprocess, os
from pydub import AudioSegment, effects
from rnnoise import RNNoise

def apply_rnnoise(input_wav, output_wav):
    rn = RNNoise()
    data, sr = sf.read(input_wav)
    cleaned = [rn.filter(frame) for frame in data]
    sf.write(output_wav, cleaned, sr)

def spectral_gate(input_path, output_path):
    y, sr = librosa.load(input_path, sr=None)
    spectral = librosa.effects.preemphasis(y)
    sf.write(output_path, spectral, sr)

def loudness_normalize(path):
    audio = AudioSegment.from_file(path)
    effects.normalize(audio).export(path, format=path.split('.')[-1])

def convert_to_wav(inp, out):
    subprocess.run(["ffmpeg","-y","-i",inp,out],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def convert_from_wav(inp, out):
    subprocess.run(["ffmpeg","-y","-i",inp,out],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def process_audio(input_path, output_path):
    t1,t2,t3="temp_in.wav","temp_rn.wav","temp_gate.wav"
    convert_to_wav(input_path,t1)
    apply_rnnoise(t1,t2)
    spectral_gate(t2,t3)
    loudness_normalize(t3)
    convert_from_wav(t3,output_path)
    for t in (t1,t2,t3):
        if os.path.exists(t): os.remove(t)
