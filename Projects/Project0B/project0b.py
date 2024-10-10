first_part = "+-+"
second_part = "| |"
third_part = "+-+-+"
spaces = "  "

squares_num = range(int(input()))

print(first_part)

for i in squares_num:
    print(spaces * i + second_part)
    if i == len(squares_num)-1:
        break
    print(spaces * i + third_part)

print(spaces * squares_num[len(squares_num)-1] + first_part)
