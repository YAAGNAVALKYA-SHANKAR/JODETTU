from datetime import timedelta,datetime
class VaccinationDues:
    @staticmethod
    def calculate_due_date(last_vacc_date:datetime,months_until_due:int=6)->datetime:
        return last_vacc_date+timedelta(days=months_until_due*30)
    @staticmethod
    def vaccinations(animal_data:dict)->dict:
        last_vacc=animal_data.get("own_animal_last_vacc")
        if last_vacc:
            try:
                due_date=VaccinationDues.calculate_due_date(last_vacc)
                animal_data["vaccination_due_date"]=due_date.isoformat()
            except Exception as e:
                animal_data["vaccination_due_date"]=None
        else:
            animal_data["vaccination_due_date"]=None
        return animal_data