imie = "Bohdan Susulovskyi"
index = imie.index(" ")
for i,ch in enumerate(imie):
    if i > index:
        print("\t"*(i-index-1),ch)
    else:
        print("\t"*i,ch)