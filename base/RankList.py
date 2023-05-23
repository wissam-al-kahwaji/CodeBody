def update_rank(self):
        switcher = {
            1: "Bronze III",
            2: "Bronze IV",
            3: "Bronze V",
            4: "Silver III",
            5: "Silver IV",
            6: "Silver V",
            7: "Gold III",
            8: "Gold IV",
            9: "Gold V",
            10: "Platinum III",
            11: "Platinum IV",
            12: "Platinum V",
            13: "Diamond III",
            14: "Diamond IV",
            15: "Diamond V",
            16: "Master III",
            17: "Master IV",
            18: "Master V",
            19: "Grandmaster III",
            20: "Grandmaster IV",
            21: "Grandmaster V",
            22: "legendary III",
            23: "legendary IV",
            24: "legendary V"
            }
        LogoUrl = {
            1: "Rank/BronzeIII.svg",
            2: "Rank/BronzeIV.svg",
            3: "Rank/BronzeV.svg",
            4: "Rank/SilverIII.svg",
            5: "Rank/SilverIV.svg",
            6: "Rank/SilverV.svg",
            7: "Rank/GoldIII.svg",
            8: "Rank/GoldIV.svg",
            9: "Rank/GoldV.svg",
            10: "Rank/PlatinumIII.svg",
            11: "Rank/PlatinumIV.svg",
            12: "Rank/PlatinumV.svg",
            13: "Rank/DiamondIII.svg",
            14: "Rank/DiamondIV.svg",
            15: "Rank/DiamondV.svg",
            16: "Rank/MasterIII.svg",
            17: "Rank/MasterIV.svg",
            18: "Rank/MasterV.svg",
            19: "Rank/GrandmasterIII.svg",
            20: "Rank/GrandmasterIV.svg",
            21: "Rank/GrandmasterV.svg",
            22: "Rank/legendaryIII.svg",
            23: "Rank/legendaryIV.svg",
            24: "Rank/legendaryV.svg"
        }
        rank_num = 0
        if self.respect < 50:
            rank_num = 1  # Bronze III
        elif self.respect < 100:
            rank_num = 2  # Bronze IV
        elif self.respect < 200:
            rank_num = 3  # Bronze V
        elif self.respect < 350:
            rank_num = 4  # Silver III
        elif self.respect < 450:
            rank_num = 5  # Silver IV
        elif self.respect < 800:
            rank_num = 6  # Silver V
        elif self.respect < 2000:
            rank_num = 7  # Gold III
        elif self.respect < 5000:
            rank_num = 8  # Gold IV
        elif self.respect < 7000:
            rank_num = 9  # Gold V
        elif self.respect < 15000:
            rank_num = 10  # Platinum III
        elif self.respect < 30000:
            rank_num = 11  # Platinum IV
        elif self.respect < 50000:
            rank_num = 12  # Platinum V
        elif self.respect < 75000:
            rank_num = 13  # Diamond III
        elif self.respect < 100000:
            rank_num = 14  # Diamond IV
        elif self.respect < 150000:
            rank_num = 15  # Diamond V
        elif self.respect < 200000:
            rank_num = 16  # Master III
        elif self.respect < 250000:
            rank_num = 17  # Master IV
        elif self.respect < 350000:
            rank_num = 18  # Master V
        elif self.respect < 450000:
            rank_num = 19  # Grandmaster III
        elif self.respect < 650000:
            rank_num = 20  # Grandmaster IV
        elif self.respect <= 750000:
            rank_num = 21  # Grandmaster V
        elif self.respect <= 1000000:
            rank_num = 22  # legendary III
        elif self.respect <= 1500000:
            rank_num = 23  # legendary IV
        elif self.respect <= 2000000:
            rank_num = 24  # legendary V
        else:
            rank_num = 24  # legendary V


        
        self.rank = switcher.get(rank_num, "Invalid Rank")
        self.Logo_rank = LogoUrl.get(rank_num, "Rank/BronzeIII.svg")
