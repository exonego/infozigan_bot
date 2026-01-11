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
                    filenames=[
                        f"{DIR_PATH}/ru/LC_MESSAGES/user.ftl",
                        f"{DIR_PATH}/ru/LC_MESSAGES/admin.ftl",
                    ],
                ),
            )
        ],
        root_locale="ru",
    )
