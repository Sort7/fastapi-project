Приложение для записи на услуги
Используемые инструменты:
    • фейерверк: Fastapi (+ типизация данных: Pydentic),
    • БД: PostgreSQL,
    • OPM: SQLAlchemy + Asyncio,
    • миграции: Alembic,
    • кеширование: Redis (модуль: fastapi-cache2),
    • фоновые задачи: Selery,
    • хеширование паролей: Bcrypt;
    • выпуск jwt токенов: PyJWT,
    • менеджер зависимостей: Poetry;
    • развертывание: Docker (dockerfile, docker-compose)
    • система управления версиями Git
Реализованный функционал:
    • Регистрация пользователей с распределением системы ролей (пользователь, тренер, администратор). Пользователь может: просматривать карточки (с информацией о тренерах) выбирать тренера и записываться к нему на дату и время (+ отменять запись). Тренер может: создать и редактировать свою карточку, видеть список записанных клиентов (даты и время). Администратор может: добавлять, редактировать карточки пользователей, удалять пользователей и их карточки; менять статусы пользователей; записывать пользователей на занятия к тренерам и отменять записи.
    • Вход по JSW токену (выпуск «access-токена» и его перевыпуск по «refresh-токену»)
    • Отправка сообщения о регистрации на email — пользователя.
    • Кеширование запросов к базе данных с помощью Redis
