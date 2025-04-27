import requests
import subprocess

VOICEVOX_SERVER_URL = "http://localhost:50021"  # VOICEVOXエンジンのURL
AUDIO_APP = "afplay"

def generate_audio(text: str, output_wav_path: str = "output.wav", speaker_id: int = 1):
    """
    指定したテキストから音声ファイル (wav) を生成する
    """
    # Step1: クエリ作成 (音声合成の設定情報)
    query_payload = {"text": text, "speaker": speaker_id}
    query_response = requests.post(f"{VOICEVOX_SERVER_URL}/audio_query", params=query_payload)

    if query_response.status_code != 200:
        raise Exception(f"audio_query failed: {query_response.text}")

    query = query_response.json()

    # Step2: 音声データを生成
    synthesis_payload = {"speaker": speaker_id}
    synthesis_response = requests.post(
        f"{VOICEVOX_SERVER_URL}/synthesis",
        params=synthesis_payload,
        json=query
    )

    if synthesis_response.status_code != 200:
        raise Exception(f"synthesis failed: {synthesis_response.text}")

    # Step3: WAVファイルに保存
    with open(output_wav_path, "wb") as f:
        f.write(synthesis_response.content)

def play_audio(wav_path: str):
    """
    WAVファイルを再生する
    """
    try:
        subprocess.run([AUDIO_APP, wav_path], check=True)
    except Exception as e:
        print(f"音声再生に失敗しました: {e}")

def speak(text: str, wav_path: str = "output.wav", speaker_id: int = 1):
    generate_audio(text, wav_path, speaker_id)
    play_audio(wav_path)
