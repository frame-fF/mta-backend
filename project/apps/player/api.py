from ninja import Router
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from .models import Player
from .schemas import (
    RegisterSchema,
    LoginSchema,
    PlayerSchema,
    MessageSchema,
    TokenSchema,
)

router = Router()


@router.post("/register", response={201: TokenSchema, 400: MessageSchema})
def register(request, data: RegisterSchema):
    """
    Register a new player account
    """
    try:
        # ตรวจสอบว่า email ไม่เป็นค่าว่าง
        if not data.email or data.email.strip() == "":
            return 400, {"message": "Email is required"}

        # ตรวจสอบว่า password ตรงกันหรือไม่
        if data.password != data.password_confirm:
            return 400, {"message": "Passwords do not match"}

        # ตรวจสอบว่า username มีอยู่แล้วหรือไม่
        if Player.objects.filter(username=data.username).exists():
            return 400, {"message": "Username already exists"}

        # ตรวจสอบว่า email มีอยู่แล้วหรือไม่
        if Player.objects.filter(email=data.email).exists():
            return 400, {"message": "Email already exists"}

        # สร้าง user ใหม่
        player = Player.objects.create(
            username=data.username,
            email=data.email,
            password=make_password(data.password),
            first_name=data.first_name or "",
            last_name=data.last_name or "",
        )

        # Login อัตโนมัติหลังจากลงทะเบียน
        login(request, player)

        # สร้าง session token (ใช้ session key เป็น token)
        token = request.session.session_key

        return 201, {"token": token, "user": PlayerSchema.from_orm(player)}

    except IntegrityError as e:
        return 400, {"message": f"Registration failed: {str(e)}"}
    except Exception as e:
        return 400, {"message": f"An error occurred: {str(e)}"}


@router.post("/login", response={200: TokenSchema, 401: MessageSchema})
def login_user(request, data: LoginSchema):
    """
    Login with username and password
    """
    # Authenticate user
    user = authenticate(request, username=data.username, password=data.password)

    if user is not None:
        # Login successful
        login(request, user)

        # สร้าง session token
        token = request.session.session_key

        return 200, {"token": token, "user": PlayerSchema.from_orm(user)}
    else:
        # Login failed
        return 401, {"message": "Invalid username or password"}


@router.post("/logout", response={200: MessageSchema})
def logout_user(request):
    """
    Logout current user
    """
    logout(request)
    return 200, {"message": "Logged out successfully"}


@router.get("/me", response={200: PlayerSchema, 401: MessageSchema})
def get_current_user(request):
    """
    Get current logged in user information
    """
    if request.user.is_authenticated:
        return 200, PlayerSchema.from_orm(request.user)
    else:
        return 401, {"message": "Not authenticated"}
