from googletrans import (
    Translator,
)


class TranslatorService:

    def __init__(self):
        self.translator = Translator()

    def translate(
            self,
            text: str,
            original_language_identifier: str = 'auto',
            target_language_identifier: str = 'ru',
    ):

        if not text:
            return None

        translated_text = self.translator.translate(
            text=text,
            src=original_language_identifier,
            dest=target_language_identifier,
        )

        return translated_text.text
