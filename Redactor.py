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

