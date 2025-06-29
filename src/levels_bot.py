def show_bot_level(idx):
    level1 = {
        "name": "very_easy",
        "epochs": "100",
        "accuracy": "85.9%",
        "average loss": "2.070778",
    }

    level2 = {
        "name": "easy",
        "epochs": "250",
        "accuracy": "84.8%",
        "average loss": "0.396488",
    }

    level3 = {
        "name": "medium",
        "epochs": "500",
        "accuracy": "90.2%",
        "average loss": "0.239477",
    }

    level4 = {
        "name": "difficult",
        "epochs": "1000",
        "accuracy": "94.6%",
        "average loss": "0.131517",
    }

    level5 = {
        "name": "statistically_impossible",
        "epochs": "2500",
        "accuracy": "100.0%",
        "average loss": "0.049081",
    }

    if idx == 1:
        s  = "difficulty: " + level1["name"] + "\n" 
        s += "epochs: " + level1["epochs"] + "\n" 
        s += "accuracy: " + level1["accuracy"] + "\n"
        s += "average loss: " + level1["average loss"] + "\n"
        return s
    elif idx == 2:
        s = "difficulty: " + level2["name"] + "\n" 
        s += "epochs: " + level2["epochs"] + "\n" 
        s += "accuracy: " + level2["accuracy"] + "\n"
        s += "average loss: " + level2["average loss"] + "\n"
        return s
    elif idx == 3:
        s = "difficulty: " + level3["name"] + "\n" 
        s += "epochs: " + level3["epochs"] + "\n" 
        s += "accuracy: " + level3["accuracy"] + "\n"
        s += "average loss: " + level3["average loss"] + "\n"
        return s
    elif idx == 4:
        s = "difficulty: " + level4["name"] + "\n" 
        s += "epochs: " + level4["epochs"] + "\n" 
        s += "accuracy: " + level4["accuracy"] + "\n"
        s += "average loss: " + level4["average loss"] + "\n"
        return s
    else:
        s = "difficulty: " + level5["name"] + "\n" 
        s += "epochs: " + level5["epochs"] + "\n" 
        s += "accuracy: " + level5["accuracy"] + "\n"
        s += "average loss: " + level5["average loss"] + "\n"
        return s
