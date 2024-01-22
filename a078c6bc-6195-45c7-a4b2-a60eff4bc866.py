#!/usr/bin/env python
# coding: utf-8

# # Исследование надежности заемщиков
# 

# Во второй части проекта вы выполните шаги 3 и 4. Их вручную проверит ревьюер.
# Чтобы вам не пришлось писать код заново для шагов 1 и 2, мы добавили авторские решения в ячейки с кодом. 
# 
# 

# ## Откройте таблицу и изучите общую информацию о данных

# **Задание 1. Импортируйте библиотеку pandas. Считайте данные из csv-файла в датафрейм и сохраните в переменную `data`. Путь к файлу:**
# 
# `/datasets/data.csv`

# In[1]:


import pandas as pd

try:
    data = pd.read_csv('/datasets/data.csv')
except:
    data = pd.read_csv('https://code.s3.yandex.net/datasets/data.csv')


# **Задание 2. Выведите первые 20 строчек датафрейма `data` на экран.**

# In[2]:


data.head(20)


# **Задание 3. Выведите основную информацию о датафрейме с помощью метода `info()`.**

# In[3]:


data.info()


# ## Предобработка данных

# ### Удаление пропусков

# **Задание 4. Выведите количество пропущенных значений для каждого столбца. Используйте комбинацию двух методов.**

# In[4]:


data.isna().sum()


# **Задание 5. В двух столбцах есть пропущенные значения. Один из них — `days_employed`. Пропуски в этом столбце вы обработаете на следующем этапе. Другой столбец с пропущенными значениями — `total_income` — хранит данные о доходах. На сумму дохода сильнее всего влияет тип занятости, поэтому заполнить пропуски в этом столбце нужно медианным значением по каждому типу из столбца `income_type`. Например, у человека с типом занятости `сотрудник` пропуск в столбце `total_income` должен быть заполнен медианным доходом среди всех записей с тем же типом.**

# In[5]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['total_income'].isna()), 'total_income'] =     data.loc[(data['income_type'] == t), 'total_income'].median()


# ### Обработка аномальных значений

# **Задание 6. В данных могут встречаться артефакты (аномалии) — значения, которые не отражают действительность и появились по какой-то ошибке. таким артефактом будет отрицательное количество дней трудового стажа в столбце `days_employed`. Для реальных данных это нормально. Обработайте значения в этом столбце: замените все отрицательные значения положительными с помощью метода `abs()`.**

# In[6]:


data['days_employed'] = data['days_employed'].abs()


# **Задание 7. Для каждого типа занятости выведите медианное значение трудового стажа `days_employed` в днях.**

# In[7]:


data.groupby('income_type')['days_employed'].agg('median')


# У двух типов (безработные и пенсионеры) получатся аномально большие значения. Исправить такие значения сложно, поэтому оставьте их как есть.

# **Задание 8. Выведите перечень уникальных значений столбца `children`.**

# In[8]:


data['children'].unique()


# **Задание 9. В столбце `children` есть два аномальных значения. Удалите строки, в которых встречаются такие аномальные значения из датафрейма `data`.**

# In[9]:


data = data[(data['children'] != -1) & (data['children'] != 20)]


# **Задание 10. Ещё раз выведите перечень уникальных значений столбца `children`, чтобы убедиться, что артефакты удалены.**

# In[10]:


data['children'].unique()


# ### Удаление пропусков (продолжение)

# **Задание 11. Заполните пропуски в столбце `days_employed` медианными значениями по каждого типа занятости `income_type`.**

# In[11]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['days_employed'].isna()), 'days_employed'] =     data.loc[(data['income_type'] == t), 'days_employed'].median()


# **Задание 12. Убедитесь, что все пропуски заполнены. Проверьте себя и ещё раз выведите количество пропущенных значений для каждого столбца с помощью двух методов.**

# In[12]:


data.isna().sum()


# ### Изменение типов данных

# **Задание 13. Замените вещественный тип данных в столбце `total_income` на целочисленный с помощью метода `astype()`.**

# In[13]:


data['total_income'] = data['total_income'].astype(int)


# ### Обработка дубликатов

# **Задание 14. Обработайте неявные дубликаты в столбце `education`. В этом столбце есть одни и те же значения, но записанные по-разному: с использованием заглавных и строчных букв. Приведите их к нижнему регистру.**

# In[14]:


data['education'] = data['education'].str.lower()


# **Задание 15. Выведите на экран количество строк-дубликатов в данных. Если такие строки присутствуют, удалите их.**

# In[15]:


data.duplicated().sum()


# In[16]:


data = data.drop_duplicates()


# ### Категоризация данных

