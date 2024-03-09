from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

# Create engine to connect to SQLite database
engine = create_engine('sqlite:///users.db')

# Create base class for declarative class definitions
Base = declarative_base()

# Create session class for database interactions
Session = sessionmaker(bind=engine)

# Define User class for database table 'users'
class User(Base):
    __tablename__ = 'users'

    # Define table columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    # Constructor to initialize User instances
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    # Method to set hashed password using bcrypt
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method to check if provided password matches stored hashed password
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Function to retrieve user by user ID
def get_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    return user

# Function to retrieve user by email
def get_user_by_email(email):
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    return user

# Function to create a new user
def create_user(user):
    session = Session()
    user.set_password(user.password)
    del user.password  # Remove plain text password from memory
    session.add(user)
    session.commit()
    session.close()

# Function to update user information
def update_user(user_id, new_user):
    session = Session()
    user = session.query(User).get(user_id)
    user.name = new_user.name
    user.email = new_user.email
    user.set_password(new_user.password)
    session.commit()
    session.close()

# Function to delete user
def delete_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    session.close()

# Create tables in the database
Base.metadata.create_all(engine)
