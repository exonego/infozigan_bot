from decimal import Decimal
from typing import Literal

from fluent_compiler.types import FluentType
from typing_extensions import TypeAlias

PossibleValue: TypeAlias = str | int | float | Decimal | bool | FluentType

class TranslatorRunner:
    def get(self, path: str, **kwargs: PossibleValue) -> str: ...
    menu: Menu
    successful: Successful
    admin: Admin

class MenuButtonPay:
    @staticmethod
    def club(*, price: PossibleValue) -> Literal["""🟢 Получить доступ { $price } ₽"""]: ...
    @staticmethod
    def mentor(*, price: PossibleValue) -> Literal["""🆕 Доступ + Наставничество { $price } ₽"""]: ...

class MenuButton:
    pay: MenuButtonPay

    @staticmethod
    def description() -> Literal["""📔 Начать обучение"""]: ...
    @staticmethod
    def guides() -> Literal["""🆓 Забрать гайды"""]: ...

class MenuInvoiceClub:
    @staticmethod
    def member() -> Literal["""🎉 Поздравляю! Ты уже состоишь в клубе."""]: ...
    @staticmethod
    def admin() -> Literal["""🤔 Похоже, ты администратор клуба."""]: ...
    @staticmethod
    def kicked() -> Literal["""☹️ К сожалению, ты был(а) исключен(а) из клуба."""]: ...
    @staticmethod
    def leave(*, username: PossibleValue) -> Literal["""😅 Похоже, ты случайно вышел/вышла из клуба. Чтобы вступить заново, напиши { $username }"""]: ...
    @staticmethod
    def title() -> Literal["""Участие в клубе"""]: ...
    @staticmethod
    def description() -> Literal["""🤖 Клубное обучение системной работе с нейро генерациями, монтаж вирусных роликов и как заработать на нейронках в 2026 году."""]: ...

class MenuInvoiceMentor:
    @staticmethod
    def member(*, price: PossibleValue) -> Literal["""Так как ты состоишь в клубе, цена для тебя составит { $price } ₽"""]: ...
    @staticmethod
    def mentor(*, username: PossibleValue) -> Literal["""🎉 Поздравляю! Ты уже состоишь в клубе, по всем вопросам пиши { $username }"""]: ...
    @staticmethod
    def title() -> Literal["""Клуб + Наставничество"""]: ...
    @staticmethod
    def description() -> Literal["""Клубное обучение + Личное наставничество"""]: ...

class MenuInvoice:
    club: MenuInvoiceClub
    mentor: MenuInvoiceMentor

class Menu:
    button: MenuButton
    invoice: MenuInvoice

    @staticmethod
    def text() -> Literal["""&lt;b&gt;👋 Привет. Я Валя Нейро, умный бот нейро креатора.&lt;/b&gt;

🔥 Ты заинтересовался(лась) нейросетями, и правильно сделал(а).
🏆 В ближайшие 5-10 лет Искусственный интеллект будет в топе и специалисты, умеющие работать с ним, будут очень востребованы.
❗️ Поэтому залетай в наше клубное сообщество и прокачивай свои навыки."""]: ...
    @staticmethod
    def description(*, club_price: PossibleValue, mentor_price: PossibleValue) -> Literal["""Я собрала простой пошаговый клуб, где ты с нуля начинаешь делать креативы в нейросетях и монетизировать навык.  
Мои ученики стартовали с нуля и уже берут заказы от 3 000 до 50 000 ₽ за один.

👉🏻 Внутри клуба ты:
• научишься создавать нейрофотосессии, карточки товаров, фото‑креативы для брендов (за которые реально платят)
• научишься делать креативный AI‑видеоконтент для своего блога и для клиентов
• разберёшь структуру виральных роликов и продающего контента (не «залетело», а система)
• получишь навыки монтажа и упаковки, чтобы ролики выглядели дорого
• получишь закрытую базу премиум‑промптов, которые экономят часы тестов
• доступ к постоянно обновляемой базе знаний
• для работы нужен только телефон 

⚡️ Важно: цена будет расти — по мере роста клуба и уроков.  

Вариант 1: участие в клубе — { $club_price } ₽  
Вариант 2: клуб + личное наставничество — { $mentor_price } ₽

❗️Для работы нужна отдельная подписка на нейросети (примерно 1690 ₽/мес), она не входит в стоимость клуба.

🎁 Заходи сейчас, пока действует текущая цена ⬇️"""]: ...

