Test django project 


Пример данных:
    • gender [male/female]
    • age [18...99]
    • abdominal_pain [yes/no]
    • systolic_bp [60...300]
    • diastolic_bp [30...250]
    
    
Пример выполнения правил:
    • If abdominal_pain = yes then ask_question (id=1)
    • If gender = female and age > 45 then ask_question (id=2)
    • If systolic_bp > 140 or diastolic_bp < 90 then ask_question (id=3)


Пример результата:
[{“ask_question”: 1},{“ask_question”: 2}]


###################

Вся логика выполнена в answers -> serializer 