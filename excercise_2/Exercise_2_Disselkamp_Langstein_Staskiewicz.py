# donuts
# Given an integer count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'
def donuts(count):
    if type(count) == int:
        if count < 10:
            return 'Number of vegan donuts: ' + str(count)
        else:
            return 'Number of vegan donuts: many'
    else:
        return 'Passed count is not an Integer'


# verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    if len(s) >= 3:
        if(s[-3:] == 'ing'):
            return s + 'ly'
        else:
            return s + 'ing'
    else: 
        #return unchanged string
        return s


# Remove adjacent
# Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.
def remove_adjacent(nums):
    i = 0
    lst = []
    for item in nums:
        # Check if it is at the edge of the list
        if len(nums) > i+1:
            # Check if next item in nums is the same --> don´t push it in lst
            if item != nums[i+1]:
                lst.append(item)
        else:
            lst.append(item)
        i = i + 1
    return lst

def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))
    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))
    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))
# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()