class SuccessfulPaymentMentor:
    @staticmethod
    def left(*, link: PossibleValue, username: PossibleValue) -> Literal["""Поздравляю с выгодным вложением! Теперь ты имеешь доступ в клуб и личное менторство.
Присоединяйся { $link } и начинай проходить уроки!
Если будут возникать вопросы, или что то не будет получаться пиши { $username }"""]: ...
    @staticmethod
    def member(*, username: PossibleValue) -> Literal["""Поздравляю тебя с выгодной инвестицией в свои навыки! По всем вопросам пиши { $username }"""]: ...

class SuccessfulPaymentAdminMentor:
    @staticmethod
    def left(*, first_name: PossibleValue, username: PossibleValue) -> Literal["""{ $first_name } ( @{ $username } ) оплатил(а) Доступ + Наставничество"""]: ...
    @staticmethod
    def member(*, first_name: PossibleValue, username: PossibleValue) -> Literal["""{ $first_name } ( @{ $username } ) оплатил(а) Наставничество"""]: ...

class SuccessfulPaymentAdmin:
    mentor: SuccessfulPaymentAdminMentor

    @staticmethod
    def club(*, first_name: PossibleValue, username: PossibleValue) -> Literal["""{ $first_name } ( @{ $username } ) оплатил(а) Доступ в клуб"""]: ...

class SuccessfulPayment:
    mentor: SuccessfulPaymentMentor
    admin: SuccessfulPaymentAdmin

    @staticmethod
    def club(*, link: PossibleValue) -> Literal["""Поздравляю с выгодным вложением! Теперь ты имеешь доступ в клуб.
Присоединяйся { $link } и начинай проходить уроки!"""]: ...

class Successful:
    payment: SuccessfulPayment

class AdminButton:
    @staticmethod
    def back() -> Literal["""⬅️ Назад"""]: ...

class AdminMenuButton:
    @staticmethod
    def analytics() -> Literal["""📊 Аналитика"""]: ...
    @staticmethod
    def price() -> Literal["""💵 Задать цену"""]: ...
    @staticmethod
    def mailing() -> Literal["""✉️ Рассылка"""]: ...
    @staticmethod
    def user() -> Literal["""👤 Перейти в меню пользователя"""]: ...

class AdminMenuPriceButtonMentor:
    @staticmethod
    def left() -> Literal["""🤖👨‍🏫 Доступ + Наставничество"""]: ...
    @staticmethod
    def member() -> Literal["""👨‍🏫 Наставничество"""]: ...

class AdminMenuPriceButton:
    mentor: AdminMenuPriceButtonMentor

    @staticmethod
    def club() -> Literal["""🤖 Доступ в клуб"""]: ...

class AdminMenuPriceSet:
    @staticmethod
    def text() -> Literal["""Задайте цену для товара, обязательно укажите копейки после точки! Формат: Р.КК"""]: ...
    @staticmethod
    def finish(*, price: PossibleValue, product: PossibleValue) -> Literal["""Новая цена для { $product }: { $price }"""]: ...

class AdminMenuPrice:
    button: AdminMenuPriceButton
    set: AdminMenuPriceSet

    @staticmethod
    def text() -> Literal["""Выберите товар, для которого хотите задать цену"""]: ...

class AdminMenu:
    button: AdminMenuButton
    price: AdminMenuPrice

    @staticmethod
    def text(*, club_price: PossibleValue, mentor_price: PossibleValue, mentor_upgrade_price: PossibleValue) -> Literal["""Добро пожаловать в админ-панель бота!

Цена для Доступ в клуб: { $club_price } ₽
Цена для Доступ + Наставничество: { $mentor_price } ₽
Цена для Наставничество: { $mentor_upgrade_price } ₽"""]: ...

class Admin:
    button: AdminButton
    menu: AdminMenu
