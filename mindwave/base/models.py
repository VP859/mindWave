from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=40)

    def get_quizes(self):
        return self.quiz_set.all()
    
    def get_diagnostic(self):
        return self.diagnostictest_set.all()

    def __str__(self) -> str:
        return self.name

#QUIZ
class Quiz(models.Model):
    name    = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time    = models.FloatField(help_text='Duration of the quiz in minutes')
    created = models.DateTimeField(auto_now_add=True)

    def get_questions(self):
        return self.question_set.all()
    
    def get_scores(self):
        return self.score_set.all().order_by('-points')

    def __str__(self) -> str:
        return f'{self.name} - {self.subject.name}'
    
class Question(models.Model):
    quiz        = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text        = models.CharField(max_length=300)
    openTask    = models.BooleanField(default=False)

    def get_answers(self):
        return self.answer_set.all()

    def __str__(self) -> str:
        return f'Question - {self.quiz.name} - ({self.pk})'
    
class Answer(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    text        = models.CharField(max_length=200)
    correct     = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Answer - {self.question} - ({self.pk})'
    
class Score(models.Model):
    user    = models.ForeignKey('accounts.profile', on_delete=models.CASCADE)
    quiz    = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    points  = models.IntegerField()
    date    = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return super().__str__()


#DIAGNOSTIC TESTS
class DiagnosticTest(models.Model):
    name    = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time    = models.FloatField(help_text='Duration of the quiz in minutes')
    created = models.DateTimeField(auto_now_add=True)

    # def get_questions(self):
    #     return self.question_set.all()
    
    def get_diagnosticcategory(self):
        return self.diagnosticcategory_set.all()

    def __str__(self) -> str:
        return f'{self.name} - {self.subject.name}'
    
class DiagnosticCategory(models.Model):
    name = models.CharField(max_length=60)
    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)

    def get_questions(self):
        return self.diagnosticquestion_set.all()
    
    def __str__(self) -> str:
        return f'{self.name} - {self.test.name}'
    
class DiagnosticQuestion(models.Model):
    # quiz = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    text        = models.CharField(max_length=300)
    openTask    = models.BooleanField(default=False)
    category    = models.ForeignKey(DiagnosticCategory, on_delete=models.CASCADE)

    def get_answers(self):
        return self.diagnosticanswer_set.all()

    def __str__(self) -> str:
        return f'Question - {self.category.name} - ({self.pk})'
    
class DiagnosticAnswer(models.Model):
    question    = models.ForeignKey(DiagnosticQuestion, on_delete=models.CASCADE)
    text        = models.CharField(max_length=200)
    correct     = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Answer - {self.question} - ({self.pk})'

class DiagnosticScore(models.Model):
    user    = models.ForeignKey('accounts.profile', on_delete=models.CASCADE)
    test    = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    points  = models.IntegerField()
    date    = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return super().__str__()
    

class Category(models.Model):
    category_name = models.CharField(max_length=60)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name