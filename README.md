# AdaptingTests
Задача адаптивного тестирования знаний студентов на Django
Код программы, разработанный для моей Выпусной Квалификационной работы бакалавра. 
  В данной ВКРБ решается задача адаптивного тестирования знаний 
студентов на основе ФОС ИАС. 
  В ходе решения поставленной задачи разработано программное 
обеспечение клиент-серверной архитектуры, с помощью которого 
авторизованные пользователи-студенты <user_student> могут пройти 
тестирование адаптивным методом по курсам <subject>, составленным 
пользователями-преподавателями <user_teacher>, с получением итогового 
результата тестирования <mark>.
  Для функционирования программы создана система распределения 
ролей, с помощью которой администраторы <user_admin> сайта смогут 
наделять теми или иными правами <permission> определенные группы 
пользователей <user>. Группа «преподаватели» <user_teacher> должна иметь 
больше прав <permission>, чем группа «студенты» <user_student>, например, 
студентам необходимо ограничить возможность просмотра информации о 
сессиях пользователей <session>, редактирования курсов <subject> и т.д.

