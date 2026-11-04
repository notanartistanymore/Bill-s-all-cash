# Bill's all cash

Небольшой REST API для работы с кошельками. Можно создать кошелёк, пополнить его, списать деньги и посмотреть баланс.

Написан на FastAPI, SQLAlchemy и PostgreSQL. Для миграций используется Alembic, для тестов pytest.

## Как запустить

Нужны Docker и Docker Compose. Из папки проекта скопируйте настройки:

```bash
cp .env.example .env
```

Пример `.env` для локального запуска:

```dotenv
DATABASE_NAME=database
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/database
TEST_DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/wallets_test
```

Затем запустите приложение и базу:

```bash
docker compose up --build
```

Миграции применятся автоматически. Документация с возможностью отправлять запросы доступна по адресу http://localhost:8000/docs.

Остановить контейнеры можно командой `docker compose down`. Данные базы при этом сохраняются.

## Что умеет API

- `POST /api/v1/wallets` - создать кошелёк. В теле запроса нужны `wallet_name` и необязательный `initial_balance` (по умолчанию `0`).
- `GET /api/v1/wallets/{wallet_uuid}` - получить кошелёк и его баланс.
- `POST /api/v1/wallets/{wallet_uuid}/operation` - пополнить кошелёк или списать средства.

Пример пополнения:

```json
{
  "operation_type": "DEPOSIT",
  "amount": 1000
}
```

Для списания используйте `WITHDRAW`. Все суммы указаны в копейках: `1000` это 10 рублей. В Python суммы имеют тип `int`, в базе баланс хранится как `BIGINT`.

При изменении баланса используется `SELECT FOR UPDATE`: параллельные операции над одним кошельком ждут друг друга до завершения транзакции. Проверка средств и изменение баланса выполняются вместе. Дополнительно в базе стоит запрет на отрицательный баланс.

Если кошелёк не найден, API вернёт `404`, если не хватает денег или имя уже занято, то`409`. Некорректный запрос вернёт `422`.

## Как запустить тесты

Тесты запускаются на компьютере в обычном виртуальном окружении, а PostgreSQL работает в Docker. Устанавливать pytest внутрь контейнера не нужно.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
docker compose up -d postgres
```

Дождитесь готовности базы (`docker compose ps`), затем выполните:

```bash
python -m pytest -v
```

В `.env` должен быть указан `TEST_DATABASE_URL` отдельной тестовой базы: тесты удаляют и создают в ней таблицы. При запуске с компьютера хост  `localhost`, внутри Docker — `postgres`.

База `wallets_test` создаётся автоматически при первой инициализации PostgreSQL. Если используется старый том и этой базы ещё нет, создайте её один раз:

```bash
docker compose exec postgres sh -c 'createdb -U "$POSTGRES_USER" wallets_test'
```

Есть проверки основных сценариев API, ошибок и параллельных пополнений и списаний одного кошелька.