# **Задание 16. На основании диапазонов, указанных ниже, создайте в датафрейме `data` столбец `total_income_category` с категориями:**
# 
# - 0–30000 — `'E'`;
# - 30001–50000 — `'D'`;
# - 50001–200000 — `'C'`;
# - 200001–1000000 — `'B'`;
# - 1000001 и выше — `'A'`.
# 
# 
# **Например, кредитополучателю с доходом 25000 нужно назначить категорию `'E'`, а клиенту, получающему 235000, — `'B'`. Используйте собственную функцию с именем `categorize_income()` и метод `apply()`.**

# In[17]:


def categorize_income(income):
    try:
        if 0 <= income <= 30000:
            return 'E'
        elif 30001 <= income <= 50000:
            return 'D'
        elif 50001 <= income <= 200000:
            return 'C'
        elif 200001 <= income <= 1000000:
            return 'B'
        elif income >= 1000001:
            return 'A'
    except:
        pass


# In[18]:


data['total_income_category'] = data['total_income'].apply(categorize_income)


# **Задание 17. Выведите на экран перечень уникальных целей взятия кредита из столбца `purpose`.**

# In[19]:


data['purpose'].unique()


# **Задание 18. Создайте функцию, которая на основании данных из столбца `purpose` сформирует новый столбец `purpose_category`, в который войдут следующие категории:**
# 
# - `'операции с автомобилем'`,
# - `'операции с недвижимостью'`,
# - `'проведение свадьбы'`,
# - `'получение образования'`.
# 
# **Например, если в столбце `purpose` находится подстрока `'на покупку автомобиля'`, то в столбце `purpose_category` должна появиться строка `'операции с автомобилем'`.**
# 
# **Используйте собственную функцию с именем `categorize_purpose()` и метод `apply()`. Изучите данные в столбце `purpose` и определите, какие подстроки помогут вам правильно определить категорию.**

# In[20]:


def categorize_purpose(row):
    try:
        if 'автом' in row:
            return 'операции с автомобилем'
        elif 'жил' in row or 'недвиж' in row:
            return 'операции с недвижимостью'
        elif 'свад' in row:
            return 'проведение свадьбы'
        elif 'образов' in row:
            return 'получение образования'
    except:
        return 'нет категории'


# In[21]:


data['purpose_category'] = data['purpose'].apply(categorize_purpose)


# ### Шаг 3. Исследуйте данные и ответьте на вопросы

# #### 3.1 Есть ли зависимость между количеством детей и возвратом кредита в срок?

# In[22]:


data['debt'].value_counts() # с помощью # value_counts посчитаем людей  в столбе debt имеющих и не имеющих задолжность


# In[23]:


# 19599 из данного дата сета не имеет задолжнотей по кредиту, 1732 человека имеют задолжность
data['children'].value_counts() # с помощью # value_counts посчитаем людей с детьми , 14091 не имеет детей, остальные 7240 имеют одного и более детей


# In[24]:


# Создаём функцию для определения наличия детей:
def children_factor(children):
    if children == 0:
        return 'Детей нет'
    if children > 0:
        return 'Дети есть'


# In[58]:


# К имеющейся таблице добавляем столбец children_factor
data['children_factor']=data['children'].apply(children_factor)
#Создаём сводную таблицу с помощью метода pivot_table()
data_pivot_children_debt = data.pivot_table(index=['children_factor'], values=['children','debt'])
data_pivot_children_debt.columns = ['no_debt', 'debt']
data_pivot_children_debt['fraction_of_debtors'] = data_pivot_children_debt['debt'] / (data_pivot_children_debt['debt']+data_pivot_children_debt['no_debt']) #Создаём столбец fraction_of_debtors(доля должников) и добавялем его к имеющейся таблице
display(data_pivot_children_debt)


# **Вывод:** Можем сделать вывод, что наличие детей влияет на возвращение кредита в срок. Клиенты с детьми чаще имеют задолжность по кредиту,по сравнению с клиентами без детей.

# #### 3.2 Есть ли зависимость между семейным положением и возвратом кредита в срок?

# In[57]:


# Создаём сводною таблицу с помощью метода pivot_table:
data_pivot_familystatus_debt = data.pivot_table (index=['family_status'], columns=['debt'], values='gender', aggfunc='count')
data_pivot_familystatus_debt.columns = ['no_debt', 'debt']
data_pivot_familystatus_debt['fraction_of_debtors'] =(data_pivot_familystatus_debt['debt'] / data_pivot_familystatus_debt['debt'] +data_pivot_familystatus_debt['no_debt'])  #считаем долю должников , называем столбец data_pivot_familystatus_debt[fraction_of_debtors]и интегрируем его в таблицу
display(data_pivot_familystatus_debt)


# **Вывод:** Женатые/замужние клиенты чаще всего имеют задолжность по кредиту. Но стоит отметить, что это может быть связано с тем что данной категория самая часто встречающаяся, поэтому и неимеющих задолжностей также лидирует данная группа.

