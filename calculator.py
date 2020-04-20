from tkinter import *
import unicodedata
import math
from decimal import *
import re

root = Tk()

root.title("Calculator")
root.geometry('500x500+0+0')
root.minsize(400, 400)
root.config(background='black')


for row_index in range(9):
    Grid.rowconfigure(root, row_index, weight=1)
    for col_index in range(4):
        Grid.columnconfigure(root, col_index, weight=1)


T = Text(root, width=35, height=2, fg='white', borderwidth=5, bg='gray', state='disabled')

T.grid(row=0, columnspan=4, padx=10, pady=5, ipadx=2, ipady=10, sticky='NSEW')
# T.config(state="normal")
# T.insert("1.0", "me")
# T.insert(END, "a")
# T.delete("1.0", END)
# T.config(state="disabled")
e = Entry(root, width=35, borderwidth=5, fg='white', bg='black')
e.grid(row=1, columnspan=4, padx=10, pady=20, ipadx=2, ipady=10, sticky='NSEW')
e.insert(END, "0")
e.config(state="disabled")


def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))

# def button_clear():
#     e.delete(0, END)
#
# def button_add():
#     first_number = e.get()
#     global f_num
#     f_num = int(first_number)
#     e.delete(0, END)
#
# def button_equal():
#     second_number = e.get()
#     e.delete(0, END)
#     e.insert(0, f_num + int(second_number))


def button_number(number):
    e.config(state="normal")
    T.config(state="normal")

    if e.get() == "0":
        e.delete(0, END)
    if len(e.get()) > 0:
        if e.get().strip('\n')[-1] == "}":
            e.delete(0, END)
            T.delete("1.0", END)
    if len(T.get("1.0", END).strip('\n')) > 0:
        if T.get("1.0", END).strip('\n')[-1] == "=":
            e.delete(0, END)
            T.delete("1.0", END)
        elif T.get("1.0", END).strip('\n')[-1] == ")":
            return
    T.config(state="disabled")
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + str(number))
    e.config(state="disabled")


def button_symbol(symbol):
    e.config(state="normal")
    e.delete(0, END)
    e.insert(0, str(symbol))
    e.config(state="disabled")


def button_clear():
    T.config(state="normal")
    T.delete("1.0", END)
    T.config(state="disabled")
    e.config(state="normal")
    e.delete(0, END)
    e.insert(0, 0)
    e.config(state="disabled")
    return

def operation(op):
    T.config(state="normal")
    text = T.get("1.0", END).strip('\n')
    entry_text = e.get().strip('\n')
    T.delete("1.0", END)
    e.config(state="normal")
    e.delete(0, END)
    e.insert(0, "0")
    e.config(state="disabled")
    if len(text) > 0:
        if text[-1] == ')':
            T.insert("1.0", text + " " + op)
        else:
            T.insert("1.0", text + " " + entry_text + " " + op)

    else:
        T.insert("1.0", text + " " + entry_text + " " + op)
    T.config(state="disabled")

def equal():

    T.config(state="normal")
    if len(T.get("1.0", END).strip('\n')) > 0:
        if T.get("1.0", END).strip('\n')[-1] == "=":
            e.delete(0, END)
            T.delete("1.0", END)
    T.config(state="disabled")

    global count_l
    global count_r
    T.config(state="normal")
    text = T.get("1.0", END).strip('\n')
    entry_text = e.get().strip('\n')
    T.delete("1.0", END)
    e.config(state="normal")
    e.delete(0, END)
    e.insert(0, "0")
    e.config(state="disabled")
    if entry_text != "0":
        T.insert("1.0", text + " " + entry_text)
    else:
        T.insert("1.0", text)
    # T.insert("1.0", text + " " + entry_text)
    while count_l != count_r:
        T.insert(END, ' ) ')
        count_r += 1
    count_l = 0
    count_r = 0
    text = T.get("1.0", END).strip('\n')
    T.config(state="disabled")
    if text[-2] == ")":
        text = text[0: len(text) - 1]
    result = evaluate(text)
    if result is not None:
        T.config(state="normal")
        T.insert(END, " =")
        T.config(state="disabled")

        e.config(state="normal")
        e.delete(0, END)
        e.insert(0, str(result).strip("0"))
        e.config(state="disabled")

def isfloat(c):
    try:
        float(c)
        return True
    except ValueError:
        return False

