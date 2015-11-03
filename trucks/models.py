from django.db import models
from django.utils import timezone
import csv
from flask_sqlalchemy import SQLAlchemy # Will this work???

# Create your models here.

class Truck(models.Model):
    """
    Turns truck facility permit records into collected objects
    """

    # __tablename__ = "trucks"
    
    #filter initial spreadsheet by Approved only; create process to remove 
    id = models.AutoField(primary_key=True)
    # db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = models.CharField(max_length=1000) #from city; Applicant
    permit_number = models.CharField(max_length=50) #from city; permit
    location_description = models.CharField(max_length=1000) #from city; LocationDescription
    food_items = models.CharField(max_length=250) #from city; FoodItems
    expiration_date = models.CharField(max_length=1000) #from city; ExpirationDate

    @classmethod
    def make_truck_records():
        # file_open = open("mobile_food_permits.csv")
        # file_read = csv.reader(file_open)

        file_read = csv.reader(open('mobile_food_permits.csv', 'rU'), quotechar='"', delimiter = ',')

        for row in file_read:
            # temp_object = Truck(row)
            # object_list.append(temp_object)
            # print temp_object
            name = row[1] #from city; Applicant
            permit_number = row[9] #from city; may not use
            location_description = row[4]
            food_items = row[11]
            expiration_date = row[21]

            temp_object = Truck(name=name, permit_number=permit_number, location_description=location_description, food_items=food_items, expiration_date=expiration_date)

            db.session.add(temp_object)

        db.session.commit()

        # return object_list
        print "Whoa, you made objects! And they apparently committed! Holy crap!"

class Truck_schedule(models.Model):

    # __tablename__ = "truck_schedule_information"

    schedule_line_id = models.AutoField(primary_key=True)
    # truck_id = models.ForeignKey('trucks.id') # not sure about this
    truck_name = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=50)
    permit_number = models.CharField(max_length=50)
    location_description = models.CharField(max_length=1000)
    extra_text = models.CharField(max_length=1000)
    location_id = models.CharField(max_length=50)
    schedule_id = models.CharField(max_length=50)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    x_coordinate = models.CharField(max_length=50)
    y_coordinate = models.CharField(max_length=50)

    @classmethod
    def make_truck_schedule(cls):
        file_read = csv.reader(open('Mobile_Food_Schedule.csv', 'rU'), quotechar='"', delimiter = ',')

        i = 1
        for row in file_read:
            if i % 100 == 0:
                print "Hello! ", i
            i += 1
            truck_name = row[9]
            truck_id_tuple = db.session.query(Truck.id).filter_by(name=truck_name).first()
            if not truck_id_tuple:
                continue
            else:
                truck_id = truck_id_tuple[0]
                
            # day_of_week, permit_number, location_description, extra_text, location_id,
            if row[0]:
                day_of_week = row[0]
            else: 
                day_of_week = ""

            if row[1]:
                permit_number = row[1]
            else:
                permit_number = ""

            if row[2]:
                # location_description = row[2].encode('latin1', errors='ignore')
                location_description = row[2].decode('utf8', errors='ignore')
            else: 
                location_description = ""

            if row[3]:
                extra_text = row[3].decode('utf8', errors='ignore')
            else: 
                extra_text = ""
  
            if row[4]:
                location_id = row[4]
            else: 
                location_id = ""

            if row[5]:
                schedule_id = row[5]
            else: 
                schedule_id = ""

            if row[6]:
                start_time = row[6]
            else:
                start_time = ""

            if row[7]:
                end_time = row[7]
            else: 
                end_time = ""

            if len(row) > 10:
                x_coordinate = row[10]
                y_coordinate = row[11]
            else:
                x_coordinate = ""
                y_coordinate = ""

            temp_object = cls(truck_id=truck_id, truck_name=truck_name, day_of_week=day_of_week, permit_number=permit_number, location_description=location_description, extra_text=extra_text, location_id=location_id, schedule_id=schedule_id, start_time=start_time, end_time=end_time, x_coordinate=x_coordinate, y_coordinate=y_coordinate)

            db.session.add(temp_object)

        db.session.commit()

        # return object_list
        print "Whoa, you made more objects! And they apparently committed again! Woohoo!"

    @classmethod
    def dump(self):

        return {"truckscheduleinfo": {'truck_id': self.truck_id,
                                    'truck_name': self.truck_name,
                                    'day_of_week': self.day_of_week,
                                    'permit_number': self.permit_number,
                                    'location_description': self.location_description,
                                    'extra_text': self.extra_text,
                                    'location_id': self.location_id,
                                    'schedule_id': self.schedule_id,
                                    'start_time': self.start_time,
                                    'end_time': self.end_time,
                                    'coordinates': self.coordinates}}