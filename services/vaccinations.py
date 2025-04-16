from datetime import timedelta, date
class VaccinationHelper:
    @staticmethod
    def calculate_due_date(last_vacc_date: date, months_until_due: int = 6) -> date:
        """
        Returns the date when the next vaccination is due, based on the last vaccination date.
        """
        return last_vacc_date + timedelta(days=months_until_due * 30)

    @staticmethod
    def process_animal_vaccinations(animal_data: dict) -> dict:
        """
        Accepts a single animal dict, adds 'vaccination_due_date' if applicable, and returns it.
        """
        last_vacc = animal_data.get("own_animal_last_vacc")
        if last_vacc:
            try:
                due_date = VaccinationHelper.calculate_due_date(last_vacc)
                animal_data["vaccination_due_date"] = due_date.isoformat()
            except Exception as e:
                animal_data["vaccination_due_date"] = None
        else:
            animal_data["vaccination_due_date"] = None

        return animal_data
