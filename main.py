from tkinter import *
from tkinter import filedialog
import subprocess
import os
import csv


def main():
    if not os.path.isfile("WherePascal.txt"):
        open("WherePascal.txt", "w")

    global tests_cnt
    tests_cnt = 0

    global dirr
    dirr = ""

    global programs
    programs = []

    root = Tk()
    root.title("Pascal Tester")
    root.geometry('600x600')

    def WherePas():
        file = filedialog.askdirectory(
            initialdir="/",
            title="Select PascalABC.NET folder",
        )

        open("WherePascal.txt", "w").write(file)
        print(file)

        if os.path.isfile(f"{file}/pabcnetcclear.exe"):
            findPas.configure(bg='#93D976')
            lbl2.configure(text=f'PascalABC.NET\n{open("WherePascal.txt", "r").read()}')

    findPas = Button(root, text="Расположение PascalABC.NET",
                     command=WherePas,
                     font="Arial 15")

    lbl2 = Label(root, text=f'PascalABC.NET\n{open("WherePascal.txt", "r").read()}', font="Arial 10", padx=10)
    lbl2.grid(column=1, row=4)

    where = open("WherePascal.txt", "r").read()
    if os.path.isfile(f"{where}/pabcnetcclear.exe"):
        findPas.configure(bg='#93D976')
        lbl2.configure(text=f'PascalABC.NET\n{open("WherePascal.txt", "r").read()}')
    else:
        findPas.configure(bg="red")
        lbl2.configure(text=f'PascalABC.NET\nНЕ ВЫБРАНО')

    findPas.grid(column=1, row=1, pady=10)

    lbl = Label(root, text="Тест", font="Arial 15", padx=10, pady=10)
    lbl.grid(column=0, row=2, pady=(20, 10))

    lbl1 = Label(root, text="Ответ", font="Arial 15", padx=10, pady=10)
    lbl1.grid(column=1, row=2, pady=(20, 10))

    def compilation(file):
        where = f'"{open("WherePascal.txt", "r").read()}/pabcnetcclear.exe"'
        atop = file[:-4]
        atop = atop + ".exe"
        file = '"' + file + '"'

        try:
            subprocess.check_output(f"{where} {file}")
        except subprocess.CalledProcessError:
            atop += "CE"

        programs.append(atop)

    def clicked():
        lbl4.configure(text=f'Тестрование\nНЕ НАЧАЛОСЬ', bg='#f0f0f0')

        global programs
        programs = []

        global tests_cnt
        global dirr

        file = filedialog.askopenfilenames(
            initialdir="/",
            title="Выберите папку с решениями",
            filetypes=[('Pascal files', '*.pas')]
        )

        dirr = os.path.dirname(file[0])
        lbl3.configure(text=f'Папка с программами учеников\n{dirr}')
        root.update()

        if not os.path.isdir(f"{dirr}/ERROR_LOG"):
            os.mkdir(f"{dirr}/ERROR_LOG")

        cnt = 0
        pas_cnt = len(file)
        for i in file:
            cnt += 1

            p = str(cnt/pas_cnt * 100)
            p = p[:p.find('.')]
            percent = p + '%'

            lbl4.configure(text=f'Компиляция\n{percent}')
            root.update()

            compilation(f"{i}")

        if not os.path.isdir(f'"{dirr}/Tests"'):
            os.system(f'mkdir "{dirr}/Tests"')

        lbl4.configure(text=f'Компиляция завершена!\nМожете начинать тестирование', bg='#93D976')
        root.update()

    lbl3 = Label(root, text=f'Папка с программами учеников\nНЕ ВЫБРАНО', font="Arial 10", padx=10)
    lbl3.grid(column=1, row=5)

    lbl4 = Label(root, text=f'Компиляция\nНЕ ИДЕТ', font="Arial 10", padx=10)
    lbl4.grid(column=1, row=6)

    btn = Button(root, text="Выбрать", command=clicked, font="Arial 15", width=20)
    btn.grid(column=0, row=1)

    def inp():
        global tests_cnt, dirr

        testValue = Test.get("1.0", "end-1c")
        ansValue = Ans.get("1.0", "end-1c")

        if testValue[len(testValue)-1] != '\n':
            testValue += '\n'

        if ansValue[len(ansValue) - 1] != '\n':
            ansValue += '\n'

        if testValue != "" and ansValue != "":
            tests_cnt += 1
            testfile = open(f"{dirr}/Tests/in{tests_cnt}.txt", "w")
            ansfile = open(f"{dirr}/Tests/out{tests_cnt}.txt", "w")
            testfile.write(testValue)
            ansfile.write(ansValue)

        Test.delete("1.0", "end-1c")
        Ans.delete("1.0", "end-1c")

    Test = Text(root, height=10, width=30)
    Test.grid(column=0, row=3, padx=10)

    Ans = Text(root, height=10, width=30)
    Ans.grid(column=1, row=3, padx=10)

    addtests = Button(root, text="Добавить тест", command=inp, font="Arial 15", width=20)
    addtests.grid(column=0, row=4, pady=(10, 30))

    def cl():
        global tests_cnt

        tests_cnt = 0
        dir = os.listdir(f"{dirr}/Tests")
        for i in dir:
            os.remove(f"{dirr}/Tests/{i}")

    cleart = Button(root, text="Очистить тесты", command=cl, font="Arial 15", width=20)
    cleart.grid(column=0, row=6)

    def see():
        os.startfile(f"{dirr}/Tests")

    see = Button(root, text="Посмотреть тесты", command=see, font="Arial 15", width=20)
    see.grid(column=0, row=5, pady=10)

    def checker():
        global dirr
        global tests_cnt

        tests_cnt = len(os.listdir(f"{dirr}/Tests")) // 2

        fields = ["Имя"]
        for i in range(tests_cnt):
            fields.append("Тест" + str(i + 1))

        rows = []

        cnt_programs = len(programs)
        cnt = 0

        for i in programs:
            cnt += 1

            p = str((cnt / cnt_programs) * 100)
            p = p[:p.find('.')]
            percent = p + '%'

            lbl4.configure(text=f'Тестрование\n{percent}', bg='#f0f0f0')
            root.update()

            atop = i[str(i).rfind('/') + 1:]

            if i[-2::] == "CE":
                atop = atop[:-6]
                atop += ".pas"
                row = [atop]
                for j in range(tests_cnt):
                    row.append("CE")
                rows.append(row)
                continue

            atop = atop[:-4]
            atop += ".pas"
            row = [atop]

            name = atop[:-4] + ".txt"
            log = open(f"{dirr}/ERROR_LOG/{name}", "w")

            for j in range(tests_cnt):
                v = open(f"{dirr}/Tests/out{j + 1}.txt", 'r').read()
                right = open(f"{dirr}/Tests/in{j + 1}.txt", 'r').read()

                result = subprocess.check_output(f'"{i}" < "{dirr}/Tests/in{j + 1}.txt"', shell=True).decode("utf-8")
                result = result.replace('\r', '')
                v = v.replace('\r', '')

                log.write(f"====== Тест #{j + 1} =======\n")
                log.write("--- Входные данные ---\n")
                log.write(right + '\n')
                log.write("--- Результат работы ---\n")
                log.write(result + '\n')
                log.write("--- Правильный ответ ---\n")
                log.write(v + '\n')
                log.write("--- Вывод проверяющей программы ---\n")

                if result != v:
                    log.write("WA\n\n")
                    row.append("WA")
                else:
                    log.write("OK\n\n")
                    row.append("OK")

            rows.append(row)

            lbl4.configure(text=f'Тестрование закончено!', font='Arial 12', bg='#93D976')
            root.update()

        print(rows)

        name = f"{dirr}/results.csv"

        with open(name, 'w', encoding='utf-8') as file:
            write = csv.writer(file)
            write.writerow(fields)

            write.writerows(rows)

    startcheck = Button(root, text="Начать проверку", command=checker, font="Arial 15", width=20)
    startcheck.grid(column=0, row=7, pady=30)

    def op():
        os.startfile(f"{dirr}/results.csv")

    check = Button(root, text="Результаты", command=op, font="Arial 15", width=20)
    check.grid(column=1, row=7)

    root.mainloop()


if __name__ == '__main__':
    main()
