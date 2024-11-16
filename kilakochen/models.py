from typing import List

from sqlalchemy import Table, Column, FLOAT, Date
from sqlalchemy import (
    INTEGER,
    String,
    DATETIME,
    Text,
    BOOLEAN,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from kilakochen import login, db


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    ADMIN_LEVEL = 15
    EDITOR_LEVEL = 10
    USER_LEVEL = 5

    ACCESS_LEVEL = {USER_LEVEL: "USER", EDITOR_LEVEL: "EDITOR", ADMIN_LEVEL: "ADMIN"}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    given_name: Mapped[str] = mapped_column(Text)
    username: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, nullable=True)
    level: Mapped[int] = mapped_column(INTEGER, nullable=True)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    last_seen: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )

    def set_password(self, password) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    @staticmethod
    def test_password(password):
        return generate_password_hash(password)

    def __init__(
        self, username=None, given_name=None, first_name=None, level=1, active=True, email=None
    ) -> None:
        self.given_name = given_name
        self.first_name = first_name
        self.username = username
        self.level = level
        self.active = active
        self.email = email

    def __repr__(self) -> str:
        return f"<User {self.username} {self.id}>"


class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    active: Mapped[bool] = mapped_column(BOOLEAN, default=True)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients_group.id"), nullable=True
    )
    group: Mapped["IngredientsGroup"] = relationship(
        "IngredientsGroup", back_populates="ingredients"
    )

    recipes: Mapped[list["Recipe"]] = relationship(
        "RecipeIngredient", back_populates="ingredient"
    )

    # Many-to-Many Beziehung zu Ingredient
    allergens: Mapped[list["Allergen"]] = relationship(
        "Allergen", secondary="ingredient_allergen", back_populates="ingredients"
    )
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )


class Allergen(db.Model):
    __tablename__ = "allergen"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    # Many-to-Many Beziehung zu Ingredient
    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient", secondary="ingredient_allergen", back_populates="allergens"
    )

    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )


ingredient_allergen_table = Table(
    "ingredient_allergen",
    db.Model.metadata,
    Column("IngredientID", INTEGER, db.ForeignKey("ingredient.id"), primary_key=True),
    Column("AllergenID", INTEGER, db.ForeignKey("allergen.id"), primary_key=True),
)


class IngredientsGroup(db.Model):
    __tablename__ = "ingredients_group"
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String(3))
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient", back_populates="group"
    )
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id"), primary_key=True
    )
    amount: Mapped[float] = mapped_column(FLOAT, nullable=False)

    # Beziehungen zu Recipe, Ingredient und Unit
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="recipes"
    )

    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.id"))
    unit: Mapped["Unit"] = relationship("Unit")

    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )


class Recipe(db.Model):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("recipe_category.id"), nullable=False
    )
    category: Mapped["RecipeCategory"] = relationship("RecipeCategory")

    # Beziehung zu RecipeIngredient
    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan"
    )

    meal_plan_side_dish: Mapped[List["MealPlan"]] = relationship(
        "MealPlan",
        foreign_keys="[MealPlan.side_dish_id]",
        back_populates="side_dish",
    )
    meal_plan_dessert: Mapped[List["MealPlan"]] = relationship(
        "MealPlan",
        foreign_keys="[MealPlan.dessert_id]",
        back_populates="dessert",
    )
    meal_plan_main_dish: Mapped[List["MealPlan"]] = relationship(
        "MealPlan",
        foreign_keys="[MealPlan.main_dish_id]",
        back_populates="main_dish",
    )

    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )


class RecipeCategory(db.Model):
    __tablename__ = "recipe_category"
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String(3))
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)


class Unit(db.Model):
    __tablename__ = "unit"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )  # z.B. "g", "ml", "Stück"
    code: Mapped[str] = mapped_column(String(3))
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )


class MealPlan(db.Model):
    __tablename__ = "meal_plan"
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    outage: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME, default=lambda: datetime.now(timezone.utc), nullable=True
    )

    main_dish_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=True)
    dessert_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=True)
    side_dish_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=True)

    side_dish: Mapped["Recipe"] = relationship(
        "Recipe", foreign_keys=[side_dish_id], back_populates="meal_plan_side_dish"
    )
    dessert: Mapped["Recipe"] = relationship(
        "Recipe", foreign_keys=[dessert_id], back_populates="meal_plan_dessert"
    )
    main_dish: Mapped["Recipe"] = relationship(
        "Recipe",
        foreign_keys=[main_dish_id],
        back_populates="meal_plan_main_dish",
    )

    def __repr__(self):
        return f"MealPlan {self.date.isoformat()} {str(self.id)}"
