import click
import os
import csv
import time

@click.group()
def cli():
    pass




@click.command()
@click.option('--filename', prompt='Enter name of your Note', help = "Name of your Note-File.")
def NewFile(filename):
    '''This func will create a new Note in this directory'''
    with open ("Notes.csv", "a", encoding="utf-8") as f:
        f.write("\n" + filename + ";" + "" + ";" + time.ctime())
cli.add_command(NewFile)

@click.command()
@click.option('--filename', prompt='Enter name of removal Note', help = 'Name of Existing Note, which you want to remove')
def RemoveFile(filename):
    os.remove(filename)
    click.echo("Succesfuly")
cli.add_command(RemoveFile)


# @click.command()
# @click.option('--filename', prompt='Enter name of redacting Note', help = "Name of redactable Note")
# def RedactFile(filename):
#     message = click.edit(filename=filename)
# cli.add_command(RedactFile)

if __name__ == "__main__":
    cli()

import os
import click
import pprint
import re
import csv
import time

@click.command("Create")
@click.argument("notename")
def Create(notename):
    '''
    "Имя заметки"\tСоздание заметки с таким именем
    '''
    with  open("Notes.csv", "r", encoding="utf-8") as file:
        file_reader = csv.reader(file, delimiter=";")
        for row in file_reader:
            if row[0] == notename:
                print("Заметка с таким именем уже есть")
                return
    with open("Notes.csv", "a", encoding="utf-8") as file:
        text = str(input("Текст заметки: "))
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        file_writer.writerow([str(notename), text, time.ctime()])


@click.command("Delete")
@click.argument("notename")
def Delete(notename):
    '''
    "Имя заметки"\t\t\tУдаление заметки с таким именем
    '''
    counter = 0
    with open("Notes.csv", "r",encoding="utf-8") as source:
        reader = csv.reader(source, delimiter=";")
        with open("dest.csv", "w", encoding="utf-8") as destination:
            writer = csv.writer(destination, delimiter=";", lineterminator="\r")
            for line in reader:
                if line[0]!=notename:
                    writer.writerow(line)
                else:
                    counter = 1
            if counter == 1:
                print(f"Заметка {notename} успешно удалена")
            else: 
                print("Такой заметки нет")
    os.remove("Notes.csv")
    os.rename("dest.csv", "Notes.csv")

@click.command("Redact")
@click.argument("notename")
def Redact(notename):
    '''
    "Имя заметки"\t\t\tРедактирование заметки с таким именем
    '''
    count = 0
    with open("Notes.csv", "r", encoding="utf-8") as source:
        reader = csv.reader(source, delimiter=";")
        with open("dest.csv", "w", encoding="utf-8") as destination:
            writer = csv.writer(destination, delimiter=";", lineterminator="\r")
            for row in reader:
                if row[0]!=notename:
                    writer.writerow(row)
                else:
                    count = 1
                    pprint.pprint(row[1])
                    temp = str(input("Участок для замены: "))
                    text = str(input("Текст для вставки: "))
                    try:
                        row[1] = row[1].replace(temp, text)
                        row[2] = time.ctime()
                        print(f"Заметка {notename} успешно изменена")
                        writer.writerow(row)
                    except:
                        print("Такого участка нет")
    if count == 0:
        print("Такой заметки нет")
    os.remove("Notes.csv")
    os.rename("dest.csv", "Notes.csv")

@click.command("ShowList")
def ShowList():
    '''
    \t\t\tВывод всех заметок
    '''
    with open("Notes.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for line in reader:
            print(f"{line[0]}\t{line[2]}\t")

@click.command("Show")
@click.argument("notename")
def Show(notename):
    '''
    "Имя заметки"\t\t\tВывод содержимого заметки с таким именем 
    '''
    with open("Notes.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for line in reader:
            if line[0]==notename:
                pprint.pprint(line[1])
                return
        else:
            print("Такой заметки нет")

@click.command("ShowByDate")
@click.option("--date", default="all", help = "Напишите день, за который нужно просмотреть заметки в формате дд.мм.гг")
def ShowByDate(date):
    '''
    --date=dd.mm.yy\t\tВывод заметок по указанной дате
    '''
    count = 0
    pattern = re.compile(r"\d\d.\d\d.\d\d")
    if date == "all":
        with open("Notes.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            for line in reader:
                print(f"{line[0]}\t{line[2]}\t")
    elif re.fullmatch(pattern, date):
        with open("Notes.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            for line in reader:
                try:
                    if (time.strptime(line[2]).tm_year == (2000 + int(date[-2:]))) and (time.strptime(line[2]).tm_mon == int(date[3:][:2])) and (time.strptime(line[2]).tm_mday==int(date[:2])):
                        count+=1
                        print(f"{line[0]}\t{line[2]}\t")
                except:
                    pass
            if count==0:
                print("Заметок по такой дате нет")
    else:
        print("Неверный формат даты")
    
    
@click.group()
def main():
    pass

main.add_command(Show)
main.add_command(ShowList)
main.add_command(Redact)
main.add_command(Delete)
main.add_command(Create)
main.add_command(ShowByDate)

if __name__ == "__main__":
    main()


    
