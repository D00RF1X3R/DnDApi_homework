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
            print("Описание: " + ans['desc'][0])
            print("В этом элементе также пристутствуют следующие элементы: ")
            keys: list = list(ans.keys())
            for i in keys:
                print(i, end=" | ")
                counter += 1
                if counter == 14:
                    print("\n")
            print("Введите название элемента, чтобы узнать о нем больше.")
            if inp in keys:
                result = inp
            elif inp not in command_list:
                print("Такого элемета нет, возможно вы ошиблись.")

        else:
            print('Введите команду из доступных или "help", чтобы увидеть их список.')

        if inp in command_list:
            if inp == "leave":
                is_working = False
            elif inp == "help":
                for i in command_list:
                    print(i + ": " + command_list[i])
            elif inp == "to_element" and result:
                result = ""
            elif inp == "to_part" and results:
                results = False
                remembered_part = remembered_part[:remembered_part.rfind("/")]
                print(remembered_part)
            elif inp == "to_start":
                remembered_part = ""


if __name__ == "__main__":
    main()
