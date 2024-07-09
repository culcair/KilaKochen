from typing import Any, List, Optional

from sqlalchemy import CHAR, DECIMAL, INTEGER, TEXT, Date, Double, ForeignKeyConstraint, Index, String, TIMESTAMP, Text, text
#from sqlalchemy.dialects.mysql import BIT, DECIMAL, INTEGER, LONGTEXT, MEDIUMTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
import decimal

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from kilakochen import login, db



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

   
class User(db.Model, UserMixin):
    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    vorname: Mapped[str] = mapped_column(Text)
    user: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    mail: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(INTEGER)
    active: Mapped[int] = mapped_column(INTEGER)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)


class Allergene(db.Model):
    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Kuerzel: Mapped[str] = mapped_column(CHAR(2),index=True)
    Bezeichnung: Mapped[str] = mapped_column(String(50),index=True)
    Aktiv: Mapped[int] = mapped_column(INTEGER, default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    Beschreibung: Mapped[Optional[str]] = mapped_column(Text)
    Kommentar: Mapped[Optional[str]] = mapped_column(Text)

    zutaten_allergene: Mapped[List['ZutatenAllergene']] = relationship('ZutatenAllergene', back_populates='allergene')


class Einheiten(db.Model):
    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Kuerzel: Mapped[str] = mapped_column(CHAR(3),index=True)
    Bezeichnung: Mapped[str] = mapped_column(String(50),index=True)
    Beschreibung: Mapped[str] = mapped_column(TEXT)
    Aktiv: Mapped[int] = mapped_column(INTEGER, server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    BasiseinheitID: Mapped[Optional[int]] = mapped_column(INTEGER)
    BasiseinheitFaktor: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 8))
    Kommentar: Mapped[Optional[str]] = mapped_column(Text)
    Sortierung: Mapped[Optional[int]] = mapped_column(INTEGER)

    rezepte_zutaten: Mapped[List['RezepteZutaten']] = relationship('RezepteZutaten', back_populates='einheiten')


class Rezeptkategorien(db.Model):
    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    BezeichnungSingular: Mapped[str] = mapped_column(String(50),index=True)
    BezeichnungPlural: Mapped[str] = mapped_column(String(50),index=True)
    URL: Mapped[str] = mapped_column(String(60),index=True)
    Aktiv: Mapped[int] = mapped_column(INTEGER, server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    Ueberarbeitet: Mapped[Any] = mapped_column(INTEGER)
    Beschreibung: Mapped[Optional[str]] = mapped_column(TEXT)
    Kuerzel: Mapped[Optional[str]] = mapped_column(CHAR(3),index=True)
    Sortierung: Mapped[Optional[int]] = mapped_column(INTEGER)

    rezepte: Mapped[List['Rezepte']] = relationship('Rezepte', back_populates='rezeptkategorien')
    speiseplan: Mapped[List['Speiseplan']] = relationship('Speiseplan', back_populates='rezeptkategorien')


class Zutatengruppen(db.Model):
    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Bezeichnung: Mapped[str] = mapped_column(String(50),index=True)
    Aktiv: Mapped[int] = mapped_column(INTEGER, server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    Ueberarbeitet: Mapped[Any] = mapped_column(INTEGER)
    Kuerzel: Mapped[Optional[str]] = mapped_column(CHAR(3),index=True)
    Sortierung: Mapped[Optional[int]] = mapped_column(INTEGER)

    zutaten: Mapped[List['Zutaten']] = relationship('Zutaten', back_populates='zutatengruppen')


class Rezepte(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['KategorieID'], ['rezeptkategorien.ID'], name='rezepte_rezeptkategorien'),
    )

    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Titel: Mapped[str] = mapped_column(String(50),index=True)
    Zubereitung: Mapped[str] = mapped_column(TEXT)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    Ueberarbeitet: Mapped[Any] = mapped_column(INTEGER)
    author: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime.date] = mapped_column(Date)
    KategorieID: Mapped[Optional[int]] = mapped_column(INTEGER)

    rezeptkategorien: Mapped['Rezeptkategorien'] = relationship('Rezeptkategorien', back_populates='rezepte')
    essensplan_beilage: Mapped[List['Essensplan']] = relationship('Essensplan', foreign_keys='[Essensplan.BeilageRezeptID]', back_populates='Beilage')
    essensplan_dessert: Mapped[List['Essensplan']] = relationship('Essensplan', foreign_keys='[Essensplan.DessertRezeptID]', back_populates='Dessert')
    essensplan_hauptgericht: Mapped[List['Essensplan']] = relationship('Essensplan', foreign_keys='[Essensplan.HauptgerichtRezeptID]', back_populates='Hauptgericht')
    rezepte_zutaten: Mapped[List['RezepteZutaten']] = relationship('RezepteZutaten', back_populates='rezepte')
    speiseplan: Mapped[List['Speiseplan']] = relationship('Speiseplan', back_populates='rezepte')