# #### 3.3 Есть ли зависимость между уровнем дохода и возвратом кредита в срок?

# In[64]:


# Создаём сводную таблицу с помощью метода pivot_table #примечание:в роли столбца по которому происходит группировка данных является раннее созданный нами столбец total_income_category(задание 16)
data_pivot_totalincome_debt = data.pivot_table (index=['total_income_category'], columns=['debt'], values='gender',aggfunc='count')
data_pivot_totalincome_debt.columns = ['no_debt', 'debt']
data_pivot_totalincome_debt['fraction_of_debtors'] = data_pivot_totalincome_debt['debt']/ (data_pivot_totalincome_debt['debt']+data_pivot_totalincome_debt['no_debt'])
data_pivot_totalincome_debt['fraction_of_debtors'] = data_pivot_totalincome_debt['fraction_of_debtors'].map('{:.1%}'.format) # переведём столбец "доля должников"в % для наглядности
display(data_pivot_totalincome_debt)


# **Вывод:** Опираясь на процентное соотношение доли должников: Лица получающие больше всех, чаще всех имеют задолжность, но т.к количество людей не сопоставимо с количеством людей в других выборках(малое количество) в зачёт мы эту выборку не берём
# Сравним самые многочисленные выборки: это категории B и C : Те кто находится  в категории "C" чаще становятся должниками ( не смотря на то что денежных средств получают больше)
# Ну и я думаю стоит отметить что категория "D" имеет самый низкий риск иметь задолжность по кредиту. ( в зачёт также не берём из-за небольшого количества)
# 

# #### 3.4 Как разные цели кредита влияют на его возврат в срок?

# In[66]:


# Создаём сводную таблицу с помощью метода pivot_table
data_purpose_debt = data.pivot_table (index='purpose_category', columns='debt', values='gender', aggfunc='count')
data_purpose_debt.columns = ['no_debt', 'debt']
data_purpose_debt['fraction_of_debtors']=data_purpose_debt['debt']/(data_purpose_debt['debt']+data_purpose_debt['no_debt'])
data_purpose_debt['fraction_of_debtors']=data_purpose_debt['fraction_of_debtors'].map('{:.1%}'.format) #Долю должников переводим в %
display(data_purpose_debt)


# Чаще всего и одинаково часто, задолжность образовывается по кредитам взятых на операции с авто, получением образования.
# Цель кредита : првоедение свадьбы занимает 3е место нашего антирейтинга
# займы на операции с недвижимостью имеют самый низкий риск задолжностей
# При всём этом операции с недвижимостью самые часто встречающиеся, поэтому при выводе на экран без столбца "доля должников" формируется мнение что "недвижимость" самый высокорискованный кредит ( в плане задолжностей)

# #### 3.5 Приведите возможные причины появления пропусков в исходных данных.

# *Ответ:* человеческий фактор(невнимательность,пропуск,опечатка),повреждение файла, возможно кто-то решил скрыть эту информацию.

# #### 3.6 Объясните, почему заполнить пропуски медианным значением — лучшее решение для количественных переменных.

#  *Ответ:* Медиана предпочтительнее т.к. в статистике она более устойчива к факторам и опечаткам допустим, поясню на примере: если мы считаем среднюю зарплату, то премия к концу года может сильно повлиять на среднее арифметическое, а медиана меньше подвержена такому риску. Итог: медиана более объективна в статистике.

# ### Шаг 4: общий вывод.

# Итак, мы взяли датафрейм, удалили пропуски, обработали аномальные значения,обработали дубликаты, изменили типы данных для возможности подсчёта некоторых значений,категоризировали данные с помощью функций
# Далее мы вывели полученные данные в сводные таблицы и сделали следующие выводы:
# 1ое: Наличие детей влияет на возвращение кредита в срок. Клиенты с детьми чаще имеют задолжность по кредиту,по сравнению с клиентами без детей.
# 2ое: Женатые/замужние клиенты чаще всего имеют задолжность по кредиту.
# 3е:Лица получающие больше всех, чаще всех имеют задолжность, но т.к количество людей не сопоставимо с количеством людей в других выборках(малое количество) в зачёт мы эту выборку не берём
# Сравним самые многочисленные выборки: это категории B и C : Те кто находится  в категории "C" чаще становятся должниками ( не смотря на то что денежных средств получают больше)
# 4е: Чаще всего и одинаково часто, задолжность образовывается по кредитам взятых на операции с авто, получением образования.
# Цель кредита : првоедение свадьбы занимает 3е место нашего антирейтинга
# займы на операции с недвижимостью имеют самый низкий риск задолжностей
# При всём этом операции с недвижимостью самые часто встречающиеся, поэтому при выводе на экран без столбца "доля должников" формируется мнение что "недвижимость" самый высокорискованный кредит ( в плане задолжностей)
# 
