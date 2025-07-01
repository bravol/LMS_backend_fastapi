from datetime import timedelta,datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from lib.repo import auth
from lib.database.tables import User,UserRolesEnum
from lib.utils.helpers import formatPhoneNumber
from lib.py_models.users import Login,Signup,UserModel,ChangePassword,ResetPassword,UserUpdate, ChangeRole,ToggleUserStatus

# LOGIN USER
def login_user(db:Session,data:Login):
    phone_number= formatPhoneNumber(data.phone_number)
    if not phone_number:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid phone number')
    data.phone_number=phone_number
    user= db.query(User).filter(User.phone_number==phone_number).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found, Please create account")
    user=auth.authenticate_user(db=db,user=data)
    access_token =auth.create_access_token(user,timedelta(hours=6))
    return {"access_token":access_token, "token_type":"bearer"}
    
# SIGN UP USER
def signup_user(db:Session,data:Signup):
    phone_number= formatPhoneNumber(data.phone_number)
    if not phone_number:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Correct phone number is required")
    data.phone_number = phone_number
    if db.query(User).filter(User.phone_number==phone_number).first():
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")
    
    hashed_password = auth.hash_password(data.password)
    user = User(phone_number=phone_number,password=hashed_password,full_name=data.full_name)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message":"User created Successfully","status":200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Failed to create User:{e}")

# GET USER DATA
def get_user_data( db: Session,user:UserModel,phone_number: str):
    phoneNumber= formatPhoneNumber(phone_number)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    try:
        user_db = db.query(User).filter(User.phone_number == phoneNumber).first()
        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user_db
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Error retrieving user data: {e}")


# CHANGE PASSWORD
def changePassword(db: Session, user:UserModel, data:ChangePassword):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user_db = db.query(User).filter(User.phone_number == user.phone_number).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        # Verify old password
        if not auth.verify_password(data.old_password, user_db.password):
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
        # Hash the new password
        hashed_password = auth.hash_password(data.new_password)
        user_db.password = hashed_password
        db.commit()
        db.refresh(user_db)

        return {"message": "Password changed successfully", "status": 200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not change password {e}")
    
# RESET PASSWORD
def reset_password(db: Session, data:ResetPassword):
    try:
        phone_number = formatPhoneNumber(data.phone_number)
        if phone_number is None:
            return {"message": "Invalid phone number", "status": 400}
        # Check if user exists
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            return {"message": "User does not exist", "status": 404}
        # Hash the new password
        hashed_password = auth.hash_password(data.new_password)   
        # Update user's password
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return {"message": "Password reset successfully", "status": 200}
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Password could not be reset {e}")


# GETTING USERS
def get_users(db: Session,user:UserModel, skip: int, limit: int):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin to access this data")
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"ERROR GETTING users: {e}")
    

# UPDATE USER
def update_user(db: Session, user:UserModel, phone_number: str, data: UserUpdate):
    try:
        phoneNumber = formatPhoneNumber(phone_number)
        user = db.query(User).filter(User.phone_number == phoneNumber).first()
        if not user:
            return {"message": "User not found", "status": 404}

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
            
        db.commit()
        return {"message": "User updated successfully", "status": 200}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update user")
    

# DELETE USER
def delete_user(db: Session, user:UserModel, phone_number: str):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin to delete this user")
    try:
        phoneNumber=formatPhoneNumber(phone_number)
        user_db = db.query(User).filter(User.phone_number == phoneNumber).first()
        if user_db:
            db.delete(user_db)
            db.commit()
        return {"message": "User deleted successfully", "status": 200}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"ERROR IN DELETING USER: {e}")
    
# CHANGING USER ROLE
def change_user_role(db:Session, user:UserModel, data:ChangeRole):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to change user roles.")

    try:
        phone_number = formatPhoneNumber(data.phone_number)
        user_db = db.query(User).filter(User.phone_number == phone_number).first()

        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found.")

        user_db.role = data.role
        db.commit()
        return {"message": "User role changed successfully","status": 200}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Error changing user role: {str(e)}")
    
# TOGGLE USER STATUS
def toggle_user_status(db:Session,user:UserModel,data:ToggleUserStatus):
    if user.role != UserRolesEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only admins can enable or disable users.")

    try:
        phone_number = formatPhoneNumber(data.phone_number)
        user_db = db.query(User).filter(User.phone_number == phone_number).first()

        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found.")

        user_db.is_active = data.is_active
        db.commit()

        action = "enabled" if data.is_active else "disabled"
        return {"message": f"User has been successfully {action}.","status": 200}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Error updating user status: {e}")