"""
utils
"""
cat_1 = 25
cat_2 = 10
main_exam = 24

total = ((cat_1 + cat_2) / 2) + main_exam
if total >= 70:
    grade = 'A'
elif total >= 60:
    grade = 'B'
elif total >= 50:
    grade = 'C'
elif total >= 40:
    grade = 'D'
else:
    grade = 'F'

print(total, grade)
