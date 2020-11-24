from django.db import models
from users.models import *
from django.db import connection
import datetime
from project_v_0_0_1.settings import dist_table





class Dashboard(models.Model):
    '''
    Сущность для определения виджетов

      Attributes
    ===========
    - name - str - название для записи

     Methods
    =============
    - None
    '''
    name = models.CharField(max_length=255, default='no name')

    def __str__(self):
        return self.name




class Role(models.Model):
    '''
        Сущность для определения роли пользователя

          Attributes
        ===========
        - name - str - название для записи
        - user - MtM - связь с сущностью UserP
        - dashboard - MtM - связь с сущностью Dashboard

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')
    user = models.ManyToManyField(UserP)
    dashboard = models.ManyToManyField(Dashboard)




# для виджета продолжительность работы
class DurationIntervalDay(models.Model):
    '''
        Сущность для определения начало и времени работы

          Attributes
        ===========
        - start - Time - начало работы
        - end - Time - конец работы
        - date - Date - дата работы

         Methods
        =============
        - None
    '''
    start = models.TimeField('start work')
    end = models.TimeField('end work')
    date = models.DateField(auto_now=False, auto_now_add=False)




class Storehouse(models.Model):
    '''
    Сущность для названия склада

          Attributes
        ===========
        - name - str - название склада

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')


    def __str__(self):
        return self.name


