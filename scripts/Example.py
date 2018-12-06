import random, requests
from datetime import *

class Example(): 

    def __init__(self,):
        self.staff_list = {
            '001' : {
                'staff_id' : 'Lucia Buhr',
                'staff_title' : 'Nurse',
                'unit' : 'Surgical intensive care',
            }, 
            '002' : {
                'staff_id' : 'Joseph Pace',
                'staff_title' : 'Doctor',
                'unit' : 'Surgical intensive care',
            },
            '003' : {
                'staff_id' : 'Thurman Converse',
                'staff_title' : 'Nurse', 
                'unit' : 'Surgical intensive care',
            },
            '004' : {
                'staff_id' : 'Rob Brown',
                'staff_title' : 'Nurse',
                'unit' : 'Long term intensive care',
            },
            '005' : {
                'staff_id' : 'Rex Campbell',
                'staff_title' : 'Nurse',
                'unit' : 'Long term intensive care'
            },
            '006' : {
                'staff_id' : 'Janet Jackson',
                'staff_title' : 'Nurse',
                'unit' : 'Long term intensive care'
            },
            '007' : {
                'staff_id' : 'Earl O. Singer',
                'staff_title' : 'Nurse',
                'unit' : 'Long term intensive care'
            },
            '008' : {
                'staff_id' : 'Steven White',
                'staff_title' : 'Doctor',
                'unit' : 'Long term intensive care'
            },
            '009' : {
                'staff_id' : 'Brenda Crouse',
                'staff_title' : 'Nurse',
                'unit' : 'Pediatric intensive care'
            },
            '010' : {
                'staff_id' : 'Sharon Price',
                'staff_title' : 'Nurse',
                'unit' : 'Pediatric intensive care'
            },
            '011' : {
                'staff_id' : 'Diane Lambert',
                'staff_title' : 'Nurse',
                'unit' : 'Pediatric intensive care'
            },
            '012' : {
                'staff_id' : 'Susan Klein',
                'staff_title' : 'Nurse',
                'unit' : 'Pediatric intensive care'
            },
            '013' : {
                'staff_id' : 'Ruby Demars',
                'staff_title' : 'Nurse',
                'unit' : 'Pediatric intensive care'
            },
            '014' : {
                'staff_id' : 'John Bailey',
                'staff_title' : 'Nurse',
                'unit' : 'Pediatric intensive care'
            },
        }
        self.responses = {
            "Entry" :["Clean", "Not clean", "Not clean", "Not clean"], #75% not clean
            #"Alert":["Alert given", "No alert"],
            "Dispenser" : ["None"]
        }
    def random_date(self, 
            start= datetime.strptime('9/10/2017 1:30 PM', '%m/%d/%Y %I:%M %p'), 
            end= datetime.strptime('9/18/2018 4:50 AM', '%m/%d/%Y %I:%M %p')):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60 * 1000000) + delta.microseconds
        # int_delta = 9 * 60 * 60 * 1000000
        random_second = random.randrange(int_delta)
        return (datetime.now() - timedelta(microseconds=random_second))

    def node_ID_generator(self,):
        return str(random.randint(1,10))

    def room_number_generator(self,):
        return str(random.randint(1,10))

    def druid_decoration(self, length):
        for i in range(length):
            staff = self.staff_list[random.choice(self.staff_list.keys())]
            node_id = self.node_ID_generator()
            room_number = self.room_number_generator()
            response_type = random.choice(self.responses.keys())
            response_message = random.choice(self.responses[response_type])
            time = self.random_date()

            payload = {
                'type': response_type, 
                'staffID': staff['staff_id'],
                'nodeID': node_id, 
                'unit': staff['unit'],  
                'room_number': room_number,
                'staff_title': staff['staff_title'],
                'response_type': response_type,
                'response_message': response_message, 
                'time': time.isoformat(),
                }
            # requests.post('http://192.168.0.103:8200/v1/post/hospital', 
            #     json=payload, 
            #     headers={'Content-Type' : 'application/json'}
            #     ).json()
            if response_message == 'Not clean':
                try:
                    time = time.replace(second = time.second + 30)
                except:
                    time = time.replace(minute = time.minute + 1, second = time.second - 30) 
                payload = {
                    'type': 'Alert', 
                    'staffID': staff['staff_id'],
                    'nodeID': node_id, 
                    'unit': staff['unit'],  
                    'room_number': room_number,
                    'staff_title': staff['staff_title'],
                    'response_type': 'Alert',
                    'response_message': random.choice(['Alert given','No Alert', 'No Alert']), # 33% no wash
                    'time': time.isoformat(),
                    }
                # requests.post('http://192.168.0.103:8200/v1/post/hospital', 
                #     json=payload, 
                #     headers={'Content-Type' : 'application/json'}
                #     ).json()

if __name__ == '__main__':
    generator = Example()
    generator.druid_decoration(1)
    