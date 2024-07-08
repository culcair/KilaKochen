from typing import Optional

from sqlalchemy import Date, Double, ForeignKey, Index, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
import decimal

from typing import Any, List, Optional

from sqlalchemy import CHAR, Date, Double, ForeignKeyConstraint, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIT, DECIMAL, INTEGER, LONGTEXT, MEDIUMTEXT, TINYINT
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
    __tablename__ = 'anwender'

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    vorname: Mapped[str] = mapped_column(Text)
    user: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    mail: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(INTEGER(11))
    active: Mapped[int] = mapped_column(INTEGER(11))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)


class Allergene(db.Model):
    __tablename__ = 'allergene'
    __table_args__ = (
        Index('Bezeichnung', 'Bezeichnung', unique=True),
        Index('Kuerzel', 'Kuerzel', unique=True)
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Kuerzel: Mapped[str] = mapped_column(CHAR(2))
    Bezeichnung: Mapped[str] = mapped_column(String(50))
    Aktiv: Mapped[int] = mapped_column(TINYINT(1), server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    Beschreibung: Mapped[Optional[str]] = mapped_column(Text)
    Kommentar: Mapped[Optional[str]] = mapped_column(Text)

    zutaten_allergene: Mapped[List['ZutatenAllergene']] = relationship('ZutatenAllergene', back_populates='allergene')


class Einheiten(db.Model):
    __tablename__ = 'einheiten'
    __table_args__ = (
        Index('Bezeichnung', 'Bezeichnung', unique=True),
        Index('Kuerzel', 'Kuerzel', unique=True)
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Kuerzel: Mapped[str] = mapped_column(CHAR(3))
    Bezeichnung: Mapped[str] = mapped_column(String(50))
    Beschreibung: Mapped[str] = mapped_column(MEDIUMTEXT)
    Aktiv: Mapped[int] = mapped_column(TINYINT(1), server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    BasiseinheitID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    BasiseinheitFaktor: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 8))
    Kommentar: Mapped[Optional[str]] = mapped_column(Text)
    Sortierung: Mapped[Optional[int]] = mapped_column(TINYINT(2))

    rezepte_zutaten: Mapped[List['RezepteZutaten']] = relationship('RezepteZutaten', back_populates='einheiten')


class Rezeptkategorien(db.Model):
    __tablename__ = 'rezeptkategorien'
    __table_args__ = (
        Index('BezeichnungPlural', 'BezeichnungPlural', unique=True),
        Index('BezeichnungSingular', 'BezeichnungSingular', unique=True),
        Index('Kuerzel', 'Kuerzel', unique=True),
        Index('URL', 'URL', unique=True)
    )

    ID: Mapped[int] = mapped_column(INTEGER(10), primary_key=True)
    BezeichnungSingular: Mapped[str] = mapped_column(String(50))
    BezeichnungPlural: Mapped[str] = mapped_column(String(50))
    URL: Mapped[str] = mapped_column(String(60))
    Aktiv: Mapped[int] = mapped_column(TINYINT(1), server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    Ueberarbeitet: Mapped[Any] = mapped_column(BIT(1))
    Beschreibung: Mapped[Optional[str]] = mapped_column(MEDIUMTEXT)
    Kuerzel: Mapped[Optional[str]] = mapped_column(CHAR(3))
    Sortierung: Mapped[Optional[int]] = mapped_column(TINYINT(2))

    rezepte: Mapped[List['Rezepte']] = relationship('Rezepte', back_populates='rezeptkategorien')
    speiseplan: Mapped[List['Speiseplan']] = relationship('Speiseplan', back_populates='rezeptkategorien')


class Zutatengruppen(db.Model):
    __tablename__ = 'zutatengruppen'
    __table_args__ = (
        Index('Bezeichnung', 'Bezeichnung', unique=True),
        Index('Kuerzel', 'Kuerzel', unique=True)
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Bezeichnung: Mapped[str] = mapped_column(String(50))
    Aktiv: Mapped[int] = mapped_column(TINYINT(1), server_default=text('1'))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    Ueberarbeitet: Mapped[Any] = mapped_column(BIT(1))
    Kuerzel: Mapped[Optional[str]] = mapped_column(CHAR(3))
    Sortierung: Mapped[Optional[int]] = mapped_column(TINYINT(2))

    zutaten: Mapped[List['Zutaten']] = relationship('Zutaten', back_populates='zutatengruppen')


class Rezepte(db.Model):
    __tablename__ = 'rezepte'
    __table_args__ = (
        ForeignKeyConstraint(['KategorieID'], ['rezeptkategorien.ID'], name='rezepte_rezeptkategorien'),
        Index('Titel', 'Titel', unique=True),
        Index('rezepte_rezeptkategorien', 'KategorieID')
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Titel: Mapped[str] = mapped_column(String(50))
    Zubereitung: Mapped[str] = mapped_column(LONGTEXT)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    Ueberarbeitet: Mapped[Any] = mapped_column(BIT(1))
    author: Mapped[str] = mapped_column(MEDIUMTEXT)
    created_at: Mapped[datetime.date] = mapped_column(Date)
    KategorieID: Mapped[Optional[int]] = mapped_column(INTEGER(10))

    rezeptkategorien: Mapped['Rezeptkategorien'] = relationship('Rezeptkategorien', back_populates='rezepte')
    essensplan_beilage: Mapped[List['Essensplan']] = relationship('Essensplan', foreign_keys='[Essensplan.BeilageRezeptID]', back_populates='Beilage')
    essensplan_dessert: Mapped[List['Essensplan']] = relationship('Essensplan', foreign_keys='[Essensplan.DessertRezeptID]', back_populates='Dessert')
    essensplan_hauptgericht: Mapped[List['Essensplan']] = relationship('Essensplan', foreign_keys='[Essensplan.HauptgerichtRezeptID]', back_populates='Hauptgericht')
    rezepte_zutaten: Mapped[List['RezepteZutaten']] = relationship('RezepteZutaten', back_populates='rezepte')
    speiseplan: Mapped[List['Speiseplan']] = relationship('Speiseplan', back_populates='rezepte')


class Zutaten(db.Model):
    __tablename__ = 'zutaten'
    __table_args__ = (
        ForeignKeyConstraint(['GruppeID'], ['zutatengruppen.ID'], name='zutaten_zutatengruppen'),
        Index('Bezeichnung', 'Bezeichnung', unique=True),
        Index('zutaten_zutatengruppen_ID', 'GruppeID')
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Bezeichnung: Mapped[str] = mapped_column(String(50))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    Ueberarbeitet: Mapped[Any] = mapped_column(BIT(1))
    Beschreibung: Mapped[Optional[str]] = mapped_column(MEDIUMTEXT)
    GruppeID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Aktiv: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text('1'))
    Sortierung: Mapped[Optional[int]] = mapped_column(TINYINT(2))
    zutat_quelle: Mapped[Optional[str]] = mapped_column(MEDIUMTEXT)
    zutat_auth: Mapped[Optional[str]] = mapped_column(MEDIUMTEXT)
    zutat_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    zutatengruppen: Mapped['Zutatengruppen'] = relationship('Zutatengruppen', back_populates='zutaten')
    rezepte_zutaten: Mapped[List['RezepteZutaten']] = relationship('RezepteZutaten', back_populates='zutaten')
    zutaten_allergene: Mapped[List['ZutatenAllergene']] = relationship('ZutatenAllergene', back_populates='zutaten')


class Essensplan(db.Model):
    __tablename__ = 'essensplan'
    __table_args__ = (
        ForeignKeyConstraint(['BeilageRezeptID'], ['rezepte.ID'], name='essensplan_rezepte_Beilage'),
        ForeignKeyConstraint(['DessertRezeptID'], ['rezepte.ID'], name='essensplan_rezepte_Dessert'),
        ForeignKeyConstraint(['HauptgerichtRezeptID'], ['rezepte.ID'], name='essensplan_rezepte_Hautgericht'),
        Index('Datum', 'Datum', unique=True),
        Index('essensplan_rezepte_Beilage', 'BeilageRezeptID'),
        Index('essensplan_rezepte_Dessert', 'DessertRezeptID'),
        Index('essensplan_rezepte_Hautgericht', 'HauptgerichtRezeptID')
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Datum: Mapped[datetime.date] = mapped_column(Date)
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    HauptgerichtRezeptID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    BeilageRezeptID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    DessertRezeptID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Ausfall: Mapped[Optional[str]] = mapped_column(String(50))
    Anmerkung: Mapped[Optional[str]] = mapped_column(String(400))

    Beilage: Mapped['Rezepte'] = relationship('Rezepte', foreign_keys=[BeilageRezeptID], back_populates='essensplan_beilage')
    Dessert: Mapped['Rezepte'] = relationship('Rezepte', foreign_keys=[DessertRezeptID], back_populates='essensplan_dessert')
    Hauptgericht: Mapped['Rezepte'] = relationship('Rezepte', foreign_keys=[HauptgerichtRezeptID], back_populates='essensplan_hauptgericht')


class RezepteZutaten(db.Model):
    __tablename__ = 'rezepte_zutaten'
    __table_args__ = (
        ForeignKeyConstraint(['EinheitID'], ['einheiten.ID'], onupdate='CASCADE', name='rezepte_zutaten_einheiten'),
        ForeignKeyConstraint(['RezeptID'], ['rezepte.ID'], ondelete='CASCADE', onupdate='CASCADE', name='rezepte_zutaten_rezepte'),
        ForeignKeyConstraint(['ZutatID'], ['zutaten.ID'], ondelete='CASCADE', onupdate='CASCADE', name='rezepte_zutaten_zutaten'),
        Index('RezeptID_ZutatID', 'RezeptID', 'ZutatID', unique=True),
        Index('rezepte_zutaten_einheiten', 'EinheitID'),
        Index('rezepte_zutaten_zutaten', 'ZutatID')
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    RezeptID: Mapped[int] = mapped_column(INTEGER(11))
    ZutatID: Mapped[int] = mapped_column(INTEGER(11))
    Menge: Mapped[decimal.Decimal] = mapped_column(Double(asdecimal=True))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    Ueberarbeitet: Mapped[Any] = mapped_column(BIT(1))
    EinheitID: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    einheiten: Mapped['Einheiten'] = relationship('Einheiten', back_populates='rezepte_zutaten')
    rezepte: Mapped['Rezepte'] = relationship('Rezepte', back_populates='rezepte_zutaten')
    zutaten: Mapped['Zutaten'] = relationship('Zutaten', back_populates='rezepte_zutaten')


class Speiseplan(db.Model):
    __tablename__ = 'speiseplan'
    __table_args__ = (
        ForeignKeyConstraint(['RezeptID'], ['rezepte.ID'], onupdate='CASCADE', name='speiseplan_rezepte'),
        ForeignKeyConstraint(['RezeptkategorieID'], ['rezeptkategorien.ID'], onupdate='CASCADE', name='speiseplan_rezeptkategorien'),
        Index('Datum_RezeptkategorieID', 'Datum', 'RezeptkategorieID', unique=True),
        Index('speiseplan_rezepte', 'RezeptID'),
        Index('speiseplan_rezeptkategorien', 'RezeptkategorieID')
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Datum: Mapped[datetime.date] = mapped_column(Date)
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
    RezeptkategorieID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    RezeptID: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Anmerkung: Mapped[Optional[str]] = mapped_column(String(400))

    rezepte: Mapped['Rezepte'] = relationship('Rezepte', back_populates='speiseplan')
    rezeptkategorien: Mapped['Rezeptkategorien'] = relationship('Rezeptkategorien', back_populates='speiseplan')


class ZutatenAllergene(db.Model):
    __tablename__ = 'zutaten_allergene'
    __table_args__ = (
        ForeignKeyConstraint(['AllergenID'], ['allergene.ID'], ondelete='CASCADE', onupdate='CASCADE', name='zutaten_allergene_allergene'),
        ForeignKeyConstraint(['ZutatID'], ['zutaten.ID'], ondelete='CASCADE', onupdate='CASCADE', name='zutaten_allergene_zutaten'),
        Index('ZutatID_AllergenID', 'ZutatID', 'AllergenID', unique=True),
        Index('zutaten_allergene_allergene', 'AllergenID')
    )

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    ZutatID: Mapped[int] = mapped_column(INTEGER(11))
    AllergenID: Mapped[int] = mapped_column(INTEGER(11))
    Stand: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    allergene: Mapped['Allergene'] = relationship('Allergene', back_populates='zutaten_allergene')
    zutaten: Mapped['Zutaten'] = relationship('Zutaten', back_populates='zutaten_allergene')