class Substance(models.Model):
    '''
    Сущность для названия хранящегося вещества

          Attributes
        ===========
        - name - str - название вещества
        - short_name - str - короткая название вещества
        - parent - FK - внешний ключь с Storehouse

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')
    short_name = models.CharField(max_length=255, default='no name')
    table_name = models.CharField(max_length=255, default='no name')
    parent = models.ForeignKey(Storehouse, on_delete=models.CASCADE)

    def __str__(self):
        data = self.name + '(' + self.parent.name + ')'
        return data

    def calculate(self, date):
        '''Забись данных в таблицу Django остатка по дате'''
        if date.date() != datetime.datetime.now().date():
            with connection.cursor() as cursor:
                sql1 = '''SELECT value, now_time FROM '''
                sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
                sql = sql1 + self.table_name + sql2
                date_now = date + datetime.timedelta(days=1)
                cursor.execute(sql, [date, date_now])
                a = cursor.fetchone()
                k = DateValue(date=a[1], value=a[0], parent=self)
                k.save()
        else:
            with connection.cursor() as cursor:
                sql1 = '''SELECT value, now_time FROM '''
                sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
                sql = sql1 + self.table_name + sql2
                date_new = date + datetime.timedelta(days=1)
                cursor.execute(sql, [date, date_new])
                a = cursor.fetchone()
        return a


    def value_date(self, date):
        if date.date() == datetime.datetime.now().date():
            try:
                k = self.calculate(date)[0]
            except TypeError:
                k = 0
        else:
            if self.datevalue_set.filter(date=date).exists():
                k = self.datevalue_set.get(date=date).value
            else:
                self.calculate(date)
                k = self.datevalue_set.get(date=date).value
        return k



class DateValue(models.Model):
    '''
    Сущность для количество вещества по времени

          Attributes
        ===========
        - date - date - дата
        - value - float - количество вещества
        - parent - FK - внешний ключь с Substance

         Methods
        =============
        - None
    '''
    date = models.DateField(auto_now=False, auto_now_add=False)
    value = models.FloatField()
    parent = models.ForeignKey(Substance, on_delete=models.CASCADE)

    def __str__(self):
        data = str(self.date) + ':  ' + self.parent.name + '-' + str(self.value)
        return data


def calculate_edition(date):
    '''Забись данных в таблицу Django остатка по дате'''
    with connection.cursor() as cursor:
        sql1 = '''SELECT value, now_time FROM '''
        sql2 = ''' WHERE now_time>=%s and now_time<%s and status=0 ORDER BY now_time DESC LIMIT 1'''
        sql = sql1 + dist_table['EditionDay'] + sql2
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        brak = cursor.fetchone()

        sql1 = '''SELECT value, now_time FROM '''
        sql2 = ''' WHERE now_time>=%s and now_time<%s and status=2 ORDER BY now_time DESC LIMIT 1'''
        sql = sql1 + dist_table['EditionDay'] + sql2
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        ne_kond = cursor.fetchone()


        sql1 = '''SELECT value, now_time FROM '''
        sql2 = ''' WHERE now_time>=%s and now_time<%s and status=1 ORDER BY now_time DESC LIMIT 1'''
        sql = sql1 + dist_table['EditionDay'] + sql2
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        godno = cursor.fetchone()

        sql1 = '''SELECT value, now_time, status FROM '''
        sql2 = ''' WHERE now_time>=%s and now_time<%s and status=3 ORDER BY now_time DESC LIMIT 1'''
        sql = sql1 + dist_table['EditionDay'] + sql2
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        zalito = cursor.fetchone()

        if brak == None:
            brak = [0]
        if ne_kond == None:
            ne_kond = [0]
        if godno == None:
            godno = [0]
        if zalito == None:
            zalito = [0]
        print("asdasd:",brak[0])
        k = EditionDay(date=date, suitable=godno[0], substandard=ne_kond[0], defect=brak[0], flooded=zalito[0], sum=brak[0]+ne_kond[0]+godno[0])
        k.save()

    return k


# для виджета Выпуск панелей
class EditionDay(models.Model):
    '''
        Сущность для определения выпуска

          Attributes
        ===========
        - suitable - float - количество годного
        - substandard - float - количество некондиции
        - defect - float - количество брака
        - flooded - float - количество залитого
        - sum - float - сумма годного, некондиции, брака
        - date - Date - дата

         Methods
        =============
        - None

    '''
    suitable = models.FloatField()
    substandard = models.FloatField()
    defect = models.FloatField()
    flooded = models.FloatField()
    sum = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)







# для виджета Суммарный расход
class SumexpenseDay(models.Model):
    '''
        Сущность для определения сумарного расхода

          Attributes
        ===========
        - iso - float - количество расхода изоцианата
        - pol - float - количество расхода полиола
        - pen - float - количество расхода пентана
        - kat1 - float - количество расхода катализатора 1
        - kat2 - float - количество расхода катализатора 2
        - kat3 - float - количество расхода катализатора 3
        - date - Date - дата

         Methods
        =============
        - None
    '''
    iso = models.FloatField()
    pol = models.FloatField()
    pen = models.FloatField()
    kat1 = models.FloatField()
    kat2 = models.FloatField()
    kat3 = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)


# для виджета Расход энергоресурсов
class EnergyConsumptionDay(models.Model):
    '''
        Сущность для определения сумарного расхода энергоресурсов

          Attributes
        ===========
        - input1 - float - расход эл.энергии ввода 1
        - input2 - float - расход эл.энергии ввода 2
        - gas - float - расход газа
        - date - Date - дата

         Methods
        =============
        - None

    '''
    input1 = models.FloatField()
    input2 = models.FloatField()
    gas = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)


# для виджета Удельный расход на км
class SpecificConsumptionDay(models.Model):
    '''
        Сущность для определения удельного расхода

          Attributes
        ===========
        - iso - float - количество удельного расхода изоцианата
        - pol - float - количество удельного расхода полиола
        - pen - float - количество удельного расхода пентана
        - kat1 - float - количество удельного расхода катализатора 1
        - kat2 - float - количество удельного расхода катализатора 2
        - kat3 - float - количество удельного расхода катализатора 3
        - date - Date - дата

         Methods
        =============
        - None
    '''
    iso = models.FloatField()
    pol = models.FloatField()
    pen = models.FloatField()
    kat1 = models.FloatField()
    kat2 = models.FloatField()
    kat3 = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
