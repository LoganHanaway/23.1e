from app import app, db, Pet

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Define some initial pets
        pets = [
            Pet(name='Fluffy', species='cat', photo_url='http://example.com/fluffy.jpg', age=3, notes='Loves to play with balls of yarn', available=True),
            Pet(name='Rex', species='dog', photo_url='http://example.com/rex.jpg', age=5, notes='Very friendly and loves to go for walks', available=True),
            Pet(name='Spike', species='porcupine', photo_url='http://example.com/spike.jpg', age=2, notes='A bit prickly but very cute', available=False),
            Pet(name='Bella', species='cat', photo_url='http://example.com/bella.jpg', age=1, notes='Shy but very loving once she gets to know you', available=True),
        ]

        # Add pets to the session and commit
        db.session.add_all(pets)
        db.session.commit()

        print("Database seeded!")

if __name__ == '__main__':
    seed_data()