def evaluate(expr):

    try:
        expr_list = expr.strip().split(' ')

        if len(expr_list) == 0:
            return 0

        number = 0
        pos = 0
        stack = []
        sign = '+'
        getcontext().prec = 10
        while pos < len(expr_list):
            character = expr_list[pos]
            if character.isdigit() or isfloat(character):
                number = number * 10 + float(character)
            if character == '(':
                # find the corresponding ")"
                end = 0
                clone = expr_list[pos:]
                posP = 0
                while end < len(clone):
                    if clone[end] == '(':
                        posP += 1
                    elif clone[end] == ')':
                        posP -= 1
                        if posP == 0:
                            break
                    end += 1
                # do recursion to calculate the sum within the next (...)
                number = evaluate(' '.join(expr_list[pos + 1: pos + end]))
                pos += end

            if pos + 1 == len(expr_list) or (character == '+' or character == '-' or character == '*' or character == '/'):
                if sign == '+':
                    stack.append(Decimal(number))
                elif sign == '-':
                    stack.append(Decimal(-number))
                elif sign == '*':
                    stack[-1] = Decimal(stack[-1]) * Decimal(number)
                elif sign == '/':
                    if int(number) != 0:
                        stack[-1] = Decimal(stack[-1]) / Decimal(float(number))
                    else:
                        raise ValueError("Cannot divide by 0")
                # if type(stack[-1]) == int:
                #     stack[-1] = int(stack[-1])
                sign = character
                number = 0
            pos += 1

        return sum(stack)
    except TypeError:
        T.config(state="normal")
        e.config(state="normal")
        T.delete("1.0", END)
        e.delete(0, END)
        e.insert(0, "{Error}")
        T.config(state="disabled")
        e.config(state="disabled")
        return

    except ValueError as err:
        T.config(state="normal")
        e.config(state="normal")
        T.delete("1.0", END)
        e.delete(0, END)
        e.insert(0, err.args)
        T.config(state="disabled")
        e.config(state="disabled")
        return

def add_decimal():
    e.config(state='normal')
    e.insert(END, '.')
    e.config(state='disabled')

def backspace():
    e.config(state='normal')
    text = e.get()
    e.delete(0, END)
    if len(text) == 1:
        e.insert(0, str(0))
    else:
        e.insert(0, text[0:len(text)-1])
    e.config(state='disabled')


count_l = 0
count_r = 0
def parenthesis(lr):
    global count_l
    global count_r

    T.config(state="normal")
    if count_l < count_r:
        return

    if lr == '(':
        count_l += 1
        if T.get("1.0", END) == "":
            T.insert(END, '(')
        else:
            T.insert(END, ' (')
    else:
        if count_l <= count_r:
            return
        count_r += 1

        text = T.get("1.0", END).strip('\n')
        entry_text = e.get().strip('\n')
        T.delete("1.0", END)
        e.config(state="normal")
        e.delete(0, END)
        e.insert(0, "0")
        e.config(state="disabled")
        T.insert("1.0", text + " " + entry_text + " )")
    T.config(state="disabled")

def absolute():
    T.config(state="normal")
    if len(T.get("1.0", END).strip('\n')) > 0:
        if T.get("1.0", END).strip('\n')[-1] == "=":
            e.delete(0, END)
            T.delete("1.0", END)
    T.config(state="disabled")
    e.config(state="normal")
    text = int(e.get())
    e.delete(0, END)
    e.insert(0, str(abs(text)))
    e.config(state="disabled")


def reciprocal():
    e.config(state="normal")
    text = int(e.get())
    e.delete(0, END)
    e.insert(0, str(1/text))
    e.config(state="disabled")


def negate():
    e.config(state="normal")

    text = e.get()
    if text[-1] == "-":
        e.delete(0, END)
        e.insert(0, text[1:])
    else:
        e.delete(0, END)
        e.insert(0, "-" + text)

    e.config(state="disabled")


def factorial():
    e.config(state="normal")


    n = float(e.get())

    if n.is_integer():
        result = math.factorial(int(e.get()))
    else:
        result = "{Has to be int}"

    e.delete(0, END)
    e.insert(0, str(result))

    e.config(state="disabled")


