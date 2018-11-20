import mongoengine


class Weather(mongoengine.Document):
    meta = {'collection': 'weather'}
    time = mongoengine.DateTimeField()
    location = mongoengine.StringField()
    condition = mongoengine.StringField()
    conditiondescription = mongoengine.StringField()
    temperature = mongoengine.DecimalField()
    pressure = mongoengine.DecimalField()
    humidity = mongoengine.DecimalField()
    windspeed = mongoengine.DecimalField()
    winddeg = mongoengine.DecimalField()

