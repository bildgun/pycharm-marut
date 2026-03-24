for i in range(99,0,-1):
    if i == 1:
        print(f"{i} bottle of beer on the wall, {i} bottle of beer. \nTake one down and pass it around\nNo more bottles of beer on the wall, no more bottles of beer.\nGo to the store and buy some more, 99 bottles of beer on the wall.")
    else:
        print(f"{i} bottles of beer on the wall, {i} bottles of beer. \nTake one down and pass it around, \n{i-1} bottles of beer on the wall\n")