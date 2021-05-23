from django.db import models

class Query(models.Model):
    # name = models.CharField('お名前', max_length=50)
    email = models.EmailField('メールアドレス')
    subject = models.CharField('件名', max_length=250)
    contents = models.TextField('お問い合わせ内容')
    date = models.DateTimeField('日時', auto_now_add=True)

    def __str__(self):
        return f'{self.subject}'
