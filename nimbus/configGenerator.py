import configparser

# List of meaningful variable names and values
animal_names = ["Lion", "Tiger", "Elephant", "Giraffe", "Zebra"]
car_names = ["Ferrari", "Lamborghini", "Tesla", "Ford", "Chevrolet"]
scientist_names = ["Einstein", "Curie", "Tesla", "Newton", "Hawking"]

# Create an instance of ConfigParser
config = configparser.ConfigParser()

# Add a section and populate with meaningful variables and values
config["config"] = {
    "Favorite_Animal": animal_names[0],
    "Second_Favorite_Animal": animal_names[1],
    "Favorite_Car": car_names[0],
    "Second_Favorite_Car": car_names[1],
    "Favorite_Scientist": scientist_names[0],
    "Second_Favorite_Scientist": scientist_names[1],
}

# Write the config to a file named config.ini
with open("config.ini", "w") as configfile:
    config.write(configfile)

print("config.ini file populated")
