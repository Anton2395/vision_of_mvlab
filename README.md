# Система мониторинга работы предприятия (СиМоРаП)
## Оглавление
### [Описание](#description)
### [Обязательноые команды](#comands)
### [Авторизация пользователя](#autUser)
### [Структура предприятия](#structFactory)
### [Dashboard](#Dashboard)

## <a name="description"> *Описание* </a>
###  Для чего
Данное ПО предназначено для предасталвение данных и API для визуальной части 
ПО фирмы МВЛАБ (Минск Беларусь).

### Краткое описание
Проект состоит из следующих частей:  
- модуль пользователей  
В данном модуле происходит настройка данных о пользователе

- модуль структуры предприятия  
В этом приложении конфигурируется структура предприятия, смены, обеды, данные и и х физические велечины

- модуль рекордер  
Данный модуль предоставляет API для просмотра записываемых данных

- модуль ОЕЕ  
Здесь предоставляется API просмотра состоянии оборудования по временной шкале

- модуль ППР  
В этом модуле ведется электронный журнал учета причин простоя оборудования а так же планово-предупредительные ремонты

- модуль настроек  
В данном модуле происходит конфигурация приложения

## <a name="comands"> *Обязательный команды* </a>

- [ ] создание окружения
- [ ] установка зависимостей
- [ ] провести миграции
- [ ] произвести создание начальной структуры
#### Подробнее [ЗДЕСЬ](project_v_0_0_1/comands/README.md)

## <a name="autUser"> *Авторизация пользователя* </a>
В данном разделе будет опиасние авторизации пользователя. 
Смотреть [ЗДЕСЬ](README/user_README.md)

## <a name="structFactory"> *Структрура предприятия* </a>
 В данном разделе будет опиасние модуля структуры предприятия  
 Описание API структуры предприятия [ЗДЕСЬ](structure/README.md)
 
 ## <a name="Dashboard"> *Dashboard * </a>
 Подробная документация по API для модуля Dashboard находится [здесь](README/dashboard_README.md)