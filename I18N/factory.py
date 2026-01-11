from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator

DIR_PATH = "I18N/locales"


def i18n_factory() -> TranslatorHub:
    return TranslatorHub(
        {"ru": ("ru",)},
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru",
                    filenames=[],
                ),
            )
        ],
        root_locale="ru",
    )
