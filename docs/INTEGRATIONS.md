# Интеграции приложений

Интеграция приложения является anti-corruption layer вокруг стабильных контрактов TRC. Она работает в двух направлениях:

```text
Consumer request/profile → подсказки RecognitionRequest
RecognitionResult        → принадлежащая consumer проекция
```

Ни одно направление не изменяет домен Core и не импортирует в него бизнес-сервисы consumer. Каждое производное поле хранит provenance до IDs исходных Region/Line/Token и revision.

## Общий контракт adapter

```text
ApplicationProfile
  name/version
  required/optional capabilities
  allowed privacy modes
  default language/mode hints

ApplicationProjector[T]
  project(result, revision_id) -> ProjectionResult[T]
  validate_provenance(projection) -> ValidationReport
```

Предупреждения проекции различают отсутствующий источник, низкий confidence и неоднозначное сопоставление. Projector детерминирован для одинаковых result, revision и версии adapter.

## Personal Chronicle

Вход: `MIXED/HTR`, подсказки Ukrainian/Russian/English, разрешённый или ожидаемый `LOCAL_ONLY`, обязательные layout и неопределённые фрагменты.

Выходная концепция, принадлежащая consumer: ID документа, вероятные даты, кандидаты записей, неопределённые фрагменты и ссылки на источники. TRC не создаёт события timeline, embeddings, RAG, summaries или ответы о дневнике.

Приёмка: raw layout страницы можно восстановить; каждая запись и неопределённый фрагмент ссылаются на source IDs; при `LOCAL_ONLY` не выбирается сетевой adapter.

## Receipt Scanner

Вход: OCR и layout, страна `UA`, подсказка валюты `UAH`, необязательная receipt capability до появления её поддержки.

Выходная концепция: merchant, timestamp, items, subtotal, discount, total и currency с confidence и source references для каждого заполненного поля. Parsing/extraction относятся к пакету интеграции; категории расходов и аналитика принадлежат Receipt Scanner.

Приёмка: поля total/items ссылаются на tokens/regions; неоднозначные суммы выдаются как предупреждения, а не выдуманные значения; арифметическая проверка не может перезаписать raw text.

## Tutor

Вход: MIXED, layout, handwriting; будущие capabilities `MATH`, `TABLE`, `DIAGRAM`, `ANSWER_REGION`, `TEACHER_COMMENT`.

Выходная концепция: кандидаты regions печатного задания, рукописного ответа и комментария преподавателя с provenance. Student, lesson, grading и генерация решения остаются в Tutor.

Приёмка: отсутствие обязательной math capability сообщается явно; необязательная будущая capability деградирует с предупреждением; печатные и рукописные regions могут направляться разным engines.

## Подключение нового consumer

1. Определить принадлежащую consumer SPEC проекции.
2. Выбрать существующие capabilities и privacy modes; новая capability Core требует отдельной проверки.
3. Реализовать input profile и projector вне домена Core.
4. Добавить contract/fixture tests на синтетических или разрешённых данных.
5. Доказать отсутствие прямой зависимости consumer от OCR SDK.

Успех означает, что consumer подключается через существующий API TRC без копирования pipeline или логики corrections.
