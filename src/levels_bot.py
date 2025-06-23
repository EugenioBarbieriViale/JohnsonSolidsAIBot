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
        sa = "difficulty: " + level1["name"] + "\n" 
        sb = "epochs: " + level1["epochs"] + "\n" 
        sc = "accuracy: " + level1["accuracy"] + "\n"
        sd = "average loss: " + level1["average loss"] + "\n"
        return sa + sb + sc + sd
    elif idx == 2:
        sa = "difficulty: " + level2["name"] + "\n" 
        sb = "epochs: " + level2["epochs"] + "\n" 
        sc = "accuracy: " + level2["accuracy"] + "\n"
        sd = "average loss: " + level2["average loss"] + "\n"
        return sa + sb + sc + sd
    elif idx == 3:
        sa = "difficulty: " + level3["name"] + "\n" 
        sb = "epochs: " + level3["epochs"] + "\n" 
        sc = "accuracy: " + level3["accuracy"] + "\n"
        sd = "average loss: " + level3["average loss"] + "\n"
        return sa + sb + sc + sd
    elif idx == 4:
        sa = "difficulty: " + level4["name"] + "\n" 
        sb = "epochs: " + level4["epochs"] + "\n" 
        sc = "accuracy: " + level4["accuracy"] + "\n"
        sd = "average loss: " + level4["average loss"] + "\n"
        return sa + sb + sc + sd
    else:
        sa = "difficulty: " + level5["name"] + "\n" 
        sb = "epochs: " + level5["epochs"] + "\n" 
        sc = "accuracy: " + level5["accuracy"] + "\n"
        sd = "average loss: " + level5["average loss"] + "\n"
        return sa + sb + sc + sd