button_1 = Button(root, text="1", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(1))
button_2 = Button(root, text="2", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(2))
button_3 = Button(root, text="3", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(3))
button_4 = Button(root, text="4", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(4))
button_5 = Button(root, text="5", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(5))
button_6 = Button(root, text="6", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(6))
button_7 = Button(root, text="7", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(7))
button_8 = Button(root, text="8", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(8))
button_9 = Button(root, text="9", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(9))
button_0 = Button(root, text="0", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_number(0))
button_pi = Button(root, text=unicodedata.lookup("GREEK SMALL LETTER PI"), width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_symbol(math.pi))
button_e = Button(root, text="e", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_symbol(math.e))
button_clear = Button(root, text="C", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=button_clear)
button_backspace = Button(root, text="<-", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=backspace)
button_reciprocal = Button(root, text="1/x", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=reciprocal)
# button_mod = Button(root, text="mod", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: operation('%'))
button_abs = Button(root, text="|x|", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=absolute)
button_left_p = Button(root, text="(", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: parenthesis('('))
button_right_p = Button(root, text=")", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: parenthesis(')'))
button_fact = Button(root, text="x!", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=factorial)
# button_exp = Button(root, text="exp", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: button_click(0))
button_division = Button(root, text="/", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: operation('/'))
button_multiplication = Button(root, text="*", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: operation('*'))
button_subtraction = Button(root, text="-", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: operation('-'))
button_addition = Button(root, text="+", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=lambda: operation('+'))
button_equal = Button(root, text="=", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=equal)
button_dot = Button(root, text=".", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=add_decimal)
button_negate = Button(root, text="+/-", width=7, height=4, padx=0, pady=0, fg='white', bg='black', command=negate)

button_pi.grid(row=2, column=0, sticky='NSEW')
button_e.grid(row=2, column=1, sticky='NSEW')
button_clear.grid(row=2, column=2, sticky='NSEW')
button_backspace.grid(row=3, column=2, sticky='NSEW')
button_reciprocal.grid(row=3, column=0, sticky='NSEW')
button_abs.grid(row=3, column=1, sticky='NSEW')
# button_exp.grid(row=3, column=2, sticky='NSEW')
# button_mod.grid(row=3, column=3, sticky='NSEW')
button_left_p.grid(row=4, column=0, sticky='NSEW')
button_right_p.grid(row=4, column=1, sticky='NSEW')
button_fact.grid(row=4, column=2, sticky='NSEW')
button_division.grid(row=2, column=3, sticky='NSEW')
button_7.grid(row=5, column=0, sticky='NSEW')
button_8.grid(row=5, column=1, sticky='NSEW')
button_9.grid(row=5, column=2, sticky='NSEW')
button_multiplication.grid(row=3, column=3, sticky='NSEW')
button_4.grid(row=6, column=0, sticky='NSEW')
button_5.grid(row=6, column=1, sticky='NSEW')
button_6.grid(row=6, column=2, sticky='NSEW')
button_subtraction.grid(row=4, column=3, sticky='NSEW')
button_1.grid(row=7, column=0, sticky='NSEW')
button_2.grid(row=7, column=1, sticky='NSEW')
button_3.grid(row=7, column=2, sticky='NSEW')
button_addition.grid(row=5, column=3, sticky='NSEW')
button_negate.grid(row=8, column=0, sticky='NSEW')
button_0.grid(row=8, column=1, sticky='NSEW')
button_dot.grid(row=8, column=2, sticky='NSEW')
button_equal.grid(row=6, column=3, rowspan=3, sticky='NSEW')


def keyboard_action(event):
    if event.keysym == "BackSpace":
        backspace()
    elif event.keysym == "Return":
        equal()
    elif event.keysym == "parenleft" or event.keysym == "Shift_0":
        if event.keysym == "Shift_9":
            parenthesis('(')
        else:
            parenthesis(')')


def keyboard_num(event):
    if event.char == "e":
        button_symbol('e')
    elif event.char in ['+', '-', '*', '/']:
        operation(event.char)
    elif event.char == "=":
        equal()
    elif event.char == ".":
        add_decimal()
    elif event.char == "-":
        negate()
    elif event.char == "(" or event.char == ")":
        parenthesis(event.char)
    elif event.char == "!":
        factorial()
    else:
        button_number(event.char)


root.bind('1', keyboard_num)
root.bind('2', keyboard_num)
root.bind('3', keyboard_num)
root.bind('4', keyboard_num)
root.bind('5', keyboard_num)
root.bind('6', keyboard_num)
root.bind('7', keyboard_num)
root.bind('8', keyboard_num)
root.bind('9', keyboard_num)
root.bind('0', keyboard_num)
root.bind('e', keyboard_num)
root.bind('+', keyboard_num)
root.bind('-', keyboard_num)
root.bind('*', keyboard_num)
root.bind('/', keyboard_num)
root.bind('!', keyboard_num)
root.bind('<BackSpace>', keyboard_action)
root.bind('<Return>', keyboard_action)
root.bind('(', keyboard_num)
root.bind(')', keyboard_num)
root.mainloop()