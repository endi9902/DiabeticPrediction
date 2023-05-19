class calculate_bmi:
    @staticmethod
    def calculate_bmi(weight, height):
        bmi = float(weight) / (float(height) ** 2)
        return bmi