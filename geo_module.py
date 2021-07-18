import bs4
import pandas as pd
import requests

from random import randint, sample


class GeoModule:
    @staticmethod
    def _delete_brackets(data):
        return data.split('(')[0]

    @staticmethod
    def _convert_to_number(data):
        split_str = data.split()
        result = ''
        for elem in split_str:
            elem = elem.replace(',', '.')
            result = result + elem
        return float(result)

    __country_list = []
    __country_set = set()
    __capital = {}
    __world_part = {}
    __capital_list = []
    __capital_url_list = []

    def __init_capitals(self):
        response = requests.get(
            url='https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%BE%D0%BB%D0%B8%D1'
                '%86_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2')
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        parts = soup('span', 'mw-headline')[:5]
        capitals_table = soup('table', 'wikitable sortable')

        for i in range(len(parts)):
            current_part = parts[i].text
            current_data = capitals_table[i]('td')

            for j in range(0, len(current_data), 3):
                index = current_data[j]
                country_info = current_data[j + 1]('a')[1]
                capital_info = current_data[j + 2].a
                if index.text[-2] == '—':
                    continue

                current_country = country_info['title']
                self.__country_list.append(current_country)
                self.__country_set.add(current_country)
                self.__world_part[current_country] = current_part

                if capital_info is None:
                    self.__capital_url_list.append(None)
                    self.__capital_list.append('Отсутствует')
                else:
                    self.__capital_url_list.append(capital_info['href'])
                    self.__capital_list.append(
                        self._delete_brackets(
                            capital_info['title']))
                self.__capital[current_country] = self.__capital_list[-1]

    __area = {}

    def __init_area(self):
        response = requests.get(
            url='https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE'
                '%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2_%D0%B8_%D0%B7%D0%B0%D0%B2%D0%B8'
                '%D1%81%D0%B8%D0%BC%D1%8B%D1%85_%D1%82%D0%B5%D1%80%D1%80%D0%B8%D1%82%D0%BE%D1%80'
                '%D0%B8%D0%B9_%D0%BF%D0%BE_%D0%BF%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%B8')
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        area_data = soup('table', 'standard sortable')[0]('td')

        for i in range(0, len(area_data), 8):
            current_data = area_data[i + 1]('a')[1]
            if current_data.text == 'Китай':
                current_country = current_data.text
            else:
                current_country = current_data['title']
            current_area = self._convert_to_number(area_data[i + 2].text)
            self.__area[current_country] = current_area
        self.__area['Ватикан'] = 0.44

    __population = {}

    def __init_population(self):
        response = requests.get(
            url='https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE'
                '%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2_%D0%B8_%D0%B7%D0%B0%D0%B2%D0%B8'
                '%D1%81%D0%B8%D0%BC%D1%8B%D1%85_%D1%82%D0%B5%D1%80%D1%80%D0%B8%D1%82%D0%BE%D1%80'
                '%D0%B8%D0%B9_%D0%BF%D0%BE_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E')
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        population_data = soup('table', 'standard sortable')[0]('td')

        for i in range(0, len(population_data), 6):
            current_data = population_data[i + 1]('a')[1]
            current_country = current_data['title']
            if current_country not in self.__country_set:
                continue
            current_population = int(
                self._convert_to_number(population_data[i + 2].text))
            self.__population[current_country] = current_population

    __data_frame = pd.DataFrame()

    def __init_data_frame(self):
        world_part_list = []
        area_list = []
        population_list = []

        for current_country in self.__country_list:
            world_part_list.append(self.__world_part[current_country])
            area_list.append(self.__area[current_country])
            population_list.append(self.__population[current_country])

        self.__data_frame = pd.DataFrame(
            {
                'Страна': self.__country_list,
                'Часть света': world_part_list,
                'Столица': self.__capital_list,
                'Площадь': area_list,
                'Население': population_list
            }
        )

    def __init__(self):
        self.__init_capitals()
        self.__init_area()
        self.__init_population()
        self.__init_data_frame()

    __COUNT_ANSWERS = 5
    __answer_list = [str(i + 1) for i in range(__COUNT_ANSWERS)]

    __count_right = 0
    __count_all = 0

    def easy_capital_test(self):
        self.__count_right = 0
        self.__count_all = 0
        while True:
            self.__count_all += 1

            index_list = sample(
                range(0, len(self.__country_list) - 1), self.__COUNT_ANSWERS)
            current_answer = randint(0, len(index_list) - 1)
            current_country = self.__country_list[index_list[current_answer]]
            print(self.__capital[current_country])

            for i in range(self.__COUNT_ANSWERS):
                print(i + 1, '. ', self.__country_list[index_list[i]], sep='')

            while True:
                answer = input()
                if answer.lower() == 'стоп':
                    self.__print_result()
                    return
                if answer not in self.__answer_list:
                    print('Неправильный формат ответа, попробуй ещё раз')
                    continue
                if current_answer + 1 == int(answer):
                    self.__count_right += 1
                    print('Молодец!!! Это правилтный ответ :)')
                else:
                    print('К сожалению, это неправильный ответ :(')
                    print('Правильный ответ: ', current_answer +
                          1, '. ', current_country, sep='')
                print('Количество правильных ответов: ',
                      self.__count_right, '/', self.__count_all, '\n', sep='')
                break

    def __print_result(self):
        self.__count_all -= 1
        print('Твой финалный счёт: ', self.__count_right,
              '/', self.__count_all, '\n', sep='')

    def __check_answer(self, answer, right_answer):
        if answer not in self.__country_set:
            print('Я не знаю такой страны, попробуй ещё раз')
            return 0
        if answer == right_answer:
            self.__count_right += 1
            print('Молодец!!! Это правилтный ответ :)')
        else:
            print('К сожалению, это неправильный ответ :(')
            print('Правильный ответ: ', right_answer, sep='')
        print('Количество правильных ответов: ', self.__count_right,
              '/', self.__count_all, '\n', sep='')
        return 1

    def hard_capital_test(self):
        self.__count_all = 0
        self.__count_right = 0

        while True:
            self.__count_all += 1

            current_country = self.__country_list[randint(
                0, len(self.__country_list) - 1)]
            print(self.__capital[current_country])

            while True:
                answer = input()
                if answer.lower() == 'стоп':
                    self.__print_result()
                    return
                if self.__check_answer(answer, current_country) == 0:
                    continue
                break

    def country_test(self, world_part=True, capital=True,
                     area=True, population=True):
        if (world_part or capital or area or population) is False:
            print('Хочешь проверить свою интуицию? Давай попробуем')

        self.__count_all = 0
        self.__count_right = 0

        while True:
            self.__count_all += 1

            current_country = self.__country_list[randint(
                0, len(self.__country_list) - 1)]

            if world_part:
                print('Часть света:', self.__world_part[current_country])
            if capital:
                print('Столица:', self.__capital[current_country])
            if area:
                print('Площадь:', self.__area[current_country])
            if population:
                print('Население:', self.__population[current_country])

            while True:
                answer = input()
                if answer.lower() == 'стоп':
                    self.__print_result()
                    return
                if self.__check_answer(answer, current_country) == 0:
                    continue
                break

    def country_info(self, country):
        return [self.__capital[country], self.__world_part[country], self.__area[country], self.__population[country]]

    __MAX_VALUE = 10 ** 18

    def get_info(
            self,
            world_parts=(
                'Европа',
                'Азия',
                'Африка',
                'Америка',
                'Австралия и Океания'),
            min_area_value=0,
            max_area_value=__MAX_VALUE,
            min_population_value=0,
            max_population_value=__MAX_VALUE):
        return self.__data_frame.loc[
            (self.__data_frame['Часть света'].isin(world_parts)) & (
                min_area_value <= self.__data_frame['Площадь']) & (
                self.__data_frame['Площадь'] <= max_area_value) & (
                min_population_value <= self.__data_frame['Население']) & (
                    self.__data_frame['Население'] <= max_population_value)]
