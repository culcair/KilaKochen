from flask_sqlalchemy import SQLAlchemy
from typing import Optional
from sqlalchemy import Column, Date, Double, ForeignKey, Index, Integer, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, TEXT
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
import datetime
import decimal

db = SQLAlchemy()

class Essensplan(db.Model):
    __tablename__ = 'essensplan'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    kw: Mapped[int] = mapped_column(INTEGER(11))
    jahr: Mapped[int] = mapped_column(INTEGER(11))
    wtag: Mapped[int] = mapped_column(INTEGER(11))
    hgericht: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    beilage: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    dessert: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    ausfall: Mapped[Optional[str]] = mapped_column(Text)
    note: Mapped[Optional[str]] = mapped_column(Text)

class Mengenangabe(db.Model):
    __tablename__ = 'mengenangabe'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)
    abkz: Mapped[str] = mapped_column(TEXT)


class Rezepte(db.Model):
    __tablename__ = 'rezepte'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)
    desc: Mapped[str] = mapped_column(TEXT)
    cat: Mapped[str] = mapped_column(TEXT)
    hgericht: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    beilage: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    dessert: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    auth: Mapped[str] = mapped_column(TEXT)
    date: Mapped[datetime.date] = mapped_column(Date)
    text: Mapped[str] = mapped_column(MEDIUMTEXT)

zutat_allergen_association = Table(
    'zutat_allergen', db.metadata,
    Column('zutat_id', Integer, ForeignKey('zutat.id')),
    Column('allergen_id', Integer, ForeignKey('allergene.id'))
)

class Allergene(db.Model):
    __tablename__ ='allergene'
    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    kurzzeichen: Mapped[str] = mapped_column(TEXT)
    desc: Mapped[str] = mapped_column(TEXT)
    zutaten: Mapped[list["Zutaten"]] = relationship(
        'Zutat', secondary=zutat_allergen_association, back_populates='allergene'
    )

class Zutaten(db.Model):
    __tablename__ = 'zutaten'
    allergene = Mapped[list["Allergene"]] = relationship(
        'Allergen', secondary=zutat_allergen_association, back_populates='zutaten'
    )
    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    gruppe: Mapped[int] = mapped_column(INTEGER(11))
    zusatz_farbst: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_konserv: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_antioxi: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_geschmv: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_gschwefel: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_gschwarz: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_phosphat: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_milcheiw: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_koffein: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_chinin: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_suessung: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_phenylan: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_gwachs: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_taurin: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zutat_name: Mapped[Optional[str]] = mapped_column(TEXT)
    zutat_quelle: Mapped[Optional[str]] = mapped_column(Text)
    zutat_date: Mapped[Optional[datetime.date]] = mapped_column(Date)


class ZutatenProRezept(db.Model):
    __tablename__ = 'zutaten_pro_rezept'

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Rezept_ID: Mapped[int] = mapped_column(INTEGER(11))
    Zutat_ID: Mapped[int] = mapped_column(INTEGER(11))
    Menge: Mapped[decimal.Decimal] = mapped_column(Double(asdecimal=True))
    Einheit: Mapped[int] = mapped_column(INTEGER(11))


class Zutatengruppe(db.Model):
    __tablename__ = 'zutatengruppe'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
