import requests

my_base = "http://127.0.0.1:5000/"

data = [{"value": "12", "suit": "spades", "colour": "red"},
        {"value": "-1", "suit": "ace", "colour": "black"},
        {"value": "0", "suit": "clubs", "colour": "red"},
        {"value": "1", "suit": "diamonds", "colour": "black"}]

for i in range(len(data)):
        # Add a card to the list
        print(requests.put(my_base + "card/1", data[i]))

# should return with 'too many'
print(requests.put(my_base + "card/1", data[2]))

# should return ace, black, -1
print(requests.get(my_base + "card/1").json())

# Should delete ace, black, -1
print(requests.delete(my_base + "card/1"))

# Should error
print(requests.delete(my_base + "card/1"))


print(requests.get(my_base + "card/2").json())
# should replace 2 with 3
print(requests.patch(my_base + "card/2", data[3]))

print(requests.get(my_base + "card/2").json())

