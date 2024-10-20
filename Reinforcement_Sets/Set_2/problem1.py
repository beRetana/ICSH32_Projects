
def find_max(nums: list[int])-> int:

    if nums == [] or nums == None or type(nums) != list:
        return None;

    _largest = nums[0]

    try:
        if len(nums) > 1:
            if nums[1] > _largest:
                _largest = nums[1]
                nums.pop(0)
            else:
                nums.pop(1)

            if len(nums) >= 2:
                _largest = find_max(nums)
    
    except TypeError:
        print("The list contains a value other than ints")
        
    return _largest


if __name__ == "__main__":
    assert find_max([0,-1,-500,234,5,2,6,3,-500, 234]) == 234
    assert find_max([0]) == 0
    assert find_max([]) == None
    assert find_max(9) == None
    assert find_max([10000000000*-1,-1,-500,234,5,2,6,3,-500,"500"]) == 234
    assert find_max([-1,-500,-234,-5]) == -1
    assert find_max([-1,5,3]) == 5