class Zutaten(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['GruppeID'], ['zutatengruppen.ID'], name='zutaten_zutatengruppen'),
    )

    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Bezeichnung: Mapped[str] = mapped_column(String(50),index=True)
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    Ueberarbeitet: Mapped[Any] = mapped_column(INTEGER)
    Beschreibung: Mapped[Optional[str]] = mapped_column(TEXT)
    GruppeID: Mapped[Optional[int]] = mapped_column(INTEGER)
    Aktiv: Mapped[Optional[int]] = mapped_column(INTEGER, server_default=text('1'))
    Sortierung: Mapped[Optional[int]] = mapped_column(INTEGER)
    zutat_quelle: Mapped[Optional[str]] = mapped_column(TEXT)
    zutat_auth: Mapped[Optional[str]] = mapped_column(TEXT)
    zutat_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    zutatengruppen: Mapped['Zutatengruppen'] = relationship('Zutatengruppen', back_populates='zutaten')
    rezepte_zutaten: Mapped[List['RezepteZutaten']] = relationship('RezepteZutaten', back_populates='zutaten')
    zutaten_allergene: Mapped[List['ZutatenAllergene']] = relationship('ZutatenAllergene', back_populates='zutaten')


class Essensplan(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['BeilageRezeptID'], ['rezepte.ID'], name='essensplan_rezepte_Beilage'),
        ForeignKeyConstraint(['DessertRezeptID'], ['rezepte.ID'], name='essensplan_rezepte_Dessert'),
        ForeignKeyConstraint(['HauptgerichtRezeptID'], ['rezepte.ID'], name='essensplan_rezepte_Hautgericht'),
    )

    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Datum: Mapped[datetime.date] = mapped_column(Date,index=True)
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    HauptgerichtRezeptID: Mapped[Optional[int]] = mapped_column(INTEGER)
    BeilageRezeptID: Mapped[Optional[int]] = mapped_column(INTEGER)
    DessertRezeptID: Mapped[Optional[int]] = mapped_column(INTEGER)
    Ausfall: Mapped[Optional[str]] = mapped_column(String(50))
    Anmerkung: Mapped[Optional[str]] = mapped_column(String(400))

    Beilage: Mapped['Rezepte'] = relationship('Rezepte', foreign_keys=[BeilageRezeptID], back_populates='essensplan_beilage')
    Dessert: Mapped['Rezepte'] = relationship('Rezepte', foreign_keys=[DessertRezeptID], back_populates='essensplan_dessert')
    Hauptgericht: Mapped['Rezepte'] = relationship('Rezepte', foreign_keys=[HauptgerichtRezeptID], back_populates='essensplan_hauptgericht')


class RezepteZutaten(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['EinheitID'], ['einheiten.ID'], onupdate='CASCADE', name='rezepte_zutaten_einheiten'),
        ForeignKeyConstraint(['RezeptID'], ['rezepte.ID'], ondelete='CASCADE', onupdate='CASCADE', name='rezepte_zutaten_rezepte'),
        ForeignKeyConstraint(['ZutatID'], ['zutaten.ID'], ondelete='CASCADE', onupdate='CASCADE', name='rezepte_zutaten_zutaten'),
    )

    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    RezeptID: Mapped[int] = mapped_column(INTEGER)
    ZutatID: Mapped[int] = mapped_column(INTEGER)
    Menge: Mapped[decimal.Decimal] = mapped_column(Double(asdecimal=True))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    Ueberarbeitet: Mapped[Any] = mapped_column(INTEGER)
    EinheitID: Mapped[Optional[int]] = mapped_column(INTEGER)

    einheiten: Mapped['Einheiten'] = relationship('Einheiten', back_populates='rezepte_zutaten')
    rezepte: Mapped['Rezepte'] = relationship('Rezepte', back_populates='rezepte_zutaten')
    zutaten: Mapped['Zutaten'] = relationship('Zutaten', back_populates='rezepte_zutaten')


class Speiseplan(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['RezeptID'], ['rezepte.ID'], onupdate='CASCADE', name='speiseplan_rezepte'),
        ForeignKeyConstraint(['RezeptkategorieID'], ['rezeptkategorien.ID'], onupdate='CASCADE', name='speiseplan_rezeptkategorien'),
        Index('Datum_RezeptkategorieID', 'Datum', 'RezeptkategorieID', unique=True),
        Index('speiseplan_rezepte', 'RezeptID'),
        Index('speiseplan_rezeptkategorien', 'RezeptkategorieID')
    )

    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    Datum: Mapped[datetime.date] = mapped_column(Date)
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))
    RezeptkategorieID: Mapped[Optional[int]] = mapped_column(INTEGER)
    RezeptID: Mapped[Optional[int]] = mapped_column(INTEGER)
    Anmerkung: Mapped[Optional[str]] = mapped_column(String(400))

    rezepte: Mapped['Rezepte'] = relationship('Rezepte', back_populates='speiseplan')
    rezeptkategorien: Mapped['Rezeptkategorien'] = relationship('Rezeptkategorien', back_populates='speiseplan')


class ZutatenAllergene(db.Model):
    __table_args__ = (
        ForeignKeyConstraint(['AllergenID'], ['allergene.ID'], ondelete='CASCADE', onupdate='CASCADE', name='zutaten_allergene_allergene'),
        ForeignKeyConstraint(['ZutatID'], ['zutaten.ID'], ondelete='CASCADE', onupdate='CASCADE', name='zutaten_allergene_zutaten'),
        Index('ZutatID_AllergenID', 'ZutatID', 'AllergenID', unique=True),
        Index('zutaten_allergene_allergene', 'AllergenID')
    )

    ID: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    ZutatID: Mapped[int] = mapped_column(INTEGER)
    AllergenID: Mapped[int] = mapped_column(INTEGER)
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(datetime.timezone.utc))

    allergene: Mapped['Allergene'] = relationship('Allergene', back_populates='zutaten_allergene')
    zutaten: Mapped['Zutaten'] = relationship('Zutaten', back_populates='zutaten_allergene')
