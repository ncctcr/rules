from django.db import models


class Answers(models.Model):
    rule = models.CharField(max_length=528,
                            blank=False,
                            null=False)
    positive_answer = models.CharField(max_length=128,
                                       blank=False,
                                       null=False)



    class Meta:
        db_table = "answer"
        verbose_name_plural = "answer's"

    def __str__(self):
        return "%s %s" % (self.positive_answer, self.rule)
