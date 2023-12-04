from typing import Optional, List
import wave
import io
import requests
from voice_class import CharacterVoice


class VoiceGenerator:

    def __init__(self) -> None:
        self.url: str = 'https://genshinvoice.top/api'
        self.headers: dict = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        }
        self.max_text_length: int = 80  # 设定最大文本长度

    def generate_voice(self,
                       text: str,
                       speaker: str = '埃德_ZH',
                       format: str = 'wav',
                       language: str = 'ZH',
                       length: str = '1',
                       sdp: str = '0.4',
                       noise: str = '0.6',
                       noisew: str = '0.8') -> Optional[bytes]:
        params: dict = {
            'speaker': speaker,
            'text': text,
            'format': format,
            'language': language,
            'length': length,
            'sdp': sdp,
            'noise': noise,
            'noisew': noisew,
        }

        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code}")
            return None

    def save_voice_to_file(self,
                           text: str,
                           filename: str = 'generated_voiceall.wav',
                           **kwargs: str) -> None:
        if len(text) > self.max_text_length:
            split_texts = [
                text[i:i + self.max_text_length]
                for i in range(0, len(text), self.max_text_length)
            ]
            combined_voice_data: List[bytes] = []
            for split_text in split_texts:
                voice_data = self.generate_voice(split_text, **kwargs)
                if voice_data:
                    combined_voice_data.append(voice_data)
                else:
                    print(f"Failed to generate voice for '{split_text}'")
                    return

            temp_index = 0

            wav_binaries = []

            for bin_data in combined_voice_data:
                wav_binary = io.BytesIO(bin_data)  # 将二进制字符串转换为 BytesIO 对象
                wav_binaries.append(wav_binary)

            with wave.open(filename, 'wb') as output_wav:
                # 假设所有文件都具有相同的参数，这里以第一个文件的参数为准
                output_wav.setparams(wave.open(wav_binaries[0]).getparams())

                for wav_data in wav_binaries:
                    output_wav.writeframesraw(wav_data.read())

                # with open(str(temp_index) + filename, 'wb') as f:
                #     f.write(voice_data)
            print(f"Voice generated and saved as '{filename}'")
        else:
            voice_data: Optional[bytes] = self.generate_voice(text, **kwargs)
            if voice_data:
                with open(filename, 'wb') as f:
                    f.write(voice_data)
                print(f"Voice generated and saved as '{filename}'")
            else:
                print("Voice generation failed.")


# Example usage:
if __name__ == "__main__":
    generator: VoiceGenerator = VoiceGenerator()
    info_txt = """
    我爱昆仑山搭街坊卡拉杀了开发商的JFK了
    """
    generator.save_voice_to_file(info_txt,
                                 speaker=CharacterVoice.派蒙_ZH.name,
                                 format='wav',
                                 language='ZH',
                                 length='1',
                                 sdp='0.4',
                                 noise='0.6',
                                 noisew='0.8')
