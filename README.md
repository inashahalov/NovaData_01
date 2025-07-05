# Data Pipeline: PostgreSQL → Kafka → ClickHouse

## Описание

Этот пайплайн переносит события из PostgreSQL в ClickHouse через Apache Kafka, обеспечивая защиту от дублирования данных.

### Компоненты:
- **PostgreSQL**: источник событий.
- **Kafka**: очередь сообщений.
- **ClickHouse**: целевое хранилище.
- **Producer**: читает из PostgreSQL, отправляет в Kafka.
- **Consumer**: получает из Kafka, пишет в ClickHouse.

---

## Как запустить

1. Убедитесь, что установлен Docker и Docker Compose.

2. Запустите инфраструктуру:
   ```bash
   docker-compose up -d