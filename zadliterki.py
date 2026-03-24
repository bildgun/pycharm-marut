imie = "Bohdan Susulovskyi"
for i,ch in enumerate(imie):
    if i > 6:
        print("\t"*(i-7),ch)
    else:
        print("\t"*i,ch)