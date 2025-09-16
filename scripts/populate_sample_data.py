# scripts/populate_sample_data.py
from users.models import User
from quiz.models import Subject, Question

# create users if not exist
surya, _ = User.objects.get_or_create(username='surya', defaults={
    'email':'suryasubramanian116@gmail.com', 'is_staff': True, 'is_superuser': True
})
if not surya.has_usable_password():
    surya.set_password('surya_pass')
    surya.save()

shiva, created = User.objects.get_or_create(username='shiva', defaults={
    'email':'shiva@example.com'
})
if created:
    shiva.set_password('shiva_pass')
    shiva.save()

subjects = [
    'Python Quiz', 'Java Quiz', 'AI/ML Quiz', 'Math Quiz', 'English Quiz'
]

for idx, title in enumerate(subjects, start=1):
    s, _ = Subject.objects.get_or_create(title=title, order=idx, defaults={'description': f'{title} description'})
    # create 10 mixed questions
    for i in range(1, 11):
        if i % 2 == 0:
            # fill in blank
            Question.objects.create(
                subject=s,
                text=f'What is {i} + {i}?',
                qtype='fib',
                difficulty=1,
                correct_answer=str(i + i)
            )
        else:
            # MCQ
            choices = ['Option A', 'Option B', 'Option C', 'Option D']
            Question.objects.create(
                subject=s,
                text=f'Choose the correct option for item {i}',
                qtype='mcq',
                difficulty=1,
                choices=choices,
                correct_answer='Option A'
            )

print("Sample data populated.")
