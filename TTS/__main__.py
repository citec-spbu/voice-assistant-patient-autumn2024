import argparse

from speakerpy.lib_speak import Speaker

def vocalize(text, pronounce):
    speaker = Speaker(model_id="v3_1_ru", language="ru", speaker="xenia", device="cpu")

    if pronounce:
        speaker.speak(text=text, sample_rate=48000, speed=1.2)
    else:
        speaker.to_mp3(text=text, name_text="Текст", sample_rate=48000, audio_dir="./mp3")

def main(args):
    pronounce = args.pronounce if args.pronounce else True
    vocalize(args.text, pronounce)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--text",
        required=True,
        help=f"Текст для озвучивания",
    )
    parser.add_argument(
        "-p",
        "--pronounce",
        required=False,
        help=f"Произнести? Иначе текст будет записан в mp3 файл",
    )

    args = parser.parse_args()
    main(args)