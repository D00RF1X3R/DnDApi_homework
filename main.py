import requests as r


def main():
    url: str = "https://www.dnd5eapi.co/api/"
    command_list: dict = {"help": "Выводит доступные команды.", "leave": "покидает программу.",
                          "to_part": "Возвращает к выбору из списка раздела.",
                          "to_start": "Возвращает к выбору раздела."}
    is_working: bool = True
    results: bool = False
    counter: int = 0
    remembered_part: str = ""
    result: str = ""
    available_ops: list = []
    while is_working is True:
        if not remembered_part:
            print('О чем бы вы хотели узнать? Чтобы узнать команды для работы с приложением, введите'
                  ' "help". Доступные разделы:')
            ans: dict = r.get(url).json()
            keys: list = list(ans.keys())
            if len(keys) > 14:
                print(" | ".join(keys[:len(keys) // 2]))
                print(" | ".join(keys[(len(keys) // 2):]))
            else:
                print(" | ".join(keys))
            inp: str = input()
            if inp in keys:
                remembered_part: str = inp
            elif inp not in command_list:
                print("Такого элемета нет, возможно вы ошиблись.")

        elif remembered_part and not results:
            print(f"Вы обратились к разделу: {remembered_part}. Выберите интересующую вас часть:")
            ans: dict = r.get(url + remembered_part).json()
            for i in range(len(ans['results']) - 1):
                print(ans['results'][i]['index'], end=" | ")
                available_ops.append(ans['results'][i]['index'])
                counter += 1
                if counter == 14:
                    counter = 0
                    print('\n')
            counter = 0
            print(ans['results'][-1]['index'])
            inp: str = input()
            if inp in available_ops:
                remembered_part = remembered_part + "/" + inp
                results: bool = True
            elif inp not in command_list:
                print("Такого элемета нет, возможно вы ошиблись.")

        elif not result:
            print(
                f"Вы обратились к элементу {remembered_part.split('/')[-1]} раздела {remembered_part.split('/')[-2]}."
                f" Выберите интересующую вас часть:")
            ans: dict = r.get(url + remembered_part).json()
            print("Имя:" + ans['name'])
            print("В этом элементе также пристутствуют следующие элементы: ")
            keys: list = list(ans.keys())
            for i in keys:
                print(i, end=" | ")
                counter += 1
                if counter == 14:
                    print("")
            counter = 0
            print(keys[-1])
            print("Введите название элемента, чтобы узнать о нем больше.")
            inp: str = input()
            if inp in keys:
                result = inp
            elif inp not in command_list:
                print("Такого элемета нет, возможно вы ошиблись.")

        else:
            work_with = ans[result]
            if type(work_with) is dict:
                for i in work_with:
                    if i != 'index' and i != 'dc':
                        print(i.capitalize() + ": " + work_with[i])
            elif type(work_with) is bool:
                print(result.capitalize() + ": " + "Нет" if not work_with else "Да")
            elif type(work_with) is str or type(work_with) is int:
                print(result.capitalize() + ": " + work_with)
            elif type(work_with) is list:
                if len(work_with) > 0:
                    if type(work_with[0]) is dict:
                        for i in work_with:
                            for j in i:
                                if j != "index":
                                    print(j.capitalize() + ": " + i[j])
                    else:
                        for i in range(len(work_with)):
                            if i != 0:
                                print(work_with[i])
                            else:
                                print(result.capitalize() + ": ", end='')
                                print(work_with[i])
            result = ""
            print(
                'Сейчас вы вернетесь к выбору элемента введите "ok", чтобы продолжить,'
                ' но вы можете ввести команду или "help", чтобы увилеть их список.')
            inp: str = input()
            if inp not in command_list and inp != "ok":
                print("Такой команды нет, возможно вы ошиблись.")

        if inp in command_list:
            if inp == "leave":
                is_working = False
            elif inp == "help":
                for i in command_list:
                    print(i + ": " + command_list[i])
            elif inp == "to_part" and results:
                results = False
                remembered_part = remembered_part[:remembered_part.rfind("/")]
            elif inp == "to_start":
                remembered_part = ""
                results = False
                result = ""


if __name__ == "__main__":
    main()
