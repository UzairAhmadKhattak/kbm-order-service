import typer
from order_service.src.session import get_db  
from models import Role  
from constants import UserConstants

app = typer.Typer()


@app.command(name="populate-roles")
def populate_roles():

    db = next(get_db())
    for role_data in [UserConstants.CUSTOMER_ROLE.value,
                      UserConstants.DELIVERER_ROLE.value,
                      UserConstants.SUPER_ADMIN.value]:
        # Check if the role already exists
        existing_role = db.query(Role).filter_by(name=role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
    db.commit()

    print("Roles populated!")

if __name__ == "__main__":
    app()
