def count_number_of_occurence(string: str, sub_string: str) -> int:
    pos: int = 0
    count: int = 0

    while True:
        pos = string.find(sub_string, pos) + 1
        if pos == 0:
            break
        count += 1
    return count


res = count_number_of_occurence('baabacdcdcdc', 'baa')
print(res)
