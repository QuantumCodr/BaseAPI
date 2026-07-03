from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.modules.access.service import AccessService
from app.modules.users.service import UserService
from app.core.security import hash_password


def seed_permissions(db: Session):
    permissions = [
        "user.read",
        "user.write",
        "user.delete",
        "role.manage",
        "permission.manage",
        "admin.access",
    ]

    for perm in permissions:
        existing = AccessService.get_permission_by_name(db, perm)

        if not existing:
            AccessService.create_permission(
                db,
                name=perm,
                description=f"Allows {perm} action"
            )


def seed_roles(db: Session):
    roles = [
        {
            "name": "admin",
            "permissions": [
                "user.read",
                "user.write",
                "user.delete",
                "role.manage",
                "permission.manage",
                "admin.access",
            ],
        },
        {
            "name": "user",
            "permissions": [
                "user.read",
            ],
        },
    ]

    for role_data in roles:
        role = AccessService.get_role_by_name(db, role_data["name"])

        if not role:
            role = AccessService.create_role(
                db,
                name=role_data["name"],
                description=f"{role_data['name']} role"
            )

        for perm in role_data["permissions"]:
            AccessService.assign_permission_to_role(db, role, perm)


def seed_admin_user(db: Session):
    email = "admin@starterapi.com"
    password = "admin123"

    user = UserService.get_by_email(db, email)

    if not user:
        user = UserService.create(
            db,
            email=email,
            password_hash=hash_password(password),  # replace if needed
            is_verified=True
        )

    AccessService.assign_role_to_user(db, user, "admin")


def run_seed():
    db = SessionLocal()

    try:
        seed_permissions(db)
        seed_roles(db)
        seed_admin_user(db)

        print("✅ Seeding completed successfully")

    except Exception as e:
        print(f"❌ Seeding failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()